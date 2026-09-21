"""Conservative duplicate and diversity handling for evidence candidates."""

import re
from typing import Any


def _normalized_text(text: str) -> str:
    return re.sub(r"\W+", " ", (text or "").casefold(), flags=re.UNICODE).strip()


def deduplicate(candidates: list[dict[str, Any]], max_per_document: int = 2) -> list[dict[str, Any]]:
    selected, by_chunk, by_page, by_text, doc_counts = [], set(), set(), set(), {}
    for candidate in candidates:
        chunk_id = candidate.get("chunk_id")
        page_key = (candidate.get("document_id"), candidate.get("page"))
        text_key = _normalized_text(candidate.get("text", ""))
        if chunk_id and chunk_id in by_chunk:
            candidate["exclusion_reason"] = "duplicate_chunk"; continue
        if page_key in by_page:
            representative = next((item for item in selected
                                   if (item.get("document_id"), item.get("page")) == page_key), None)
            if representative is not None:
                representative.setdefault("equivalent_sources", []).append(_citation(candidate))
            candidate["exclusion_reason"] = "duplicate_document_page"; continue
        if text_key and text_key in by_text:
            representative = next((item for item in selected
                                   if _normalized_text(item.get("text", "")) == text_key), None)
            if representative is not None:
                representative.setdefault("equivalent_sources", []).append(_citation(candidate))
            candidate["exclusion_reason"] = "equivalent_content"; continue
        document_id = candidate.get("document_id")
        if document_id and doc_counts.get(document_id, 0) >= max_per_document:
            candidate["exclusion_reason"] = "document_diversity_limit"; continue
        if chunk_id: by_chunk.add(chunk_id)
        by_page.add(page_key)
        if text_key: by_text.add(text_key)
        if document_id: doc_counts[document_id] = doc_counts.get(document_id, 0) + 1
        selected.append(candidate)
    return selected


def _citation(candidate: dict[str, Any]) -> dict[str, Any]:
    return {key: candidate.get(key) for key in ("document_id", "filename", "page", "language")}
