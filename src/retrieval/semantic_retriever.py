"""Semantic dense retrieval over a selected Qdrant collection."""

import statistics
import time
from typing import Any

from src.embeddings.base import EmbeddingProvider
from src.vectorstore.qdrant_store import QdrantStore


class SemanticRetriever:
    def __init__(self, provider: EmbeddingProvider, store: QdrantStore,
                 collection_name: str):
        self.provider = provider
        self.store = store
        self.collection_name = collection_name

    def search(self, query: str, top_k: int = 8, score_threshold: float | None = None,
               query_filter: Any | None = None) -> list[dict[str, Any]]:
        if top_k <= 0:
            return []
        started = time.perf_counter()
        vector = self.provider.embed_query(query)
        embedding_ms = (time.perf_counter() - started) * 1000
        started = time.perf_counter()
        points = self.store.search(self.collection_name, vector, top_k, score_threshold, query_filter)
        search_ms = (time.perf_counter() - started) * 1000
        results = []
        for rank, point in enumerate(points, start=1):
            payload = getattr(point, "payload", None) or point.get("payload", {})
            score = getattr(point, "score", None)
            if score is None and isinstance(point, dict):
                score = point.get("score", 0.0)
            results.append({"rank": rank, "score": float(score or 0.0),
                "chunk_id": payload.get("chunk_id"), "text": payload.get("text", ""),
                "document_id": payload.get("document_id"), "filename": payload.get("filename"),
                "page": payload.get("page"), "language": payload.get("language")})
        self.last_timing = {"embedding_ms": embedding_ms, "search_ms": search_ms,
                            "total_ms": embedding_ms + search_ms}
        return results

    def search_with_timing(self, *args: Any, **kwargs: Any) -> tuple[list[dict[str, Any]], dict[str, float]]:
        results = self.search(*args, **kwargs)
        return results, self.last_timing
