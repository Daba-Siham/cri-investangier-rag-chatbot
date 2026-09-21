"""Phase 4E.3: evidence-based final gate correction.

This evaluator treats Phase 4E.2 as immutable evidence.  It does not rerun or
tune retrieval; it only validates the frozen retrieval/context rows and, when
the configured LLM is reachable, evaluates a fixed generation subset.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.generation.llm_client import LLMClient
from src.retrieval.evaluation_4e1 import experimental_temporal_context, is_strict_year_query, temporal_status
from src.retrieval.evaluation_v2 import generate_with_same_prompt, v2_generation_results
from src.utils.config import LLM_BASE_URL, LLM_MODEL, LLM_TIMEOUT_SECONDS
from scripts.evaluate_rag_4e1 import generation_subset, support_audit

OUT = ROOT / "data" / "retrieval_v2"
FROZEN_RESULTS = OUT / "eval_4e2_results.json"
FROZEN_QUERIES = OUT / "eval_4e2_queries.json"
FROZEN_4E_RESULTS = OUT / "eval_v1_v2_results.json"
RESULTS = OUT / "eval_4e3_results.json"
REPORT = OUT / "eval_4e3_report.md"
GENERATION_SUBSET = OUT / "eval_4e3_generation_subset.json"
GENERATION_CHECKPOINT = OUT / "eval_4e3_generation_checkpoint.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def sanitized_host(url: str) -> str | None:
    if not url:
        return None
    parsed = urlparse(url)
    return parsed.hostname or (url.split("/", 1)[0] if url else None)


class RateLimitPaused(RuntimeError):
    pass


def is_rate_limit(value: Any) -> bool:
    text = str(value).casefold()
    return "429" in text or "rate limit" in text or "rate_limit" in text or "rate_limit_exceeded" in text


def retry_after_seconds(value: Any) -> float | None:
    match = re.search(r"(?:try again in|retry[- ]after)\s*([0-9]+(?:\.[0-9]+)?)\s*s?", str(value), re.I)
    return float(match.group(1)) if match else None


def atomic_json_write(path: Path, value: Any) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def context_signature(context: dict[str, Any]) -> str:
    payload = {
        "context_text": context.get("context_text", ""),
        "evidence": [item.get("retrieval_chunk_id") for item in context.get("evidence", [])],
        "citations": [item.get("citation_id") for item in context.get("citations", [])],
    }
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def preflight() -> dict[str, Any]:
    """Perform one trivial and one RAG-style request, without retry loops."""
    checks: list[dict[str, Any]] = []
    configuration = {
        "endpoint_host": sanitized_host(LLM_BASE_URL),
        "model": LLM_MODEL or None,
        "api_key_configured": bool(__import__("src.utils.config", fromlist=["LLM_API_KEY"]).LLM_API_KEY),
    }
    if not LLM_BASE_URL or not LLM_MODEL or not configuration["api_key_configured"]:
        missing = [name for name, present in (("URL", bool(LLM_BASE_URL)), ("model", bool(LLM_MODEL)), ("API key", configuration["api_key_configured"])) if not present]
        return {"status": "FAIL", "category": "configuration", "missing": missing, "configuration": configuration, "checks": checks}
    # Groq's strict JSON response can exhaust a 32-token preflight budget
    # before emitting a valid document; keep this diagnostic small but valid.
    client = LLMClient(temperature=0.0, max_tokens=64, timeout=LLM_TIMEOUT_SECONDS, max_retries=0)
    try:
        client.generate(
            [{"role": "system", "content": "Return JSON with keys ok and kind."},
             {"role": "user", "content": 'Return {"ok":true,"kind":"trivial"}.'}],
            _max_attempts=1,
        )
        checks.append({"name": "trivial_request", "status": "PASS"})
    except Exception as exc:
        return {"status": "FAIL", "category": classify_error(exc), "configuration": configuration,
                "checks": checks + [{"name": "trivial_request", "status": "FAIL", "error": str(exc)[:300]}]}
    try:
        client.generate(
            [{"role": "system", "content": "Answer only from supplied evidence and return JSON."},
             {"role": "user", "content": "Question: What color is the sky? Evidence: The supplied evidence says the sky is blue. Return a JSON answer."}],
            _max_attempts=1,
        )
        checks.append({"name": "rag_style_request", "status": "PASS"})
        return {"status": "PASS", "configuration": configuration, "checks": checks, "client": client}
    except Exception as exc:
        return {"status": "FAIL", "category": classify_error(exc), "configuration": configuration,
                "checks": checks + [{"name": "rag_style_request", "status": "FAIL", "error": str(exc)[:300]}]}


def classify_error(exc: Exception) -> str:
    text = str(exc).casefold()
    if "rate limit" in text or "429" in text or "rate_limit" in text:
        return "rate limit"
    if any(value in text for value in ("auth", "api key", "401", "unauthorized")):
        return "authentication"
    if "timeout" in text or "timed out" in text:
        return "timeout"
    if "model" in text and ("not" in text or "unavailable" in text):
        return "model availability"
    if any(value in text for value in ("connection", "connect", "network", "dns")):
        return "connection"
    return "other"


def citation_integrity(context: dict[str, Any]) -> dict[str, Any]:
    evidence = context.get("evidence", [])
    citations = context.get("citations", [])
    by_evidence = {item.get("evidence_id"): item for item in evidence}
    failures: list[str] = []
    for citation in citations:
        evidence_id = citation.get("evidence_id")
        item = by_evidence.get(evidence_id)
        if not item:
            failures.append(f"missing_evidence:{evidence_id}")
            continue
        if citation.get("retrieval_chunk_id") != item.get("retrieval_chunk_id"):
            failures.append(f"retrieval_mismatch:{evidence_id}")
        if citation.get("source_pages") != item.get("source_pages"):
            failures.append(f"pages_mismatch:{evidence_id}")
        if not item.get("source_spans") or not item.get("text", "").strip():
            failures.append(f"empty_provenance:{evidence_id}")
    return {"valid": not failures and len(citations) == len(evidence), "citation_count": len(citations), "evidence_count": len(evidence), "failures": failures}


def aggregate_generation(generated: list[dict[str, Any]], system: str) -> dict[str, Any]:
    rows = [row for row in generated if row[system].get("status") == "answered" and row[system].get("answer", "").strip()]
    attempted = len(generated)
    succeeded = len(rows)
    claims = [claim for row in rows for claim in row["evaluation"][system]["judge"].get("claims", [])]
    judge_attempted = sum(row[system].get("status") == "answered" and row[system].get("answer", "").strip() != "" for row in generated)
    judge_succeeded = sum(row["evaluation"][system]["judge"].get("status") == "PASS" for row in generated)
    judge_failed = judge_attempted - judge_succeeded
    total = len(claims)
    supported = sum(claim["status"] == "supported" for claim in claims)
    partial = sum(claim["status"] == "partially_supported" for claim in claims)
    unsupported = sum(claim["status"] == "unsupported" for claim in claims)
    unclear = sum(claim["status"] == "unclear" for claim in claims)
    return {
        "attempted": attempted, "succeeded": succeeded, "failed": attempted - succeeded,
        "success_rate": succeeded / attempted if attempted else 0.0,
        "judge_attempted": judge_attempted, "judge_succeeded": judge_succeeded,
        "judge_failed": judge_failed, "judge_success_rate": judge_succeeded / judge_attempted if judge_attempted else 0.0,
        "total_factual_claims": total,
        "supported_claim_rate": supported / total if total else None,
        "partially_supported_rate": partial / total if total else None,
        "unsupported_claim_rate": unsupported / total if total else None,
        "unclear_claim_rate": unclear / total if total else None,
        "language_compliance_rate": mean(row["evaluation"][system]["language_compliant"] for row in rows) if rows else None,
        "relevance_pass_rate": mean(row["evaluation"][system]["relevance_pass"] for row in rows if row["evaluation"][system]["relevance_pass"] is not None) if any(row["evaluation"][system]["relevance_pass"] is not None for row in rows) else None,
        "completeness_pass_rate": mean(row["evaluation"][system]["completeness_pass"] for row in rows if row["evaluation"][system]["completeness_pass"] is not None) if any(row["evaluation"][system]["completeness_pass"] is not None for row in rows) else None,
        "citation_validation_pass_rate": mean(row["evaluation"][system]["citation_validation"]["citation_validation_pass"] for row in rows) if rows else None,
        "language_breakdown": {
            language: {
                "count": sum(row["query"].get("language") == language for row in rows),
                "compliance_rate": mean(row["evaluation"][system]["language_compliant"] for row in rows if row["query"].get("language") == language) if any(row["query"].get("language") == language for row in rows) else None,
            }
            for language in ("fr", "en", "ar", "es")
        },
    }


def language_compliant(answer: str, language: str) -> bool:
    if not answer.strip():
        return False
    arabic = len(re.findall(r"[\u0600-\u06ff]", answer))
    latin = len(re.findall(r"[A-Za-zÀ-ÿÁ-ÿ]", answer))
    if language == "ar":
        return arabic >= max(3, latin // 3)
    if language in {"fr", "en", "es"}:
        return latin >= max(3, arabic * 3)
    return True


def claim_evaluation(answer: str, context: str, language: str) -> dict[str, Any]:
    # This is deliberately secondary to the evidence-only judge. It is still
    # useful if the endpoint is available but a judge response is malformed.
    audit = support_audit(answer, context)
    claims = []
    for item in audit.get("claims", []):
        status = item.get("status", "unclear")
        claims.append({"claim": item.get("sentence", ""), "status": status, "evidence_ids": []})
    return {
        "claims": claims,
        "lexical_secondary": audit,
        "language_compliant": language_compliant(answer, language),
        "relevance_pass": bool(answer.strip()),
        "completeness_pass": bool(answer.strip()),
    }


def evidence_judge(provider: Any, question: str, context: str, answer: str) -> dict[str, Any]:
    """Ask the configured model for an evidence-only claim audit."""
    if not answer.strip():
        return {"status": "not_applicable", "claims": []}
    messages = [
        {"role": "system", "content": "Audit only the supplied answer against the supplied evidence. Do not use outside knowledge. Return JSON: {\"claims\":[{\"claim\":string,\"status\":\"supported|partially_supported|unsupported|unclear\",\"evidence_ids\":[string]}],\"relevance\":\"pass|fail\",\"completeness\":\"pass|fail\"}."},
        {"role": "user", "content": f"Question:\n{question}\n\nEvidence:\n{context}\n\nAnswer to audit:\n{answer}"},
    ]
    try:
        raw = provider.generate(messages, _max_attempts=1)
        parsed = json.loads(raw)
        claims = parsed.get("claims") if isinstance(parsed, dict) else None
        if not isinstance(claims, list):
            raise ValueError("judge claims missing")
        if parsed.get("relevance") not in {"pass", "fail"} or parsed.get("completeness") not in {"pass", "fail"}:
            raise ValueError("judge relevance/completeness missing")
        allowed = {"supported", "partially_supported", "unsupported", "unclear"}
        normalized = []
        for claim in claims:
            if not isinstance(claim, dict) or claim.get("status") not in allowed:
                raise ValueError("invalid judge claim")
            normalized.append({"claim": str(claim.get("claim", "")), "status": claim["status"], "evidence_ids": claim.get("evidence_ids", [])})
        return {"status": "PASS", "claims": normalized, "relevance": parsed["relevance"], "completeness": parsed["completeness"]}
    except Exception as exc:
        return {"status": "FAIL", "error": str(exc)[:300], "claims": []}


def validate_generated_citations(answer: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    """Validate the production AnswerGenerator citation contract for v2.

    AnswerGenerator returns mapped citations with ``source_id`` values such as
    SOURCE_1.  Those IDs must resolve to the exact source records supplied to
    the generator, and the corresponding Phase-4D context must already pass
    its provenance validation.
    """
    evidence = context.get("evidence", [])
    provenance = citation_integrity(context)
    valid_source_ids = {f"SOURCE_{index}" for index in range(1, len(evidence) + 1)}
    emitted = [item.get("source_id") for item in answer.get("citations", []) if isinstance(item, dict)]
    valid = [value for value in emitted if value in valid_source_ids]
    unknown = [value for value in emitted if value not in valid_source_ids]
    answer_has_citations = answer.get("status") == "answered" and bool(emitted)
    passed = bool(answer_has_citations and not unknown and provenance["valid"] and len(valid) == len(emitted))
    return {
        "emitted_citation_ids": emitted,
        "valid_citation_ids": valid,
        "unknown_citation_ids": unknown,
        "context_provenance_valid": provenance["valid"],
        "citation_validation_pass": passed,
    }


def run_generation(rows: list[dict[str, Any]], provider: Any, args: argparse.Namespace) -> dict[str, Any]:
    selected = generation_subset(rows, limit=30)
    selected_ids = [row["query"]["query_id"] for row in selected]
    GENERATION_SUBSET.write_text(json.dumps([row["query"] for row in selected], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint: dict[str, Any] = {"schema_version": "4e3-generation-1", "subset_query_ids": selected_ids, "rows": {}, "stats": {"actual_llm_calls": 0, "avoided_llm_calls": 0, "rate_limit_events": [], "total_rate_limit_wait_seconds": 0.0, "resumed_queries": 0}}
    if GENERATION_CHECKPOINT.exists():
        try:
            previous = json.loads(GENERATION_CHECKPOINT.read_text(encoding="utf-8"))
            if previous.get("subset_query_ids") == selected_ids:
                checkpoint = previous
                checkpoint.setdefault("rows", {})
                checkpoint.setdefault("stats", {})
                checkpoint["stats"].setdefault("actual_llm_calls", 0)
                checkpoint["stats"].setdefault("avoided_llm_calls", 0)
                checkpoint["stats"].setdefault("rate_limit_events", [])
                checkpoint["stats"].setdefault("total_rate_limit_wait_seconds", 0.0)
                checkpoint["stats"]["resumed_queries"] = sum(bool(value) for value in checkpoint["rows"].values())
        except (OSError, json.JSONDecodeError):
            pass
    stats = checkpoint["stats"]

    def save() -> None:
        checkpoint["stats"] = stats
        atomic_json_write(GENERATION_CHECKPOINT, checkpoint)

    def paced_call(fn, query_id: str, system: str, phase: str):
        for retry_number in range(args.max_rate_limit_retries + 1):
            if stats["actual_llm_calls"] and args.request_delay_seconds > 0:
                time.sleep(args.request_delay_seconds)
            stats["actual_llm_calls"] += 1
            result = fn()
            error_text = result.get("error", "") if isinstance(result, dict) else ""
            failed = isinstance(result, dict) and result.get("status") in {"generation_error", "FAIL"}
            if not (failed and is_rate_limit(error_text)):
                return result
            retry_after = retry_after_seconds(error_text)
            delay = max(args.rate_limit_wait_seconds, retry_after or 0.0)
            stats["rate_limit_events"].append({"query_id": query_id, "system": system, "phase": phase, "retry_number": retry_number + 1, "status": "429", "retry_delay_seconds": delay})
            stats["total_rate_limit_wait_seconds"] += delay
            save()
            if retry_number >= args.max_rate_limit_retries:
                raise RateLimitPaused(f"rate-limit retries exhausted for {query_id}/{system}/{phase}")
            time.sleep(delay)
        raise RateLimitPaused("rate-limit retry loop exhausted")

    def system_complete(entry: dict[str, Any], system: str) -> bool:
        answer = entry.get(system, {})
        evaluation = entry.get("evaluation", {}).get(system, {})
        return answer.get("status") == "answered" and bool(answer.get("answer", "").strip()) and evaluation.get("judge", {}).get("status") == "PASS"

    def complete_evaluation(entry: dict[str, Any], query: dict[str, Any], system: str, answer: dict[str, Any], context: str, context_obj: dict[str, Any] | None) -> None:
        evaluation = claim_evaluation(answer.get("answer", ""), context, query["language"])
        evaluation["citation_validation"] = validate_generated_citations(answer, context_obj) if system == "v2" and context_obj is not None else {"citation_validation_pass": False, "emitted_citation_ids": [], "valid_citation_ids": [], "unknown_citation_ids": []}
        judge = paced_call(lambda: evidence_judge(provider, query["question"], context, answer.get("answer", "")), query["query_id"], system, "judge")
        evaluation["judge"] = judge
        evaluation["relevance_pass"] = judge.get("relevance") == "pass" if judge.get("status") == "PASS" else None
        evaluation["completeness_pass"] = judge.get("completeness") == "pass" if judge.get("status") == "PASS" else None
        entry.setdefault("evaluation", {})[system] = evaluation

    generated: list[dict[str, Any]] = []
    try:
        for source_row in selected:
            query = source_row["query"]
            qid = query["query_id"]
            entry = checkpoint["rows"].setdefault(qid, {"query_id": qid, "query": query})
            v1_context = source_row["v1"].get("context", "")
            v2_context_obj = source_row["v2"]["context"]
            experimental_context_obj = source_row["v2"]["experimental_context"]
            v2_context = v2_context_obj.get("context_text", "")
            experimental_context = experimental_context_obj.get("context_text", "")
            same_experimental = context_signature(v2_context_obj) == context_signature(experimental_context_obj)
            entry["experimental_generation_reused"] = same_experimental

            systems = (("v1", source_row["v1"].get("results", []), v1_context, None), ("v2", v2_generation_results(v2_context_obj), v2_context, v2_context_obj))
            for system, retrieval_results, context, context_obj in systems:
                if not system_complete(entry, system):
                    started = time.perf_counter()
                    answer = paced_call(lambda rr=retrieval_results: generate_with_same_prompt(query["question"], rr, provider), qid, system, "generation")
                    answer["evaluation_ms"] = (time.perf_counter() - started) * 1000
                    entry[system] = answer
                    entry.setdefault("evaluation", {})[system] = {"claims": [], "language_compliant": False, "relevance_pass": None, "completeness_pass": None, "citation_validation": {"citation_validation_pass": False, "emitted_citation_ids": [], "valid_citation_ids": [], "unknown_citation_ids": []}, "judge": {"status": "not_applicable", "claims": []}}
                    if answer.get("status") == "answered" and answer.get("answer", "").strip():
                        complete_evaluation(entry, query, system, answer, context, context_obj)
                    save()

            if same_experimental and system_complete(entry, "v2"):
                if not system_complete(entry, "v2_experimental"):
                    entry["v2_experimental"] = copy.deepcopy(entry["v2"])
                    entry.setdefault("evaluation", {})["v2_experimental"] = copy.deepcopy(entry["evaluation"]["v2"])
                    stats["avoided_llm_calls"] += 2
                    save()
            elif not system_complete(entry, "v2_experimental"):
                if "v2_experimental" not in entry or not entry["v2_experimental"].get("answer"):
                    started = time.perf_counter()
                    answer = paced_call(lambda: generate_with_same_prompt(query["question"], v2_generation_results(experimental_context_obj), provider), qid, "v2_experimental", "generation")
                    answer["evaluation_ms"] = (time.perf_counter() - started) * 1000
                    entry["v2_experimental"] = answer
                if entry["v2_experimental"].get("status") == "answered" and entry["v2_experimental"].get("answer", "").strip():
                    complete_evaluation(entry, query, "v2_experimental", entry["v2_experimental"], experimental_context, experimental_context_obj)
                save()

            if all(system_complete(entry, system) for system in ("v1", "v2", "v2_experimental")):
                entry["completed"] = True
            save()
            generated.append(entry)
    except RateLimitPaused as exc:
        save()
        complete = [entry for entry in checkpoint["rows"].values() if entry.get("completed")]
        return {"status": "RATE_LIMIT_PAUSED", "pause_reason": str(exc), "subset_count": len(selected), "completed_queries": len(complete), "attempted": stats["actual_llm_calls"], "succeeded": 0, "failed": 0, "success_rate": 0.0, "system_success": {}, "stats": stats, "rows": list(checkpoint["rows"].values())}
    complete = [entry for entry in checkpoint["rows"].values() if entry.get("completed")]
    system_success = {}
    for system in ("v1", "v2", "v2_experimental"):
        succeeded = sum(entry.get(system, {}).get("status") == "answered" and bool(entry.get(system, {}).get("answer", "").strip()) for entry in checkpoint["rows"].values())
        attempted = len(selected)
        system_success[system] = {"attempted": attempted, "succeeded": succeeded, "failed": attempted - succeeded, "success_rate": succeeded / attempted if attempted else 0.0}
    attempted = sum(item["attempted"] for item in system_success.values())
    succeeded = sum(item["succeeded"] for item in system_success.values())
    status = "COMPLETED" if len(complete) == len(selected) else "INCOMPLETE"
    return {"status": status, "subset_count": len(selected), "completed_queries": len(complete), "attempted": stats["actual_llm_calls"], "succeeded": succeeded, "failed": attempted - succeeded, "success_rate": succeeded / attempted if attempted else 0.0, "system_success": system_success, "stats": stats, "rows": list(checkpoint["rows"].values())}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-generation", action="store_true")
    parser.add_argument("--request-delay-seconds", type=float, default=3.0)
    parser.add_argument("--rate-limit-wait-seconds", type=float, default=60.0)
    parser.add_argument("--max-rate-limit-retries", type=int, default=5)
    args = parser.parse_args()
    frozen = json.loads(FROZEN_RESULTS.read_text(encoding="utf-8"))
    frozen_4e = json.loads(FROZEN_4E_RESULTS.read_text(encoding="utf-8"))
    query_artifact = json.loads(FROZEN_QUERIES.read_text(encoding="utf-8"))
    rows = frozen.get("rows", [])
    output: dict[str, Any] = {
        "status": "PASS",
        "frozen_4e2_results_sha256": sha256(FROZEN_RESULTS),
        "frozen_4e2_queries_sha256": sha256(FROZEN_QUERIES),
        "frozen_4e_results_sha256": sha256(FROZEN_4E_RESULTS),
        "frozen_4e2_gate": frozen.get("gate"),
        "query_count": len(query_artifact.get("queries", [])),
        "answerable_count": sum(item.get("category") != "no_answer" for item in query_artifact.get("queries", [])),
        "no_answer_count": sum(item.get("category") == "no_answer" for item in query_artifact.get("queries", [])),
        "frozen_calibration": {
            "threshold": frozen.get("recommended_evaluation_policy", {}).get("threshold"),
            "evidence": frozen.get("recommended_evaluation_policy", {}).get("evidence"),
            "temporal_experiment": frozen.get("temporal_experiment"),
        },
    }
    report = ["# Phase 4E.3 — final evidence-based evaluation gate", "", f"- Timestamp UTC: `{datetime.now(timezone.utc).isoformat()}`", "- Phase 4E, 4E.1, and 4E.2 artifacts were read-only inputs.", ""]

    # Validate the frozen context citations before attempting generation.
    citation_checks = [citation_integrity(row.get("v2", {}).get("context", {})) for row in rows]
    citation_valid = sum(check["valid"] for check in citation_checks)
    output["frozen_context_citation_validation"] = {"checked": len(citation_checks), "passed": citation_valid, "pass_rate": citation_valid / len(citation_checks) if citation_checks else 0.0, "failures": [failure for check in citation_checks for failure in check["failures"]]}

    preflight_result = {"status": "SKIPPED", "reason": "--skip-generation"} if args.skip_generation else preflight()
    output["llm_preflight"] = {key: value for key, value in preflight_result.items() if key != "client"}
    if preflight_result.get("status") == "PASS":
        output["generated_answers"] = run_generation(rows, preflight_result["client"], args)
    else:
        output["generated_answers"] = {"status": "NOT_EVALUATED", "subset_count": 0, "attempted": 0, "succeeded": 0, "failed": 0, "success_rate": 0.0, "rows": []}

    generation = output["generated_answers"]
    if generation.get("status") == "COMPLETED":
        for system in ("v1", "v2", "v2_experimental"):
            output.setdefault("generation_metrics", {})[system] = aggregate_generation(generation["rows"], system)
        output["generation_metrics"]["required_success_rate"] = 1.0
        output["generation_metrics"]["success_requirement_met"] = all(output["generation_metrics"][system]["success_rate"] == 1.0 for system in ("v1", "v2", "v2_experimental"))
        # A judge is required for the primary groundedness gate; lexical audit is secondary.
        for system in ("v1", "v2", "v2_experimental"):
            judge_claims = [claim for row in generation["rows"] for claim in row["evaluation"][system]["judge"].get("claims", [])]
            output["generation_metrics"][system]["judge_claim_count"] = len(judge_claims)
            output["generation_metrics"][system]["judge_failed"] = sum(row["evaluation"][system]["judge"].get("status") == "FAIL" for row in generation["rows"])
            if judge_claims:
                output["generation_metrics"][system]["judge_supported_claim_rate"] = sum(c["status"] == "supported" for c in judge_claims) / len(judge_claims)
                output["generation_metrics"][system]["judge_unsupported_claim_rate"] = sum(c["status"] == "unsupported" for c in judge_claims) / len(judge_claims)
            else:
                output["generation_metrics"][system]["judge_supported_claim_rate"] = None
                output["generation_metrics"][system]["judge_unsupported_claim_rate"] = None
    else:
        output["generation_metrics"] = {system: {"status": "NOT_EVALUATED", "supported_claim_rate": None, "unsupported_claim_rate": None, "language_compliance_rate": None, "relevance_pass_rate": None, "completeness_pass_rate": None} for system in ("v1", "v2", "v2_experimental")}

    # Evidence-derived retrieval/temporal gate fields. No constants stand in for measured values.
    answerable_rows = [row for row in rows if row.get("query", {}).get("category") != "no_answer"]
    current_family_recall = mean(bool(row.get("v2", {}).get("metrics", {}).get("family_recall_at_5")) for row in answerable_rows) if answerable_rows else 0.0
    frozen_family_recall = frozen_4e.get("summaries", {}).get("v2", {}).get("family_recall_at_5")
    frozen_language_baseline = frozen_4e.get("summaries", {}).get("v2", {}).get("by_language", {})
    languages = {}
    for language in ("fr", "en", "ar", "es"):
        group = [row for row in answerable_rows if row["query"].get("language") == language]
        measured = mean(bool(row["v2"]["metrics"].get("family_recall_at_5")) for row in group) if group else None
        frozen_measured = frozen_language_baseline.get(language, {}).get("family_recall_at_5")
        languages[language] = {"count": len(group), "frozen_recall_at_5": frozen_measured, "evaluated_recall_at_5": measured, "not_worse": measured is not None and frozen_measured is not None and measured >= frozen_measured}
    temporal = frozen.get("temporal_experiment", {})
    calibration = frozen.get("recommended_evaluation_policy", {})
    system_success = generation.get("system_success", {})
    required_systems = ("v1", "v2", "v2_experimental")
    generation_complete = (
        generation.get("status") == "COMPLETED"
        and generation.get("subset_count", 0) >= 30
        and all(system_success.get(system, {}).get("success_rate") == 1.0 for system in required_systems)
    )
    judge_complete = generation_complete and all(output["generation_metrics"].get(system, {}).get("judge_success_rate") == 1.0 for system in required_systems)
    if generation_complete:
        gm = output["generation_metrics"]
        grounded = bool(judge_complete and gm["v2"].get("judge_supported_claim_rate") is not None and gm["v1"].get("judge_supported_claim_rate") is not None and gm["v2"]["judge_supported_claim_rate"] >= gm["v1"]["judge_supported_claim_rate"] and gm["v2"].get("judge_unsupported_claim_rate") is not None and gm["v1"].get("judge_unsupported_claim_rate") is not None and gm["v2"]["judge_unsupported_claim_rate"] <= gm["v1"]["judge_unsupported_claim_rate"])
        relevance = bool(judge_complete and gm["v2"].get("relevance_pass_rate") is not None and gm["v1"].get("relevance_pass_rate") is not None and gm["v2"]["relevance_pass_rate"] >= gm["v1"]["relevance_pass_rate"])
        completeness = bool(judge_complete and gm["v2"].get("completeness_pass_rate") is not None and gm["v1"].get("completeness_pass_rate") is not None and gm["v2"]["completeness_pass_rate"] >= gm["v1"]["completeness_pass_rate"])
        language_ok = bool(judge_complete and all(gm["v2"]["language_breakdown"][language].get("compliance_rate") is not None and gm["v1"]["language_breakdown"][language].get("compliance_rate") is not None and gm["v2"]["language_breakdown"][language]["compliance_rate"] >= gm["v1"]["language_breakdown"][language]["compliance_rate"] for language in ("fr", "en", "ar", "es")))
        citation_rate = gm["v2"].get("citation_validation_pass_rate")
        citation_gate = bool(generation_complete and citation_rate is not None and citation_rate == 1.0)
    else:
        grounded = relevance = completeness = language_ok = citation_gate = False
    output["gate_metrics"] = {"v2_family_recall_at_5": current_family_recall, "frozen_v2_family_recall_at_5": frozen_family_recall, "language_breakdown": languages, "generation_success_rate": generation.get("success_rate", 0.0), "frozen_context_citation_pass_rate": output["frozen_context_citation_validation"]["pass_rate"]}
    critical_details: list[str] = []
    if frozen_family_recall is not None and current_family_recall < frozen_family_recall:
        critical_details.append("retrieval_below_frozen_v2")
    if any(value["evaluated_recall_at_5"] is None or value["frozen_recall_at_5"] is None for value in languages.values()):
        critical_details.append("missing_language_group_evidence")
    if temporal.get("experimental", {}).get("conflicting_year_context_rate", 1.0) >= temporal.get("frozen", {}).get("conflicting_year_context_rate", 1.0):
        critical_details.append("temporal_conflict_improvement_not_preserved")
    if output["frozen_context_citation_validation"]["pass_rate"] < 1.0:
        critical_details.append("frozen_context_citation_validation_failure")
    output["critical_regression_details"] = critical_details
    if preflight_result.get("status") == "PASS" and not generation_complete:
        critical_details.append("generation_benchmark_incomplete")
    if preflight_result.get("status") == "PASS" and generation_complete and not judge_complete:
        critical_details.append("evidence_judge_benchmark_incomplete")
    if generation_complete and output["generation_metrics"]["v2"].get("citation_validation_pass_rate") != 1.0:
        critical_details.append("generated_citation_validation_failure")
    if generation_complete and output["generation_metrics"]["v2"].get("judge_unsupported_claim_rate") is not None and output["generation_metrics"]["v1"].get("judge_unsupported_claim_rate") is not None and output["generation_metrics"]["v2"]["judge_unsupported_claim_rate"] > output["generation_metrics"]["v1"]["judge_unsupported_claim_rate"] + 0.05:
        critical_details.append("v2_unsupported_claim_rate_worse_than_v1")
    output["critical_regression_details"] = critical_details
    gate = {
        "unicode_dataset_validation": bool(frozen.get("unicode_dataset_validation", {}).get("status") == "PASS"),
        "retrieval_at_least_frozen_v2": bool(frozen_family_recall is not None and current_family_recall >= frozen_family_recall),
        "multilingual_acceptable": bool(all(value["not_worse"] for value in languages.values())),
        "abstention_calibrated": bool(calibration.get("threshold") == 0.825 and calibration.get("evidence", {}).get("false_acceptance_rate") == 0.0),
        "temporal_improvement_preserved": bool(temporal.get("experimental", {}).get("conflicting_year_context_rate", 1.0) < temporal.get("frozen", {}).get("conflicting_year_context_rate", 1.0)),
        "generation_evaluation_completed": generation_complete,
        "generation_success_rate": generation.get("success_rate", 0.0),
        "judge_success_requirement_met": judge_complete,
        "v1_supported_claim_rate": output["generation_metrics"]["v1"].get("judge_supported_claim_rate"),
        "v2_supported_claim_rate": output["generation_metrics"]["v2"].get("judge_supported_claim_rate"),
        "v1_unsupported_claim_rate": output["generation_metrics"]["v1"].get("judge_unsupported_claim_rate"),
        "v2_unsupported_claim_rate": output["generation_metrics"]["v2"].get("judge_unsupported_claim_rate"),
        "groundedness_at_least_v1": grounded,
        "answer_relevance_at_least_v1": relevance,
        "answer_completeness_at_least_v1": completeness,
        "answer_language_at_least_v1": language_ok,
        "citation_validation_pass_rate": 1.0 if citation_gate else (None if not generation_complete else 0.0),
        "exact_citations": citation_gate,
        "critical_regressions": len(critical_details),
    }
    gate["status"] = "V2_READY_FOR_CUTOVER" if all(gate[key] for key in ("unicode_dataset_validation", "retrieval_at_least_frozen_v2", "multilingual_acceptable", "abstention_calibrated", "temporal_improvement_preserved", "generation_evaluation_completed", "judge_success_requirement_met", "groundedness_at_least_v1", "answer_relevance_at_least_v1", "answer_completeness_at_least_v1", "answer_language_at_least_v1", "exact_citations")) and gate["critical_regressions"] == 0 else "V2_NOT_READY"
    output["gate"] = gate
    report += build_report(output)
    RESULTS.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps({"status": output["status"], "report": str(REPORT), "results": str(RESULTS), "gate": output["gate"]}, ensure_ascii=False))


def build_report(output: dict[str, Any]) -> list[str]:
    lines = [
        "## Frozen retrieval evidence", "", f"- Frozen 4E.2 results SHA-256: `{output['frozen_4e2_results_sha256']}`", f"- Frozen 4E.2 queries SHA-256: `{output['frozen_4e2_queries_sha256']}`", f"- Query composition: {output['query_count']} total / {output['answerable_count']} answerable / {output['no_answer_count']} no-answer.", f"- Frozen context citation validation: `{output['frozen_context_citation_validation']['pass_rate']:.3f}`.", "", "## LLM preflight", "", json.dumps(output["llm_preflight"], ensure_ascii=False, indent=2), "", "## Generation execution", "", json.dumps({key: value for key, value in output["generated_answers"].items() if key != "rows"}, ensure_ascii=False, indent=2), "", "## Groundedness, relevance, completeness, and language", "", json.dumps(output["generation_metrics"], ensure_ascii=False, indent=2), "", "## Evidence-derived gate measurements", "", json.dumps(output["gate_metrics"], ensure_ascii=False, indent=2), "", "## Final 4E.3 gate", "", json.dumps(output["gate"], ensure_ascii=False, indent=2), "", "No production cutover was performed; no corpus, collection, or ranking artifact was modified.",
    ]
    if output["generated_answers"]["status"] != "COMPLETED":
        lines += ["", "Generation is `NOT_EVALUATED`; groundedness, answer quality, and generated-answer citation validity are not claimed."]
    return lines


if __name__ == "__main__":
    main()
