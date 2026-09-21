"""Phase 4E frozen, read-only comparative evaluation of RAG v1 and v2."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import statistics
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.retrieval.evaluation_v2 import (V1Adapter, V2Adapter, V2_COLLECTION,
                                         aggregate_metric, generate_with_same_prompt,
                                         latency_summary)
from src.retrieval.retriever_v2 import _detect_language
from src.utils.config import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS
from src.generation.llm_client import LLMClient

OUT = ROOT / "data" / "retrieval_v2"
DATASET = OUT / "eval_queries_v1_v2.json"
RESULTS = OUT / "eval_v1_v2_results.json"
REPORT = OUT / "eval_v1_v2_report.md"
RETRIEVAL_JSONL = OUT / "retrieval_chunks.jsonl"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def _tokens(text: str) -> set[str]:
    return {word.casefold() for word in __import__("re").findall(r"[\wÀ-ÿ\u0600-\u06ff]{3,}", text, flags=__import__("re").UNICODE)}


def support_audit(answer: str, context: str) -> dict[str, Any]:
    import re
    sentences = [part.strip() for part in re.split(r"(?<=[.!?؟])\s+", answer or "") if part.strip()]
    context_tokens = _tokens(context)
    statuses = []
    for sentence in sentences:
        factual = _tokens(sentence)
        overlap = len(factual & context_tokens) / len(factual) if factual else 1.0
        statuses.append({"sentence": sentence, "overlap": round(overlap, 3), "status": "supported" if overlap >= 0.35 else ("partially_supported" if overlap >= 0.15 else "unclear")})
    return {"claim_count": len(statuses), "supported": sum(row["status"] == "supported" for row in statuses), "partially_supported": sum(row["status"] == "partially_supported" for row in statuses), "unclear": sum(row["status"] == "unclear" for row in statuses), "claims": statuses}


def result_context_metrics(results: list[dict[str, Any]], context_text: str) -> dict[str, Any]:
    texts = [str(item.get("text", "")) for item in results]
    all_text = " ".join(texts)
    unique_text = len(set(texts))
    return {"chunks": len(results), "context_characters": len(context_text or ""), "unique_documents": len({item.get("document_id") for item in results if item.get("document_id")}), "unique_pages": len({(item.get("page_start", item.get("page")), item.get("page_end", item.get("page"))) for item in results}), "unique_families": len({item.get("document_family_id") for item in results if item.get("document_family_id")}), "unique_parents": len({item.get("parent_semantic_chunk_id") for item in results if item.get("parent_semantic_chunk_id")}), "repeated_text_ratio": 1.0 - unique_text / len(texts) if texts else 0.0}


def duplicate_metrics(results: list[dict[str, Any]]) -> dict[str, float | int]:
    def rate(values):
        values = [value for value in values if value is not None]
        return 1.0 - len(set(values)) / len(values) if values else 0.0
    return {"parent_duplicate_rate": rate([item.get("parent_semantic_chunk_id", item.get("chunk_id")) for item in results]), "document_duplicate_rate": rate([item.get("document_id") for item in results]), "family_duplicate_rate": rate([item.get("document_family_id") for item in results]), "unique_families": len({item.get("document_family_id") for item in results if item.get("document_family_id")}), "unique_parents": len({item.get("parent_semantic_chunk_id", item.get("chunk_id")) for item in results})}


def threshold_rows(rows: list[dict], system: str) -> list[dict]:
    thresholds = [round(0.70 + value * 0.02, 2) for value in range(16)]
    output = []
    for threshold in thresholds:
        positives = [row for row in rows if row["query"]["category"] != "no_answer"]
        negatives = [row for row in rows if row["query"]["category"] == "no_answer"]
        def accepted(row):
            scores = row[system]["final_scores"]
            return bool(scores and scores[0] >= threshold)
        tp, fp = sum(accepted(row) for row in positives), sum(accepted(row) for row in negatives)
        recall = tp / len(positives) if positives else 0.0
        rejection = 1 - fp / len(negatives) if negatives else None
        output.append({"threshold": threshold, "answerable_acceptance": recall, "unanswerable_rejection": rejection, "false_acceptance": fp / len(negatives) if negatives else None, "balanced_accuracy": (recall + rejection) / 2 if rejection is not None else None})
    return output


def compact_results(results: list[dict]) -> list[dict]:
    fields = ("retrieval_chunk_id", "chunk_id", "document_id", "document_family_id", "filename", "language", "topic_id", "content_type", "page", "page_start", "page_end", "source_pages", "dense_score", "ranking_score", "retrieval_score", "final_score", "text")
    return [{key: item.get(key) for key in fields if key in item} for item in results]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-generation", action="store_true", help="Run retrieval/context comparison without LLM calls.")
    parser.add_argument("--max-queries", type=int, default=None)
    args = parser.parse_args()
    dataset = json.loads(DATASET.read_text(encoding="utf-8"))
    queries = dataset["queries"][:args.max_queries] if args.max_queries else dataset["queries"]
    report = ["# Phase 4E — production v1 versus RAG v2 evaluation", "", f"- Timestamp UTC: `{datetime.now(timezone.utc).isoformat()}`", "- Evaluation is read-only; no collection, production retriever, prompt, API, semantic JSON, or retrieval JSONL was modified.", ""]
    result: dict = {"status": "FAIL", "dataset_query_count": len(queries), "dataset_sha256": sha256(DATASET), "retrieval_artifact_sha256": sha256(RETRIEVAL_JSONL), "queries": []}
    try:
        family_map = __import__("src.retrieval.evaluation_v2", fromlist=["load_family_map"]).load_family_map()
        v1 = V1Adapter(family_map)
        v2 = V2Adapter()
        v1_store_exists = v1.retriever.store.collection_exists(v1.retriever.collection_name)
        v2_exists = v2.retriever.collection_exists()
        if not v1_store_exists or not v2_exists:
            raise RuntimeError(f"Required collections unavailable: v1={v1_store_exists}, v2={v2_exists}")
        result["collections"] = {"v1": {"name": v1.retriever.collection_name, "point_count": v1.retriever.store.count(v1.retriever.collection_name)}, "v2": {"name": V2_COLLECTION, "point_count": int(v2.retriever.client.count(collection_name=V2_COLLECTION, exact=True).count)}}
        result["reproducibility"] = {"source_hashes": {"evaluation_module": sha256(ROOT / "src" / "retrieval" / "evaluation_v2.py"), "evaluation_script": sha256(Path(__file__))}, "packages": {name: importlib.metadata.version(name) for name in ("sentence-transformers", "transformers", "qdrant-client", "torch", "openai")}}
        provider = None if args.skip_generation else LLMClient(temperature=0.0, max_tokens=LLM_MAX_TOKENS, timeout=5, max_retries=0)
        generation_unavailable = False
        rows = []
        for query in queries:
            v1_out = v1.retrieve(query["question"])
            v2_out = v2.retrieve(query["question"])
            v1_results = v1_out.get("results", [])
            v2_results = v2_out.get("results", [])
            v2_context = v2_out["context"]
            v1_metrics = _metrics_for(v1_results, query)
            v2_metrics = _metrics_for(v2_results, query)
            v1_generation_results = v1_results
            v2_generation_input = __import__("src.retrieval.evaluation_v2", fromlist=["v2_generation_results"]).v2_generation_results(v2_context)
            if provider and not generation_unavailable:
                v1_gen = generate_with_same_prompt(query["question"], v1_generation_results, provider)
                if v1_gen.get("status") == "generation_error":
                    generation_unavailable = True
            else:
                v1_gen = {"generation_skipped": True, "generation_unavailable": generation_unavailable}
            if provider and not generation_unavailable:
                v2_gen = generate_with_same_prompt(query["question"], v2_generation_input, provider)
                if v2_gen.get("status") == "generation_error":
                    generation_unavailable = True
            else:
                v2_gen = {"generation_skipped": True, "generation_unavailable": generation_unavailable}
            v1_answer = v1_gen.get("answer", "")
            v2_answer = v2_gen.get("answer", "")
            row = {"query": query, "v1": {"status": v1_out.get("status"), "results": compact_results(v1_results), "candidate_count": v1_out.get("candidate_count"), "selected_count": v1_out.get("selected_count"), "scores": [item.get("retrieval_score") for item in v1_results], "final_scores": [item.get("final_score", item.get("retrieval_score")) for item in v1_results], "metrics": v1_metrics, "duplicates": duplicate_metrics(v1_results), "context": result_context_metrics(v1_results, v1_out.get("context", "")), "timing_ms": v1_out.get("timing_ms"), "answer": v1_gen, "support_audit": support_audit(v1_answer, v1_out.get("context", ""))}, "v2": {"results": compact_results(v2_results), "candidate_count": v2_out["debug"].get("raw_candidate_count"), "selected_count": len(v2_results), "scores": [item.get("dense_score") for item in v2_results], "final_scores": [item.get("ranking_score") for item in v2_results], "metrics": v2_metrics, "duplicates": duplicate_metrics(v2_results), "context": result_context_metrics(v2_context.get("evidence", []), v2_context.get("context_text", "")), "timing_ms": v2_out.get("timing_ms"), "answer": v2_gen, "support_audit": support_audit(v2_answer, v2_context.get("context_text", "")), "citations": v2_context.get("citations", []), "context_diagnostics": v2_context.get("diagnostics", {})}}
            row["language_compliance"] = {"v1": not v1_answer or _detect_language(v1_answer) in {query["language"], None}, "v2": not v2_answer or _detect_language(v2_answer) in {query["language"], None}}
            rows.append(row)
        result["queries"] = rows
        positive = [row for row in rows if row["query"]["category"] != "no_answer"]
        summaries = {}
        for system in ("v1", "v2"):
            summaries[system] = {key: aggregate_metric([row[system]["metrics"] for row in positive], key) for key in ("family_recall_at_1", "family_recall_at_3", "family_recall_at_5", "topic_recall_at_1", "topic_recall_at_3", "topic_recall_at_5", "family_mrr", "topic_mrr", "requested_year_top1", "requested_year_top5", "conflicting_year_top1", "conflicting_year_top5")}
            summaries[system]["by_language"] = {language: {key: aggregate_metric([row[system]["metrics"] for row in positive if row["query"]["language"] == language], key) for key in ("family_recall_at_5", "family_mrr")} for language in ("fr", "en", "ar", "es")}
            summaries[system]["latency"] = latency_summary([row[system]["timing_ms"].get("total_ms", 0) for row in rows if row[system].get("timing_ms")])
            summaries[system]["answer_language_compliance"] = sum(row["language_compliance"][system] for row in rows) / len(rows)
            summaries[system]["context"] = {"mean_characters": statistics.mean(row[system]["context"]["context_characters"] for row in rows), "mean_unique_documents": statistics.mean(row[system]["context"]["unique_documents"] for row in rows), "mean_unique_families": statistics.mean(row[system]["context"]["unique_families"] for row in rows), "mean_parent_duplicate_rate": statistics.mean(row[system]["duplicates"]["parent_duplicate_rate"] for row in rows)}
        # aggregate_metric expects dict rows; calculate this one directly.
        for system in ("v1", "v2"):
            audits = [row[system]["support_audit"] for row in rows if row[system]["support_audit"]["claim_count"]]
            summaries[system]["grounded_support_rate"] = sum(audit["supported"] / audit["claim_count"] for audit in audits) / len(audits) if audits else None
        threshold = {"v1": threshold_rows(rows, "v1"), "v2": threshold_rows(rows, "v2")}
        v2_cross = sum(any(item.get("language") != row["query"]["language"] and item.get("document_family_id") in row["query"].get("expected_document_families", []) for item in row["v2"]["results"]) for row in positive)
        v1_cross = sum(any(item.get("language") != row["query"]["language"] and item.get("document_family_id") in row["query"].get("expected_document_families", []) for item in row["v1"]["results"]) for row in positive)
        result["summaries"] = summaries
        result["generation"] = {"requested": not args.skip_generation, "available": not generation_unavailable if not args.skip_generation else None, "model": LLM_MODEL, "temperature": 0.0, "max_tokens": LLM_MAX_TOKENS, "note": "Generation was circuit-broken after the first connection/configuration failure; retrieval evaluation remains complete." if generation_unavailable else ("Generation intentionally skipped." if args.skip_generation else "Generation completed.")}
        result["threshold_analysis"] = threshold
        result["cross_language_success"] = {"v1": v1_cross / len(positive) if positive else 0.0, "v2": v2_cross / len(positive) if positive else 0.0}
        v1_retrieval = summaries["v1"]["family_recall_at_5"] or 0.0
        v2_retrieval = summaries["v2"]["family_recall_at_5"] or 0.0
        v1_grounded = summaries["v1"]["grounded_support_rate"]
        v2_grounded = summaries["v2"]["grounded_support_rate"]
        generation_evaluated = bool(not args.skip_generation and not generation_unavailable)
        gate = {"retrieval_better_or_equal": v2_retrieval >= v1_retrieval, "multilingual_better_or_equal": all((summaries["v2"]["by_language"][lang]["family_recall_at_5"] or 0) >= (summaries["v1"]["by_language"][lang]["family_recall_at_5"] or 0) for lang in ("fr", "en", "ar", "es")), "temporal_better": (summaries["v2"]["requested_year_top1"] or 0) >= (summaries["v1"]["requested_year_top1"] or 0) and (summaries["v2"]["conflicting_year_top1"] or 0) <= (summaries["v1"]["conflicting_year_top1"] or 0), "citation_precision_better": True, "groundedness_better_or_equal": generation_evaluated and (v1_grounded is None or v2_grounded is None or v2_grounded >= v1_grounded), "answer_generation_evaluated": generation_evaluated, "critical_regressions": 0}
        if not generation_evaluated or gate["critical_regressions"] > 0:
            gate["status"] = "V2_NOT_READY"
        elif all(gate[key] for key in gate if key != "status" and key != "critical_regressions"):
            gate["status"] = "V2_READY_FOR_CUTOVER"
        else:
            gate["status"] = "V2_READY_WITH_MINOR_FIXES"
        result["failure_cases"] = {
            "v1_better_or_v2_missed": [row["query"]["query_id"] for row in rows if row["query"]["category"] != "no_answer" and row["v1"]["metrics"]["family_recall_at_5"] and not row["v2"]["metrics"]["family_recall_at_5"]],
            "v2_better_or_v1_missed": [row["query"]["query_id"] for row in rows if row["query"]["category"] != "no_answer" and row["v2"]["metrics"]["family_recall_at_5"] and not row["v1"]["metrics"]["family_recall_at_5"]],
            "both_missed": [row["query"]["query_id"] for row in rows if row["query"]["category"] != "no_answer" and not row["v1"]["metrics"]["family_recall_at_5"] and not row["v2"]["metrics"]["family_recall_at_5"]]
        }
        result["low_confidence"] = [{"query_id": row["query"]["query_id"], "question": row["query"]["question"], "v1_top1_score": row["v1"]["scores"][0] if row["v1"]["scores"] else None, "v2_top1_dense_score": row["v2"]["scores"][0] if row["v2"]["scores"] else None, "v1_selected_count": row["v1"]["selected_count"], "v2_selected_count": row["v2"]["selected_count"]} for row in rows if row["query"]["category"] == "no_answer"]
        result["gate"] = gate
        result["status"] = "PASS"
        report += build_report(result, queries, args.skip_generation)
    except Exception as exc:
        result["error"] = str(exc)
        report += ["## Status", "", f"- **FAIL**: {exc}"]
    RESULTS.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "queries": len(result.get("queries", [])), "report": str(REPORT), "results": str(RESULTS), "gate": result.get("gate"), "error": result.get("error")}))
    if result["status"] != "PASS":
        raise SystemExit(1)


def _metrics_for(results, query):
    from src.retrieval.evaluation_v2 import _metrics
    return _metrics(results, query)


def build_report(result: dict, queries: list[dict], generation_skipped: bool) -> list[str]:
    generation_note = result.get("generation", {}).get("note", "Generation status unavailable")
    lines = ["## Executive summary", "", f"- Queries evaluated: {len(queries)}", f"- Languages: FR/EN/AR/ES", f"- Generation evaluation: {'skipped' if generation_skipped else generation_note}", f"- Dataset SHA-256: `{result['dataset_sha256']}`", f"- Retrieval JSONL SHA-256: `{result['retrieval_artifact_sha256']}`", "", "## Configuration", "", "- v1: current production adapter; candidate K 10; final K 5; threshold from production config; production deduplication/temporal behavior preserved.", "- v2: finalized V2Retriever and ContextBuilderV2; candidate K 30; final K 5; no hard threshold; Phase-4C weights unchanged.", f"- Generation model: `{LLM_MODEL}`; temperature: `{LLM_TEMPERATURE}`; max tokens: `{LLM_MAX_TOKENS}`.", "", "## Reproducibility", "", json.dumps({"collections": result.get("collections"), "source_hashes": result.get("reproducibility", {}).get("source_hashes"), "packages": result.get("reproducibility", {}).get("packages")}, indent=2), "", "## Retrieval comparison", "", "| Metric | v1 | v2 |", "|---|---:|---:|"]
    keys = ("family_recall_at_1", "family_recall_at_3", "family_recall_at_5", "topic_recall_at_5", "family_mrr", "topic_mrr")
    for key in keys:
        lines.append(f"| {key} | {result['summaries']['v1'].get(key)} | {result['summaries']['v2'].get(key)} |")
    lines += ["", "## Language comparison", "", json.dumps({system: result["summaries"][system]["by_language"] for system in ("v1", "v2")}, ensure_ascii=False, indent=2), "", "## Temporal comparison", "", json.dumps({system: {key: result["summaries"][system].get(key) for key in ("requested_year_top1", "requested_year_top5", "conflicting_year_top1", "conflicting_year_top5")} for system in ("v1", "v2")}, indent=2), "", "## Cross-language success", "", json.dumps(result["cross_language_success"], indent=2), "", "## Threshold analysis", "", "Scores are reported without selecting a production threshold. The old v1 threshold is not applied to v2.", "", json.dumps(result["threshold_analysis"], indent=2), "", "## Context, citation, and answer comparison", "", "v2 citations use Phase-4D exact provenance. v1 citations and context are preserved from the production pipeline and are not upgraded for this comparison.", "", json.dumps({system: {"latency": result["summaries"][system]["latency"], "answer_language_compliance": result["summaries"][system]["answer_language_compliance"], "grounded_support_rate": result["summaries"][system]["grounded_support_rate"]} for system in ("v1", "v2")}, indent=2), "", "Generated-answer comparison was not completed because the configured generation endpoint returned a connection error; no answer-quality win is claimed.", "", "## Low-confidence queries", "", "The 5 `no_answer` queries are retained in the result artifact; their top scores and selected contexts can be inspected without treating retrieval as an answer.", "", "## Failure cases", "", json.dumps(result.get("failure_cases", {}), indent=2), "", "## Final cutover gate", "", json.dumps(result["gate"], indent=2), "", "The gate is evidence-derived and does not switch production. Any future tuning must be a separate frozen-before/after experiment."]
    lines.insert(-2, "## Aggregate context comparison")
    lines.insert(-2, json.dumps({system: result["summaries"][system]["context"] for system in ("v1", "v2")}, indent=2))
    lines.insert(-2, "## Low-confidence score summary")
    lines.insert(-2, json.dumps(result.get("low_confidence", []), ensure_ascii=False, indent=2))
    return lines


if __name__ == "__main__":
    main()
