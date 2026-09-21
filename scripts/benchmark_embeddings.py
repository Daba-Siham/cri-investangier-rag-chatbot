"""Benchmark existing embedding indexes against validated retrieval questions."""

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.embeddings.factory import create_embedding_provider
from src.evaluation.metrics import (is_cross_language_expected_source,
                                    is_expected_source, summarize_metrics)
from src.evaluation.thresholds import calibrate_threshold, threshold_candidates
from src.retrieval.semantic_retriever import SemanticRetriever
from src.utils.config import (BGE_M3_COLLECTION, E5_COLLECTION,
                               EMBEDDING_BATCH_SIZE, QDRANT_API_KEY, QDRANT_URL)
from src.vectorstore.qdrant_store import QdrantStore


def _percentile(values, percentile):
    if not values:
        return 0.0
    ordered = sorted(values)
    position = (len(ordered) - 1) * percentile
    lower, upper = int(position), min(int(position) + 1, len(ordered) - 1)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def _subset_metrics(rows, predicate):
    subset = [row for row in rows if predicate(row["question"])]
    return {"question_count": len(subset), **summarize_metrics(subset)}


def _cross_metrics(rows):
    values = {}
    for k in (1, 3, 5, 10):
        values[f"cross_lingual_recall_at_{k}"] = (
            sum(any(is_cross_language_expected_source(result, row["expected_sources"],
                                                       row["question"].get("query_language"))
                    for result in row["results"][:k]) for row in rows) / len(rows) if rows else 0.0)
    values["cross_lingual_mrr"] = (sum(next((1.0 / rank for rank, result in enumerate(row["results"], 1)
        if is_cross_language_expected_source(result, row["expected_sources"], row["question"].get("query_language"))), 0.0)
        for row in rows) / len(rows) if rows else 0.0)
    values["question_count"] = len(rows)
    return values


def _diagnostic(row):
    question, results = row["question"], row["results"]
    relevant = [r["rank"] for r in results if is_expected_source(r, row["expected_sources"])]
    cross = [r["rank"] for r in results if is_cross_language_expected_source(
        r, row["expected_sources"], question.get("query_language"))]
    return {"id": question.get("id"), "question": question.get("question"),
            "query_language": question.get("query_language"), "answerable": question.get("answerable", True),
            "cross_lingual": question.get("cross_lingual", False), "expected_sources": row["expected_sources"],
            "top_results": [{"rank": r["rank"], "score": r["score"], "document_id": r.get("document_id"),
                             "page": r.get("page"), "language": r.get("language"),
                             "preview": (r.get("text") or "")[:160]} for r in results],
            "top1_score": results[0].get("score") if results else None,
            "first_relevant_rank": min(relevant) if relevant else None,
            "first_cross_language_relevant_rank": min(cross) if cross else None,
            "recall_hits": {f"recall_at_{k}": any(rank <= k for rank in relevant) for k in (1, 3, 5, 10)}}


def benchmark_model(model, questions, top_k=10):
    collection = BGE_M3_COLLECTION if model == "bge-m3" else E5_COLLECTION
    provider = create_embedding_provider(model, EMBEDDING_BATCH_SIZE)
    retriever = SemanticRetriever(provider, QdrantStore(QDRANT_URL, QDRANT_API_KEY), collection)
    retriever.search(questions[0]["question"], top_k=1)  # warm-up, outside measured loop
    rows, total, embedding, search = [], [], [], []
    for question in questions:
        started = time.perf_counter()
        results, timing = retriever.search_with_timing(question["question"], top_k)
        total.append((time.perf_counter() - started) * 1000)
        embedding.append(timing["embedding_ms"]); search.append(timing["search_ms"])
        expected = list(question.get("expected_sources", []))
        expected.extend(question.get("expected_chunk_ids", []))
        rows.append({"question": question, "results": results, "expected_sources": expected, "timing": timing})
    answerable = [r for r in rows if r["question"].get("answerable", True)]
    cross_rows = [r for r in answerable if r["question"].get("cross_lingual", False)]
    languages = sorted({q.get("query_language", "other") for q in questions})
    scores = [r["results"][0]["score"] for r in rows if r["results"]]
    candidates = threshold_candidates(rows)
    calibration = calibrate_threshold(rows, candidates)
    best = max(calibration, key=lambda x: (x["balanced_accuracy"], x["f1"]), default=None)
    latency = {name: {"average": statistics.mean(values), "p50": _percentile(values, .50), "p95": _percentile(values, .95)}
               for name, values in (("total", total), ("query_embedding", embedding), ("qdrant_search", search))}
    return {"model": model, "collection": collection, "number_of_questions": len(questions),
            "answerable_question_count": len(answerable), "unanswerable_question_count": len(rows) - len(answerable),
            **summarize_metrics(answerable),
            "per_language": {lang: _subset_metrics(answerable, lambda q, lang=lang: q.get("query_language", "other") == lang) for lang in languages},
            "same_language": _subset_metrics(answerable, lambda q: not q.get("cross_lingual", False)),
            "cross_lingual": _cross_metrics(cross_rows),
            "observed_top1_score_range": {"min": min(scores) if scores else None, "max": max(scores) if scores else None},
            "latency_ms": latency, "threshold_candidates": candidates, "threshold_evaluation": calibration,
            "recommended_threshold": best, "diagnostics": [_diagnostic(row) for row in rows]}


def _selection(results):
    bge, e5 = results
    rationale = ["Corrected evaluation is preliminary because it uses only 20 answerable and 9 unanswerable questions.",
                 f"Arabic Recall@5: BGE-M3={bge['per_language'].get('ar', {}).get('recall_at_5')}; E5={e5['per_language'].get('ar', {}).get('recall_at_5')}.",
                 f"True cross-lingual Recall@5: BGE-M3={bge['cross_lingual']['cross_lingual_recall_at_5']:.4f}; E5={e5['cross_lingual']['cross_lingual_recall_at_5']:.4f}."]
    if (bge["recall_at_5"], bge["recall_at_10"]) > (e5["recall_at_5"], e5["recall_at_10"]):
        return "bge-m3", rationale
    if (e5["recall_at_5"], e5["recall_at_10"]) > (bge["recall_at_5"], bge["recall_at_10"]):
        return "multilingual-e5-base", rationale
    rationale.append("Priority Recall@5/Recall@10 are tied; no automatic winner is justified.")
    return None, rationale


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=("bge-m3", "multilingual-e5-base", "both"), default="both")
    parser.add_argument("--questions", type=Path, default=PROJECT_ROOT / "evaluation" / "retrieval_questions.json")
    parser.add_argument("--top-k", type=int, default=10)
    args = parser.parse_args()
    questions = json.loads(args.questions.read_text(encoding="utf-8"))
    models = ("bge-m3", "multilingual-e5-base") if args.model == "both" else (args.model,)
    results = [benchmark_model(model, questions, args.top_k) for model in models]
    result_dir = PROJECT_ROOT / "evaluation" / "results"; result_dir.mkdir(parents=True, exist_ok=True)
    for result in results:
        diagnostics = result.pop("diagnostics")
        stem = "bge_m3" if result["model"] == "bge-m3" else "multilingual_e5_base"
        (result_dir / f"{stem}_results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        (result_dir / f"{stem}_diagnostics.json").write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2), encoding="utf-8")
        if result["model"] == "bge-m3":
            print("Arabic diagnostics (BGE-M3):", json.dumps([
                {"id": d["id"], "first_relevant_rank": d["first_relevant_rank"], "recall_hits": d["recall_hits"]}
                for d in diagnostics if d["query_language"] == "ar" and d["answerable"]], ensure_ascii=False))
    recommended, rationale = _selection(results) if len(results) == 2 else (None, ["Comparison requires both models."])
    comparison = {"models": results, "recommended_model": recommended, "selection_rationale": rationale,
                  "selection": "Corrected benchmark comparison; recommendation is preliminary."}
    (result_dir / "comparison.json").write_text(json.dumps(comparison, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(comparison, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
