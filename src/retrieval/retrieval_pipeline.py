"""Task 4 retrieval enhancement pipeline, without answer generation."""

from typing import Any

from src.retrieval.context_selector import format_context, select_context
from src.retrieval.deduplicator import deduplicate
from src.retrieval.reranker import Reranker
from src.retrieval.temporal import (extract_document_years, extract_exact_tokens,
                                     extract_years, exact_match_adjustment,
                                     temporal_score)
from src.utils.config import (ENABLE_RERANKER, E5_RELEVANCE_THRESHOLD,
                              EXACT_MATCH_BONUS, MAX_CHUNKS_PER_DOCUMENT,
                              MAX_CONTEXT_CHARACTERS, RERANKER_BATCH_SIZE,
                              RERANKER_MODEL, TEMPORAL_BONUS, TEMPORAL_PENALTY)


class RetrievalPipeline:
    def __init__(self, semantic_retriever, threshold: float = E5_RELEVANCE_THRESHOLD,
                 reranker: Reranker | None = None, enable_reranker: bool = ENABLE_RERANKER,
                 max_per_document: int = MAX_CHUNKS_PER_DOCUMENT,
                 max_context_characters: int = MAX_CONTEXT_CHARACTERS,
                 enable_temporal: bool = True, enable_exact: bool = True,
                 enable_dedup: bool = True):
        self.semantic_retriever = semantic_retriever
        self.threshold = threshold
        self.enable_reranker = enable_reranker
        self.reranker = reranker
        self.max_per_document = max_per_document
        self.max_context_characters = max_context_characters
        self.enable_temporal, self.enable_exact, self.enable_dedup = enable_temporal, enable_exact, enable_dedup

    def _get_reranker(self):
        if self.reranker is None:
            from src.retrieval.reranker import MultilingualCrossEncoderReranker
            self.reranker = MultilingualCrossEncoderReranker(RERANKER_MODEL, RERANKER_BATCH_SIZE)
        return self.reranker

    @staticmethod
    def _diagnostic_item(item: dict[str, Any]) -> dict[str, Any]:
        diagnostic = {key: value for key, value in item.items() if key != "text"}
        diagnostic["text_preview"] = " ".join((item.get("text") or "").split())[:240]
        return diagnostic

    def retrieve(self, query: str, candidate_k: int = 10, final_k: int = 5,
                 diagnostics: bool = False) -> dict[str, Any]:
        raw = self.semantic_retriever.search(query, candidate_k)
        candidates, audited = [], []
        query_years, query_tokens = extract_years(query), extract_exact_tokens(query)
        top1_score = float(raw[0].get("score", 0.0)) if raw else None
        query_gate_passed = bool(raw) and top1_score >= self.threshold
        for result in raw:
            item = dict(result)
            item["retrieval_score"] = float(result.get("score", 0.0))
            item.pop("score", None)
            item["query_gate_passed"] = query_gate_passed
            item["query_years"] = sorted(query_years)
            item["document_years"] = sorted(extract_document_years(item.get("filename"), item.get("document_id")))
            item["mentioned_years"] = sorted(extract_years(item.get("text", "")))
            item["temporal_adjustment"], item["temporal_reason"] = temporal_score(
                query_years, set(item["document_years"]), set(item["mentioned_years"]), TEMPORAL_BONUS, TEMPORAL_PENALTY) if self.enable_temporal else (0.0, "no_temporal_signal")
            item["exact_match_adjustment"] = exact_match_adjustment(query_tokens, item.get("text", ""), EXACT_MATCH_BONUS) if self.enable_exact else 0.0
            audited.append(item)
            if query_gate_passed:
                candidates.append(item)
        if not candidates:
            for item in audited:
                item["selected"] = False
                item["exclusion_reason"] = "below_query_gate"
            result = {"query": query, "status": "insufficient_evidence", "top1_score": top1_score,
                      "query_threshold": self.threshold, "query_gate_passed": False, "candidate_count": len(raw),
                      "accepted_count": 0, "selected_count": 0, "results": [], "candidate_results": [], "context": ""}
            if diagnostics:
                result["diagnostics"] = [self._diagnostic_item(item) for item in audited]
            return result
        if self.enable_reranker:
            candidates = self._get_reranker().rerank(query, candidates)
        else:
            for item in candidates:
                item["rerank_score"] = None
        for item in candidates:
            base = item["rerank_score"] if item["rerank_score"] is not None else item["retrieval_score"]
            item["final_score"] = float(base + item["temporal_adjustment"] + item["exact_match_adjustment"])
        candidates.sort(key=lambda item: item["final_score"], reverse=True)
        unique = deduplicate(candidates, self.max_per_document) if self.enable_dedup else candidates
        selected, limited = select_context(unique, final_k, self.max_context_characters)
        selected_ids = {item.get("chunk_id") for item in selected}
        for item in candidates:
            item["selected"] = item.get("chunk_id") in selected_ids
            if not item["selected"] and "exclusion_reason" not in item:
                item["exclusion_reason"] = "context_budget" if limited else "final_k_limit"
        for item in audited:
            if not item["query_gate_passed"]:
                item["selected"] = False
                item["exclusion_reason"] = "below_query_gate"
        result = {"query": query, "status": "ok", "top1_score": top1_score,
                  "query_threshold": self.threshold, "query_gate_passed": True, "candidate_count": len(raw),
                  "accepted_count": len(candidates), "selected_count": len(selected),
                  "context_limited": limited, "results": selected, "candidate_results": candidates,
                  "context": format_context(selected)}
        if diagnostics:
            result["diagnostics"] = [self._diagnostic_item(item) for item in audited]
        return result
