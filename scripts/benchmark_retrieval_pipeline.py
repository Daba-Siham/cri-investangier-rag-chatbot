"""Compare baseline E5 retrieval with Task 4 retrieval-only variants."""

import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.embeddings.factory import create_embedding_provider
from src.evaluation.metrics import (is_cross_language_expected_source,
                                    is_expected_source, reciprocal_rank,
                                    recall_at_k, summarize_metrics)
from src.retrieval.retrieval_pipeline import RetrievalPipeline
from src.retrieval.semantic_retriever import SemanticRetriever
from src.utils.config import (E5_COLLECTION, E5_RELEVANCE_THRESHOLD,
                              EMBEDDING_BATCH_SIZE, QDRANT_API_KEY,
                              QDRANT_URL, RETRIEVAL_CANDIDATE_K,
                              RETRIEVAL_FINAL_K)
from src.vectorstore.qdrant_store import QdrantStore


class StaticRetriever:
    def __init__(self, results):
        self.results = results

    def search(self, query, top_k):
        return self.results[:top_k]


def _latency(values):
    values = sorted(values)
    position = (len(values) - 1) * .95
    low, high = int(position), min(int(position) + 1, len(values) - 1)
    return {"average": statistics.mean(values), "p50": values[int((len(values) - 1) * .5)],
            "p95": values[low] + (values[high] - values[low]) * (position - low)}


def _cross(rows):
    output = {}
    for k in (1, 3, 5, 10):
        result_key = "results" if "results" in rows[0] else "candidate_results" if rows else "results"
        output[f"recall_at_{k}"] = sum(any(is_cross_language_expected_source(
            result, row["expected_sources"], row["query_language"]) for result in row[result_key][:k])
            for row in rows) / len(rows) if rows else 0.0
    result_key = "results" if "results" in rows[0] else "candidate_results" if rows else "results"
    output["mrr"] = sum(next((1 / rank for rank, result in enumerate(row[result_key], 1)
        if is_cross_language_expected_source(result, row["expected_sources"], row["query_language"])), 0.0)
        for row in rows) / len(rows) if rows else 0.0
    return output


def _metrics(rows, final=False):
    metric_rows = [{"results": row["selected"] if final else row["candidate_results"],
                    "expected_sources": row["expected_sources"]} for row in rows]
    return summarize_metrics(metric_rows)


def _coverage(rows):
    return sum(any(is_expected_source(result, row["expected_sources"]) for result in row["selected"])
               for row in rows) / len(rows) if rows else 0.0


def _final_mrr(rows):
    return sum(reciprocal_rank(row["selected"], row["expected_sources"]) for row in rows) / len(rows) if rows else 0.0


def _per_language(rows):
    return {language: _metrics([row for row in rows if row["query_language"] == language])
            for language in sorted({row["query_language"] for row in rows})}


def _compact(result):
    item = {key: value for key, value in result.items() if key != "text"}
    item["text_preview"] = " ".join((result.get("text") or "").split())[:240]
    return item


def _run_variant(raw_rows, questions, name, *, temporal=True, exact=True, dedup=True,
                 threshold=E5_RELEVANCE_THRESHOLD, final_k=RETRIEVAL_FINAL_K):
    rows, processing_times, diagnostics = [], [], []
    for raw, question in zip(raw_rows, questions):
        pipeline = RetrievalPipeline(StaticRetriever(raw), threshold=threshold,
                                      enable_reranker=False, enable_temporal=temporal,
                                      enable_exact=exact, enable_dedup=dedup)
        started = time.perf_counter()
        output = pipeline.retrieve(question["question"], len(raw), final_k, diagnostics=True)
        processing_times.append((time.perf_counter() - started) * 1000)
        rows.append({"candidate_results": output.get("candidate_results", []),
                     "selected": output.get("results", []),
                     "expected_sources": question.get("expected_sources", []),
                     "query_language": question.get("query_language"),
                     "cross_lingual": question.get("cross_lingual", False)})
        diagnostics.append({"id": question["id"], "question": question["question"], "variant": name,
                            "output": output})
    answerable = [row for row, question in zip(rows, questions) if question.get("answerable", True)]
    cross = [row for row in answerable if row["cross_lingual"]]
    final_metrics = _metrics(answerable, final=True)
    return {"name": name, "candidate_metrics": _metrics(answerable),
            "final_context_metrics": {**final_metrics, "context_recall_at_final_k": _coverage(answerable),
                                       "final_context_mrr": _final_mrr(answerable)},
            "per_language_candidate": _per_language(answerable),
            "per_language_final_context": _per_language([dict(row, candidate_results=row["selected"]) for row in answerable]),
            "true_cross_lingual_candidate": _cross(cross),
            "latency_ms": {"pipeline_overhead": _latency(processing_times)}, "diagnostics": diagnostics}


def main():
    questions = json.loads((ROOT / "evaluation" / "retrieval_questions.json").read_text(encoding="utf-8"))
    provider = create_embedding_provider("multilingual-e5-base", EMBEDDING_BATCH_SIZE)
    retriever = SemanticRetriever(provider, QdrantStore(QDRANT_URL, QDRANT_API_KEY), E5_COLLECTION)
    retriever.search(questions[0]["question"], top_k=1)  # warm-up
    raw_rows, baseline_times = [], []
    for question in questions:
        started = time.perf_counter(); raw = retriever.search(question["question"], RETRIEVAL_CANDIDATE_K)
        baseline_times.append((time.perf_counter() - started) * 1000)
        raw_rows.append(raw)
    baseline_rows = [{"candidate_results": raw, "selected": raw[:RETRIEVAL_FINAL_K],
                      "expected_sources": q.get("expected_sources", []), "query_language": q.get("query_language"),
                      "cross_lingual": q.get("cross_lingual", False)} for raw, q in zip(raw_rows, questions)]
    answerable = [row for row, q in zip(baseline_rows, questions) if q.get("answerable", True)]
    cross_rows = [row for row in answerable if row["cross_lingual"]]
    baseline = {"candidate_metrics": _metrics(answerable), "final_context_metrics": {**_metrics(answerable, True),
                "context_recall_at_final_k": _coverage(answerable), "final_context_mrr": _final_mrr(answerable)},
                "per_language_candidate": _per_language(answerable), "true_cross_lingual_candidate": _cross(cross_rows),
                "per_language_final_context": _per_language([dict(row, candidate_results=row["selected"]) for row in answerable]),
                "latency_ms": {"retrieval": _latency(baseline_times)}}
    variants = [
        _run_variant(raw_rows, questions, "query_gate_only", temporal=False, exact=False, dedup=False),
        _run_variant(raw_rows, questions, "query_gate_temporal_exact", temporal=True, exact=True, dedup=False),
        _run_variant(raw_rows, questions, "corrected_task4", temporal=True, exact=True, dedup=True),
    ]
    result = {"model": "multilingual-e5-base", "collection": E5_COLLECTION,
              "candidate_k": RETRIEVAL_CANDIDATE_K, "final_k": RETRIEVAL_FINAL_K,
              "query_threshold": E5_RELEVANCE_THRESHOLD, "reranker_enabled": False,
              "baseline": baseline,
              "corrected_pipeline": variants[-1],
              "acceptance_assessment": "not_beneficial_yet: final context metrics must be checked separately from candidate metrics"}
    ablation = {"model": result["model"], "baseline": baseline, "variants": variants}
    outdir = ROOT / "evaluation" / "results"; outdir.mkdir(exist_ok=True, parents=True)
    (outdir / "retrieval_pipeline_results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (outdir / "retrieval_pipeline_ablation.json").write_text(json.dumps(ablation, ensure_ascii=False, indent=2), encoding="utf-8")
    diagnostics = {"baseline": [{"question": q["question"], "results": [_compact(item) for item in raw]} for q, raw in zip(questions, raw_rows)],
                   "variants": [{"name": variant["name"], "diagnostics": variant["diagnostics"]} for variant in variants]}
    (outdir / "retrieval_pipeline_diagnostics.json").write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "corrected_pipeline"} | {
        "corrected_pipeline": {key: value for key, value in variants[-1].items() if key != "diagnostics"}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
