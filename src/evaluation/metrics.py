"""Small retrieval metric functions used by the benchmark."""

from typing import Any


def _expected_sources(expected_sources: list[dict[str, Any]] | None) -> list[Any]:
    return list(expected_sources or [])


def is_expected_source(result: dict[str, Any], expected_sources: list[Any] | None) -> bool:
    """Match a retrieval by source identity, ignoring non-identity metadata.

    ``language`` is descriptive metadata and must not make a valid document/page
    pair fail. String entries are retained for compatibility with old
    chunk-id-only evaluation rows.
    """
    for expected in _expected_sources(expected_sources):
        if isinstance(expected, str):
            if result.get("chunk_id") == expected:
                return True
            continue
        if not isinstance(expected, dict):
            continue
        expected_chunk_ids = expected.get("expected_chunk_ids")
        if expected_chunk_ids and result.get("chunk_id") in expected_chunk_ids:
            return True
        if (result.get("document_id") == expected.get("document_id") and
                result.get("page") == expected.get("page")):
            return True
    return False


def is_cross_language_expected_source(
    result: dict[str, Any], expected_sources: list[Any] | None, query_language: str | None
) -> bool:
    """Return true only for a valid source retrieved in another language."""
    return (is_expected_source(result, expected_sources) and
            bool(result.get("language")) and result.get("language") != query_language)


def recall_at_k(results: list[dict[str, Any]], expected_sources: list[Any], k: int) -> float:
    return float(any(is_expected_source(result, expected_sources) for result in results[:k]))


def reciprocal_rank(results: list[dict[str, Any]], expected_sources: list[Any]) -> float:
    for rank, result in enumerate(results, start=1):
        if is_expected_source(result, expected_sources):
            return 1.0 / rank
    return 0.0


def summarize_metrics(rows: list[dict[str, Any]], ks: tuple[int, ...] = (1, 3, 5, 10)) -> dict[str, float]:
    if not rows:
        return {f"recall_at_{k}": 0.0 for k in ks} | {"mrr": 0.0}
    return {f"recall_at_{k}": sum(recall_at_k(r["results"], r["expected_sources"], k) for r in rows) / len(rows)
            for k in ks} | {"mrr": sum(reciprocal_rank(r["results"], r["expected_sources"]) for r in rows) / len(rows)}
