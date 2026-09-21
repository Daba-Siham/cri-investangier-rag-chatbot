"""Explainable year-aware and exact-token scoring features."""

import re

YEAR_RE = re.compile(r"(?<!\d)(?:19|20)\d{2}(?!\d)")
NUMBER_RE = re.compile(r"(?<!\w)\d+(?:[.,]\d+)?\s*%?(?!\w)")
UPPER_RE = re.compile(r"\b[A-Z][A-Z0-9]{2,}\b")


def extract_years(text: str) -> set[int]:
    return {int(value) for value in YEAR_RE.findall(text or "")}


def extract_document_years(filename: str | None, document_id: str | None) -> set[int]:
    """Extract years describing the document identity, not its body content."""
    return extract_years(f"{filename or ''} {document_id or ''}")


def extract_exact_tokens(text: str, include_years: bool = False) -> set[str]:
    text = text or ""
    tokens = {value.lower().replace(" ", "") for value in NUMBER_RE.findall(text)
              if include_years or not re.fullmatch(r"(?:19|20)\d{2}", value.strip())}
    tokens.update(value.lower() for value in UPPER_RE.findall(text))
    return tokens


def temporal_adjustment(query_years: set[int], candidate_years: set[int], bonus: float, penalty: float) -> float:
    if not query_years or not candidate_years:
        return 0.0
    if query_years & candidate_years:
        return bonus
    return -penalty


def temporal_score(query_years: set[int], document_years: set[int], mentioned_years: set[int],
                   bonus: float, penalty: float) -> tuple[float, str]:
    if not query_years:
        return 0.0, "no_temporal_signal"
    if document_years:
        if query_years & document_years:
            return bonus, "document_year_match"
        return -penalty, "document_year_conflict"
    if query_years & mentioned_years:
        return bonus, "mentioned_year_match"
    return 0.0, "no_temporal_signal"


def exact_match_adjustment(query_tokens: set[str], candidate_text: str, bonus: float) -> float:
    if not query_tokens:
        return 0.0
    candidate_tokens = extract_exact_tokens(candidate_text)
    return bonus * len(query_tokens & candidate_tokens)
