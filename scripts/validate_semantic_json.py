"""Validate semantic JSON schema 2.2 without touching source data."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ALLOWED_CONTENT_TYPES = {
    "narrative", "statistics", "procedure", "faq", "financial_product",
    "investment_opportunity", "industrial_zone", "cost_information",
    "contact_information", "legal_information", "service",
    "eligibility_conditions", "table",
}
CANONICAL_ID = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")


def _string_list(value, field: str, errors: list[str]) -> None:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        errors.append(f"{field} must be an array of non-empty strings")


def _temporal_scope(value, chunk_id: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{chunk_id}: temporal_scope must be an object")
        return
    for field in ("primary_year", "years_mentioned", "reference_period"):
        if field not in value:
            errors.append(f"{chunk_id}: temporal_scope missing {field}")
    if value.get("primary_year") is not None and not isinstance(value.get("primary_year"), int):
        errors.append(f"{chunk_id}: primary_year must be integer or null")
    years = value.get("years_mentioned")
    if not isinstance(years, list) or not all(isinstance(year, int) for year in years):
        errors.append(f"{chunk_id}: years_mentioned must be an array of integers")
    elif years != sorted(set(years)):
        errors.append(f"{chunk_id}: years_mentioned must be sorted and unique")
    period = value.get("reference_period")
    if not isinstance(period, dict):
        errors.append(f"{chunk_id}: reference_period must be an object")
    else:
        for field in ("type", "year", "semester", "quarter", "start_date", "end_date"):
            if field not in period:
                errors.append(f"{chunk_id}: reference_period missing {field}")
        if period.get("year") is not None and not isinstance(period.get("year"), int):
            errors.append(f"{chunk_id}: reference_period.year must be integer or null")


def validate(path: Path, source: Path | None = None) -> list[str]:
    errors: list[str] = []
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"invalid UTF-8 or JSON: {exc}"]
    if not isinstance(document, dict):
        return ["root must be an object"]
    for field in ("schema_version", "document_id", "document_family_id", "metadata", "sections"):
        if field not in document:
            errors.append(f"missing root field: {field}")
    if document.get("schema_version") != "2.2":
        errors.append("schema_version must be '2.2'")
    if not isinstance(document.get("document_id"), str) or not document.get("document_id"):
        errors.append("document_id must be a non-empty string")
    if not isinstance(document.get("document_family_id"), str) or not document.get("document_family_id"):
        errors.append("document_family_id must be a non-empty string")
    metadata = document.get("metadata")
    if not isinstance(metadata, dict):
        errors.append("metadata must be an object")
    else:
        for field in ("title", "filename", "language", "document_type", "publisher", "region", "publication_year", "reference_period", "topics"):
            if field not in metadata:
                errors.append(f"missing metadata field: {field}")
        for field in ("title", "filename", "language", "document_type", "publisher", "region"):
            if field in metadata and not isinstance(metadata[field], str):
                errors.append(f"metadata.{field} must be a string")
        _string_list(metadata.get("topics"), "metadata.topics", errors)
    if not isinstance(document.get("sections"), list):
        errors.append("sections must be an array")
        return errors
    ids: set[str] = set()
    for section in document["sections"]:
        for field in ("section_id", "title", "topic_id", "subsections"):
            if field not in section:
                errors.append(f"section missing {field}")
        if not isinstance(section.get("title"), str) or not section.get("title"):
            errors.append("section.title must be a non-empty source-language string")
        if not isinstance(section.get("topic_id"), str) or not section.get("topic_id"):
            errors.append("section.topic_id must be a non-empty identifier")
        elif not CANONICAL_ID.fullmatch(section["topic_id"]):
            errors.append(f"section.topic_id must be a canonical snake_case identifier: {section['topic_id']}")
        for subsection in section.get("subsections", []):
            for field in ("subsection_id", "title", "chunks"):
                if field not in subsection:
                    errors.append(f"subsection missing {field}")
            if not isinstance(subsection.get("title"), str) or not subsection.get("title"):
                errors.append("subsection.title must be a non-empty source-language string")
            for chunk in subsection.get("chunks", []):
                required = ("chunk_id", "content_type", "semantic_tags", "heading_path", "page_start", "page_end", "source_spans", "text", "keywords", "entities", "temporal_scope")
                for field in required:
                    if field not in chunk:
                        errors.append(f"chunk missing {field}")
                chunk_id = chunk.get("chunk_id", "<unknown>")
                if chunk_id in ids:
                    errors.append(f"duplicate chunk_id: {chunk_id}")
                ids.add(chunk_id)
                if chunk.get("content_type") not in ALLOWED_CONTENT_TYPES:
                    errors.append(f"{chunk_id}: unsupported content_type: {chunk.get('content_type')}")
                _string_list(chunk.get("semantic_tags"), f"{chunk_id}.semantic_tags", errors)
                _string_list(chunk.get("heading_path"), f"{chunk_id}.heading_path", errors)
                _string_list(chunk.get("keywords"), f"{chunk_id}.keywords", errors)
                _string_list(chunk.get("entities"), f"{chunk_id}.entities", errors)
                if not isinstance(chunk.get("page_start"), int) or not isinstance(chunk.get("page_end"), int):
                    errors.append(f"{chunk_id}: page_start/page_end must be integers")
                elif chunk["page_start"] > chunk["page_end"]:
                    errors.append(f"{chunk_id}: page_start is greater than page_end")
                if not isinstance(chunk.get("text"), str) or not chunk["text"].strip():
                    errors.append(f"{chunk_id}: text must be non-empty")
                spans = chunk.get("source_spans")
                if not isinstance(spans, list) or not spans:
                    errors.append(f"{chunk_id}: source_spans must be a non-empty array")
                else:
                    span_pages = []
                    span_texts = []
                    for span in spans:
                        if not isinstance(span, dict) or not isinstance(span.get("page"), int) or not isinstance(span.get("text"), str):
                            errors.append(f"{chunk_id}: each source span needs integer page and string text")
                            continue
                        span_pages.append(span["page"])
                        span_texts.append(span["text"])
                    if span_pages:
                        if chunk.get("page_start") != min(span_pages) or chunk.get("page_end") != max(span_pages):
                            errors.append(f"{chunk_id}: page_start/page_end must match source span bounds")
                        if chunk.get("text") != "\n\n".join(span_texts):
                            errors.append(f"{chunk_id}: text must equal source span text joined by blank lines")
                        if source is not None:
                            try:
                                source_doc = json.loads(source.read_text(encoding="utf-8"))
                                source_pages = {int(item["page"]): str(item.get("text") or "") for item in source_doc.get("pages", [])}
                            except Exception as exc:
                                errors.append(f"{chunk_id}: could not read source for span validation: {exc}")
                                source_pages = {}
                            for span in spans:
                                page, text = span.get("page"), span.get("text")
                                if page not in source_pages or not source_pages[page].strip():
                                    errors.append(f"{chunk_id}: source page {page} missing or empty")
                                elif text not in source_pages[page]:
                                    errors.append(f"{chunk_id}: source span is not an exact substring of page {page}")
                _temporal_scope(chunk.get("temporal_scope"), chunk_id, errors)
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--source-dir", type=Path, default=None, help="Optional raw JSON directory for exact source-span validation")
    args = parser.parse_args()
    failures = 0
    for path in args.paths:
        source = (args.source_dir / path.name) if args.source_dir is not None else None
        errors = validate(path, source)
        if errors:
            failures += 1
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {path}")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
