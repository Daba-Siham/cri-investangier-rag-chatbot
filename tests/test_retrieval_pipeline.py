from src.retrieval.deduplicator import deduplicate
from src.retrieval.retrieval_pipeline import RetrievalPipeline
from src.retrieval.temporal import (extract_document_years, extract_exact_tokens,
                                     extract_years, exact_match_adjustment,
                                     temporal_adjustment, temporal_score)


class FakeRetriever:
    def __init__(self, results):
        self.results = results

    def search(self, query, top_k):
        return self.results[:top_k]


class FakeReranker:
    def rerank(self, query, candidates):
        # Deliberately reverse the semantic order.
        return [{**candidate, "rerank_score": 1.0 - candidate["retrieval_score"]}
                for candidate in reversed(candidates)]


def candidate(chunk, score, document="doc", page=1, text="evidence 2023"):
    return {"rank": chunk, "score": score, "chunk_id": f"c{chunk}", "text": text,
            "document_id": document, "filename": "doc.pdf", "page": page, "language": "fr"}


def test_threshold_and_insufficient_evidence():
    pipeline = RetrievalPipeline(FakeRetriever([candidate(1, .8), candidate(2, .7)]), threshold=.75,
                                 enable_reranker=False)
    result = pipeline.retrieve("question", 2, 1)
    assert result["accepted_count"] == 2 and result["results"][0]["retrieval_score"] == .8
    empty = RetrievalPipeline(FakeRetriever([candidate(1, .7)]), threshold=.9, enable_reranker=False).retrieve("q")
    assert empty["status"] == "insufficient_evidence" and empty["results"] == []


def test_query_gate_keeps_lower_scoring_top10_candidates():
    results = [candidate(1, .9), candidate(2, .7), candidate(3, .6)]
    output = RetrievalPipeline(FakeRetriever(results), threshold=.8, enable_reranker=False).retrieve("q", 3, 3, True)
    assert output["query_gate_passed"] is True
    assert output["accepted_count"] == 3
    assert len(output["candidate_results"]) == 3
    assert all(item["query_gate_passed"] for item in output["diagnostics"])


def test_document_year_takes_priority_over_mentioned_comparison_year():
    assert extract_document_years("Chiffres clés CRUI 2024_Français.pdf", "doc") == {2024}
    adjustment, reason = temporal_score({2024}, {2024}, {2023}, .03, .03)
    assert adjustment == .03 and reason == "document_year_match"
    adjustment, reason = temporal_score({2024}, {2025}, {2024}, .03, .03)
    assert adjustment == -.03 and reason == "document_year_conflict"


def test_year_is_not_in_exact_bonus_when_temporal_scoring_is_separate():
    tokens = extract_exact_tokens("CRUI 2024 54%")
    assert "2024" not in tokens
    assert "crui" in tokens and "54%" in tokens


def test_reranking_can_change_order_and_disabled_path_preserves_score():
    retriever = FakeRetriever([candidate(1, .9), candidate(2, .85)])
    changed = RetrievalPipeline(retriever, threshold=.8, reranker=FakeReranker(), enable_reranker=True).retrieve("q", 2, 2)
    assert changed["results"][0]["chunk_id"] == "c2"
    assert changed["results"][0]["retrieval_score"] == .85
    assert changed["results"][0]["rerank_score"] is not None
    disabled = RetrievalPipeline(retriever, threshold=.8, enable_reranker=False).retrieve("q", 2, 2)
    assert disabled["results"][0]["rerank_score"] is None


def test_temporal_and_exact_features():
    assert extract_years("CRUI en 2023") == {2023}
    assert temporal_adjustment({2023}, {2023}, .03, .03) > 0
    assert temporal_adjustment({2023}, {2025}, .03, .03) < 0
    tokens = extract_exact_tokens("PIAFE CRUI 54% 2023")
    assert {"piafe", "crui", "54%"} <= tokens
    assert exact_match_adjustment(tokens, "CRUI PIAFE 2023 54%", .01) > 0


def test_deduplication_diversity_and_equivalent_citations():
    items = [candidate(1, .9, page=1, text="same"), candidate(2, .8, page=1, text="same"),
             candidate(3, .7, page=2, text="other"), candidate(4, .6, document="other", page=1, text="third")]
    selected = deduplicate(items, max_per_document=2)
    assert [item["chunk_id"] for item in selected] == ["c1", "c3", "c4"]
    assert selected[0]["equivalent_sources"][0]["page"] == 1


def test_context_budget_unicode_and_citations():
    results = [candidate(1, .9, text="العربية Réponse ¿Qué?"), candidate(2, .8, text="second")]
    result = RetrievalPipeline(FakeRetriever(results), threshold=.5, enable_reranker=False,
                               max_context_characters=len(results[0]["text"]) + 1).retrieve("q", 2, 2)
    assert result["selected_count"] == 1
    assert "العربية" in result["context"]
    assert {"document_id", "filename", "page", "language", "chunk_id"} <= set(result["results"][0])
