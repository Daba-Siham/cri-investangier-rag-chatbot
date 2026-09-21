"""Read-only comparative evaluation adapters for production v1 and RAG v2."""
from __future__ import annotations

import json
import statistics
import time
from pathlib import Path
from typing import Any

from src.generation.answer_generator import AnswerGenerator
from src.generation.llm_client import LLMClient
from src.retrieval.context_builder_v2 import ContextBuilderV2, ProvenanceStore, page_label
from src.retrieval.retriever_v2 import V2Retriever, _model_source
from src.retrieval.retrieval_pipeline import RetrievalPipeline
from src.retrieval.semantic_retriever import SemanticRetriever
from src.utils.config import (E5_COLLECTION, E5_RELEVANCE_THRESHOLD, ENABLE_RERANKER,
                              QDRANT_API_KEY, QDRANT_URL, RETRIEVAL_CANDIDATE_K,
                              RETRIEVAL_FINAL_K)
from src.embeddings.factory import create_embedding_provider
from src.vectorstore.qdrant_store import QdrantStore

ROOT = Path(__file__).resolve().parents[2]
V2_COLLECTION = "cri_chunks_multilingual_e5_v2"


def load_family_map() -> dict[str, str]:
    output = {}
    for path in sorted((ROOT / "data" / "semantic_json").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema_version") == "2.2":
            output[data.get("document_id")] = data.get("document_family_id")
    return output


def _families(results: list[dict[str, Any]]) -> list[str]:
    return [item.get("document_family_id") for item in results if item.get("document_family_id")]


def _family_hit(result: dict[str, Any], expected: list[str]) -> bool:
    return bool(expected) and result.get("document_family_id") in expected


def _topic_hit(result: dict[str, Any], expected: list[str]) -> bool:
    topics = set(result.get("semantic_tags") or []) | {result.get("topic_id")}
    return bool(expected) and bool(topics.intersection(expected))


def _metrics(results: list[dict[str, Any]], query: dict[str, Any]) -> dict[str, Any]:
    families = query.get("expected_document_families", [])
    topics = query.get("expected_topics", [])
    family_ranks = [rank for rank, item in enumerate(results, 1) if _family_hit(item, families)]
    topic_ranks = [rank for rank, item in enumerate(results, 1) if _topic_hit(item, topics)]
    answerable = query.get("category") != "no_answer"
    topic_available = any(item.get("topic_id") or item.get("semantic_tags") for item in results)
    return {
        "answerable": answerable,
        "family_recall_at_1": bool(family_ranks and family_ranks[0] <= 1),
        "family_recall_at_3": bool(family_ranks and family_ranks[0] <= 3),
        "family_recall_at_5": bool(family_ranks and family_ranks[0] <= 5),
        "topic_recall_at_1": bool(topic_ranks and topic_ranks[0] <= 1) if topic_available else None,
        "topic_recall_at_3": bool(topic_ranks and topic_ranks[0] <= 3) if topic_available else None,
        "topic_recall_at_5": bool(topic_ranks and topic_ranks[0] <= 5) if topic_available else None,
        "family_mrr": 1.0 / family_ranks[0] if family_ranks else 0.0,
        "topic_mrr": 1.0 / topic_ranks[0] if topic_ranks else (0.0 if topic_available else None),
        "family_rank": family_ranks[0] if family_ranks else None,
        "topic_rank": topic_ranks[0] if topic_ranks else None,
        "explicit_year": query.get("explicit_year"),
        "requested_year_top1": _year_supported(results[0], query.get("explicit_year")) if query.get("explicit_year") and results else False,
        "requested_year_top5": any(_year_supported(item, query.get("explicit_year")) for item in results[:5]) if query.get("explicit_year") else None,
        "conflicting_year_top1": _year_conflict(results[0], query.get("explicit_year")) if query.get("explicit_year") and results else False,
        "conflicting_year_top5": any(_year_conflict(item, query.get("explicit_year")) for item in results[:5]) if query.get("explicit_year") else None,
    }


def _year_supported(item: dict[str, Any], year: int | None) -> bool:
    if not year:
        return False
    return year in {item.get("primary_year"), item.get("reference_period_year"), *(item.get("years_mentioned") or [])}


def _year_conflict(item: dict[str, Any], year: int | None) -> bool:
    if not year:
        return False
    primary = {value for value in (item.get("primary_year"), item.get("reference_period_year")) if isinstance(value, int)}
    years = item.get("years_mentioned") or []
    return bool(primary and year not in primary) or bool(not primary and years and year not in years)


def _v1_result(item: dict[str, Any], family_map: dict[str, str]) -> dict[str, Any]:
    output = dict(item)
    output["document_family_id"] = family_map.get(item.get("document_id"))
    output["page_start"] = item.get("page")
    output["page_end"] = item.get("page")
    output["source_pages"] = [item.get("page")] if item.get("page") is not None else []
    document_years = item.get("document_years") or []
    output["primary_year"] = document_years[0] if len(document_years) == 1 else None
    output["reference_period_year"] = None
    output["years_mentioned"] = item.get("mentioned_years") or []
    output["dense_score"] = item.get("retrieval_score", item.get("score"))
    output["ranking_score"] = item.get("final_score", output["dense_score"])
    return output


class V1Adapter:
    """Read-only wrapper around the current production retrieval classes."""

    def __init__(self, family_map: dict[str, str]):
        # Use the already available exact E5 model snapshot when present. This
        # changes no v1 behavior; it only prevents a read-only benchmark from
        # attempting an unnecessary network download.
        from sentence_transformers import SentenceTransformer
        from src.embeddings.multilingual_e5 import MultilingualE5Provider
        provider = MultilingualE5Provider(model=SentenceTransformer(_model_source()))
        store = QdrantStore(QDRANT_URL, QDRANT_API_KEY)
        self.retriever = SemanticRetriever(provider, store, E5_COLLECTION)
        self.pipeline = RetrievalPipeline(self.retriever, E5_RELEVANCE_THRESHOLD,
                                          enable_reranker=ENABLE_RERANKER)
        self.family_map = family_map

    def retrieve(self, query: str) -> dict[str, Any]:
        started = time.perf_counter()
        output = self.pipeline.retrieve(query, RETRIEVAL_CANDIDATE_K, RETRIEVAL_FINAL_K, diagnostics=True)
        elapsed = (time.perf_counter() - started) * 1000
        final = [_v1_result(item, self.family_map) for item in output.get("results", [])]
        candidates = [_v1_result(item, self.family_map) for item in output.get("candidate_results", [])]
        output["results"] = final
        output["candidate_results"] = candidates
        output["timing_ms"] = {"total_ms": elapsed, **getattr(self.retriever, "last_timing", {})}
        return output


class V2Adapter:
    def __init__(self):
        self.retriever = V2Retriever(candidate_k=30, final_k=5, max_per_parent=1,
                                     max_per_family=None, family_repeat_penalty=0.002,
                                     language_bonus=0.005, semantic_bonus=0.004,
                                     temporal_bonus=0.012)
        self.provenance = ProvenanceStore()
        self.context_builder = ContextBuilderV2(self.provenance, max_evidence_units=6,
                                                max_context_characters=12000,
                                                expand_siblings=True)

    def retrieve(self, query: str) -> dict[str, Any]:
        started = time.perf_counter()
        retrieval = self.retriever.retrieve(query, debug=True)
        retrieval_ms = (time.perf_counter() - started) * 1000
        started = time.perf_counter()
        context = self.context_builder.build(retrieval, query=query,
                                             query_language=retrieval["debug"].get("query_language"))
        context_ms = (time.perf_counter() - started) * 1000
        retrieval["context"] = context
        retrieval["timing_ms"] = {"retrieval_ms": retrieval_ms, "context_ms": context_ms,
                                  "total_ms": retrieval_ms + context_ms}
        return retrieval


def v2_generation_results(context: dict[str, Any]) -> list[dict[str, Any]]:
    output = []
    for item in context.get("evidence", []):
        output.append({"chunk_id": item["retrieval_chunk_id"], "document_id": item["document_id"],
                       "filename": item["filename"], "page": page_label(item["source_pages"]),
                       "language": item["language"], "text": item["text"]})
    return output


def generate_with_same_prompt(question: str, results: list[dict[str, Any]], provider: Any) -> dict[str, Any]:
    if not results:
        return {"status": "insufficient_evidence", "answer": "", "citations": [], "generation_skipped": True}
    generator = AnswerGenerator(provider)
    started = time.perf_counter()
    try:
        output = generator.generate(question, results)
        output["generation_ms"] = (time.perf_counter() - started) * 1000
        output["generation_metadata"] = dict(generator.last_generation_metadata)
        return output
    except Exception as exc:
        return {"status": "generation_error", "answer": "", "citations": [],
                "error": str(exc)[:500], "generation_ms": (time.perf_counter() - started) * 1000,
                "generation_metadata": dict(generator.last_generation_metadata)}


def aggregate_metric(rows: list[dict[str, Any]], key: str) -> float | None:
    values = [row[key] for row in rows if row.get(key) is not None]
    return sum(values) / len(values) if values else None


def latency_summary(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"median_ms": None, "p95_ms": None}
    ordered = sorted(values)
    return {"median_ms": statistics.median(ordered), "p95_ms": ordered[min(len(ordered) - 1, max(0, int(len(ordered) * 0.95) - 1))]}
