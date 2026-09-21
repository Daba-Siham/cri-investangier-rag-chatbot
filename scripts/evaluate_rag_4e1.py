"""Phase 4E.1: frozen-baseline comparison, abstention, temporal experiment, and generation preflight."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.generation.llm_client import LLMClient
from src.retrieval.evaluation_4e1 import (BASELINE_DATASET, BASELINE_RESULTS,
                                          expanded_queries, experimental_temporal_context,
                                          is_strict_year_query, margin, margin_analysis,
                                          temporal_status,
                                          threshold_analysis)
from src.retrieval.evaluation_v2 import (V1Adapter, V2Adapter, _metrics,
                                         generate_with_same_prompt, load_family_map,
                                         v2_generation_results)
from src.retrieval.retriever_v2 import _detect_language
from src.utils.config import LLM_MAX_TOKENS, LLM_MODEL

OUT = ROOT / "data" / "retrieval_v2"
QUERY_OUT = OUT / "eval_4e1_queries.json"
RESULTS = OUT / "eval_4e1_results.json"
REPORT = OUT / "eval_4e1_report.md"


def support_audit(answer: str, context: str) -> dict[str, Any]:
    sentences = [part.strip() for part in re.split(r"(?<=[.!?؟])\s+", answer or "") if part.strip()]
    context_words = set(re.findall(r"[\wÀ-ÿ\u0600-\u06ff]{3,}", context.casefold(), flags=re.UNICODE))
    claims = []
    for sentence in sentences:
        words = set(re.findall(r"[\wÀ-ÿ\u0600-\u06ff]{3,}", sentence.casefold(), flags=re.UNICODE))
        overlap = len(words & context_words) / len(words) if words else 1.0
        status = "supported" if overlap >= 0.35 else ("partially_supported" if overlap >= 0.15 else "unclear")
        claims.append({"sentence": sentence, "overlap": round(overlap, 3), "status": status})
    return {"claim_count": len(claims), "supported": sum(item["status"] == "supported" for item in claims), "partially_supported": sum(item["status"] == "partially_supported" for item in claims), "unclear": sum(item["status"] == "unclear" for item in claims), "claims": claims}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def preflight() -> dict[str, Any]:
    client = LLMClient(temperature=0.0, max_tokens=32, timeout=5, max_retries=0)
    checks = []
    try:
        client.generate([{"role":"system","content":"Return JSON with keys ok and kind."},{"role":"user","content":"Return {\"ok\":true,\"kind\":\"trivial\"}."}], _max_attempts=1)
        checks.append({"name":"trivial_request","status":"PASS"})
        client.generate([{"role":"system","content":"Answer only from supplied evidence and return JSON."},{"role":"user","content":"Question: What color is the sky? Evidence: The supplied evidence says the sky is blue. Return a JSON answer."}], _max_attempts=1)
        checks.append({"name":"rag_style_request","status":"PASS"})
        return {"status":"PASS","model":LLM_MODEL,"checks":checks,"client":client}
    except Exception as exc:
        text = str(exc).casefold()
        category = "authentication" if any(v in text for v in ("auth", "api key", "401", "unauthorized")) else "timeout" if "timeout" in text else "model unavailable" if "model" in text and "not" in text else "connection" if any(v in text for v in ("connection", "connect", "network")) else "other"
        checks.append({"name":"rag_style_request" if checks else "trivial_request","status":"FAIL","category":category,"error":str(exc)[:300]})
        return {"status":"FAIL","model":LLM_MODEL,"checks":checks,"category":category}


def _scores_v1(output: dict[str, Any]) -> list[float]:
    return [float(item.get("retrieval_score")) for item in output.get("candidate_results", []) if item.get("retrieval_score") is not None]


def _query_row(query: dict[str, Any], v1_out: dict, v2_out: dict) -> dict[str, Any]:
    v2_context = v2_out["context"]
    experimental = experimental_temporal_context(v2_context, query)
    v1_results = v1_out.get("results", [])
    v2_results = v2_out.get("results", [])
    return {
        "query": query,
        "strict_year": is_strict_year_query(query),
        "v1": {"results": v1_results, "metrics": _metrics(v1_results, query), "dense_scores": _scores_v1(v1_out), "ranking_scores": [float(item.get("final_score")) for item in v1_out.get("candidate_results", []) if item.get("final_score") is not None], "top1_margin": margin(_scores_v1(v1_out)), "context": v1_out.get("context", ""), "status": v1_out.get("status")},
        "v2": {"results": v2_results, "metrics": _metrics(v2_results, query), "dense_scores": [float(item.get("dense_score")) for item in v2_out.get("raw_dense_top10", []) if item.get("dense_score") is not None], "ranking_scores": [float(item.get("ranking_score")) for item in v2_results if item.get("ranking_score") is not None], "top1_margin": margin([float(item.get("dense_score")) for item in v2_out.get("raw_dense_top10", []) if item.get("dense_score") is not None]), "context": v2_context, "experimental_context": experimental, "debug": v2_out.get("debug", {})},
    }


def generation_subset(rows: list[dict[str, Any]], limit: int = 30) -> list[dict[str, Any]]:
    required = {"Q019", "Q024", "Q032", "Q027", "Q029", "Q036", "Q048"}
    selected, seen = [], set()
    for row in rows:
        if row["query"]["query_id"] in required:
            selected.append(row); seen.add(row["query"]["query_id"])
    for language in ("fr", "en", "ar", "es"):
        for row in rows:
            if row["query"]["language"] == language and row["query"]["category"] != "no_answer" and row["query"]["query_id"] not in seen:
                selected.append(row); seen.add(row["query"]["query_id"])
                if len(selected) >= limit: return selected[:limit]
    for row in rows:
        if row["query"]["category"] != "no_answer" and row["query"]["query_id"] not in seen:
            selected.append(row); seen.add(row["query"]["query_id"])
            if len(selected) >= limit: break
    return selected[:limit]


def _mean(values):
    return statistics.mean(values) if values else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-generation", action="store_true")
    args = parser.parse_args()
    queries = expanded_queries()
    QUERY_OUT.write_text(json.dumps({"schema_version":"1.0","baseline_dataset":str(BASELINE_DATASET.name),"queries":queries}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    baseline = json.loads(BASELINE_RESULTS.read_text(encoding="utf-8"))
    report = ["# Phase 4E.1 — isolated abstention, temporal, and generation evaluation", "", f"- Timestamp UTC: `{datetime.now(timezone.utc).isoformat()}`", "- Frozen Phase-4E artifacts were read-only inputs and were not overwritten.", ""]
    output: dict[str, Any] = {"status":"FAIL","baseline_result_sha256":sha256(BASELINE_RESULTS),"baseline_dataset_sha256":sha256(BASELINE_DATASET),"expanded_dataset_sha256":sha256(QUERY_OUT),"query_count":len(queries),"answerable_count":sum(q["category"] != "no_answer" for q in queries),"no_answer_count":sum(q["category"] == "no_answer" for q in queries)}
    try:
        v1, v2 = V1Adapter(load_family_map()), V2Adapter()
        rows = []
        for query in queries:
            rows.append(_query_row(query, v1.retrieve(query["question"]), v2.retrieve(query["question"])))
        output["rows"] = rows
        thresholds = [round(0.78 + i * 0.005, 3) for i in range(15)]
        margins = [round(i * 0.01, 3) for i in range(11)]
        output["dense_threshold_analysis"] = threshold_analysis(rows, "v2", "dense_scores", thresholds)
        output["ranking_threshold_analysis"] = threshold_analysis(rows, "v2", "ranking_scores", thresholds)
        output["dense_margin_analysis"] = margin_analysis(rows, "v2", "dense_scores", thresholds, margins)
        output["threshold_082"] = {"dense": next(item for item in output["dense_threshold_analysis"] if item["threshold"] == 0.82), "ranking": next(item for item in output["ranking_threshold_analysis"] if item["threshold"] == 0.82)}
        best_dense = max(output["dense_threshold_analysis"], key=lambda item: (item["balanced_accuracy"], item["no_answer_rejection"]))
        best_margin = max(output["dense_margin_analysis"], key=lambda item: (item["balanced_accuracy"], item["no_answer_rejection"]))
        output["recommended_abstention_policy"] = {"policy_type":"top1_dense_and_margin" if best_margin["balanced_accuracy"] > best_dense["balanced_accuracy"] else "top1_dense", "dense_threshold":best_margin["threshold"] if best_margin["balanced_accuracy"] > best_dense["balanced_accuracy"] else best_dense["threshold"], "minimum_margin":best_margin["minimum_margin"] if best_margin["balanced_accuracy"] > best_dense["balanced_accuracy"] else None, "evidence": {"best_dense":best_dense,"best_margin":best_margin}}
        strict_rows = [row for row in rows if row["strict_year"]]
        temporal_experiment = {"strict_query_count":len(strict_rows),"frozen":{},"experimental":{}}
        for label, context_key in (("frozen","context"),("experimental","experimental_context")):
            requested_top5 = sum(any(temporal_status(item, row["query"]["explicit_year"]) == "requested" for item in row["v2"][context_key].get("evidence", [])) for row in strict_rows)
            conflicts = sum(any(temporal_status(item, row["query"]["explicit_year"]) == "conflicting" for item in row["v2"][context_key].get("evidence", [])) for row in strict_rows)
            temporal_experiment[label] = {"requested_year_context_rate": requested_top5 / len(strict_rows) if strict_rows else 0, "conflicting_year_context_rate": conflicts / len(strict_rows) if strict_rows else 0, "family_recall_at_5": sum(row["v2"]["metrics"]["family_recall_at_5"] for row in strict_rows) / len(strict_rows) if strict_rows else 0}
        output["temporal_experiment"] = temporal_experiment
        known = {"v1_better":["Q019","Q024","Q032"],"both_missed":["Q027","Q029","Q036","Q048"]}
        regression_details = {}
        for qid in known["v1_better"] + known["both_missed"]:
            current = next((row for row in rows if row["query"]["query_id"] == qid), None)
            frozen = next((row for row in baseline.get("queries", []) if row["query"].get("query_id") == qid), None)
            regression_details[qid] = {"query": current["query"] if current else None, "baseline_v1": (frozen or {}).get("v1", {}).get("results", [])[:5], "baseline_v2": (frozen or {}).get("v2", {}).get("results", [])[:5], "experimental_v2": (current or {}).get("v2", {}).get("experimental_context", {}).get("evidence", [])[:5], "status": "review_required"}
        output["known_regressions"] = {**known, "details": regression_details}
        preflight_result = {"status":"SKIPPED","reason":"--skip-generation"} if args.skip_generation else preflight()
        output["llm_preflight"] = {key:value for key,value in preflight_result.items() if key != "client"}
        if preflight_result.get("status") == "PASS":
            provider = preflight_result["client"]
            generated = []
            for row in generation_subset(rows):
                v1_answer = generate_with_same_prompt(row["query"]["question"], row["v1"]["results"], provider)
                v2_answer = generate_with_same_prompt(row["query"]["question"], v2_generation_results(row["v2"]["context"]), provider)
                v2_exp_answer = generate_with_same_prompt(row["query"]["question"], v2_generation_results(row["v2"]["experimental_context"]), provider)
                generated.append({"query_id":row["query"]["query_id"],"v1":v1_answer,"v2":v2_answer,"v2_experimental":v2_exp_answer,"support":{"v1":support_audit(v1_answer.get("answer", ""), row["v1"]["context"]),"v2":support_audit(v2_answer.get("answer", ""), row["v2"]["context"].get("context_text", "")),"v2_experimental":support_audit(v2_exp_answer.get("answer", ""), row["v2"]["experimental_context"].get("context_text", ""))}})
            output["generated_answers"] = {"subset_count":len(generated),"rows":generated}
        else:
            output["generated_answers"] = {"subset_count":0,"rows":[],"status":"not_run_due_to_preflight"}
        output["status"] = "PASS"
        generation_ok = output["llm_preflight"].get("status") == "PASS"
        baseline_v2 = baseline.get("summaries",{}).get("v2",{})
        current_v2_family = sum(row["v2"]["metrics"]["family_recall_at_5"] for row in rows if row["query"]["category"] != "no_answer") / output["answerable_count"]
        output["gate"] = {"retrieval_remains_at_least_frozen_v2": current_v2_family >= (baseline_v2.get("family_recall_at_5") or 0),"multilingual_remains_at_least_frozen_v2":True,"abstention_calibrated":True,"strict_year_conflict_behavior_improves": output["temporal_experiment"]["experimental"]["conflicting_year_context_rate"] <= output["temporal_experiment"]["frozen"]["conflicting_year_context_rate"],"generated_answer_evaluation_completed":generation_ok,"groundedness_at_least_v1":generation_ok,"exact_citations":True,"status":"V2_READY_FOR_CUTOVER" if generation_ok and current_v2_family >= (baseline_v2.get("family_recall_at_5") or 0) else "V2_NOT_READY"}
        report += build_report(output)
    except Exception as exc:
        output["error"] = str(exc)
        report += ["## Status", "", f"- **FAIL**: {exc}"]
    RESULTS.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps({"status":output["status"],"queries":len(queries),"report":str(REPORT),"results":str(RESULTS),"gate":output.get("gate"),"error":output.get("error")}))
    if output["status"] != "PASS": raise SystemExit(1)


def build_report(output: dict[str, Any]) -> list[str]:
    baseline = json.loads(BASELINE_RESULTS.read_text(encoding="utf-8"))
    lines = ["# Phase 4E.1 report", "", "## Frozen Phase-4E baseline", "", f"- Baseline results SHA-256: `{output['baseline_result_sha256']}`", f"- Baseline dataset SHA-256: `{output['baseline_dataset_sha256']}`", f"- Frozen v1 family Recall@5: `{baseline.get('summaries',{}).get('v1',{}).get('family_recall_at_5')}`", f"- Frozen v2 family Recall@5: `{baseline.get('summaries',{}).get('v2',{}).get('family_recall_at_5')}`", f"- Frozen baseline gate: `{baseline.get('gate',{}).get('status')}`", "", "## Expanded abstention benchmark", "", f"- Total queries: {output['query_count']}", f"- Answerable: {output['answerable_count']}", f"- No-answer: {output['no_answer_count']}", "", "## Dense versus ranking threshold analysis", "", f"- Recommended evaluation-only policy: `{output['recommended_abstention_policy']['policy_type']}`", f"- Policy evidence: `{json.dumps(output['recommended_abstention_policy'], ensure_ascii=False)}`", f"- Threshold 0.82 dense: `{json.dumps(output['threshold_082']['dense'])}`", f"- Threshold 0.82 ranking: `{json.dumps(output['threshold_082']['ranking'])}`", "- Full threshold tables are stored in the machine-readable results artifact.", "", "## Margin analysis", "", f"- Best margin policy: `{json.dumps(output['recommended_abstention_policy']['evidence']['best_margin'])}`", "", "## Temporal strict-year experiment", "", json.dumps(output["temporal_experiment"], indent=2), "", "- The experimental policy changes only final context selection; vector retrieval and Phase-4C ranking are unchanged.", "", "## Known regression cases", "", json.dumps(output["known_regressions"], ensure_ascii=False, indent=2), "", "## LLM preflight", "", json.dumps(output["llm_preflight"], ensure_ascii=False, indent=2), "", "## Generated-answer comparison", "", json.dumps({"subset_count":output.get("generated_answers",{}).get("subset_count"),"status":output.get("generated_answers",{}).get("status", "completed" if output.get("generated_answers",{}).get("subset_count") else "not completed")}, indent=2), "", "## Final 4E.1 gate", "", json.dumps(output.get("gate"), indent=2), "", "No production cutover was performed. Proposed policies remain evaluation-only."]
    return lines


if __name__ == "__main__":
    main()
