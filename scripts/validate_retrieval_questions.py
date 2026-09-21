"""Validate retrieval ground truth against the immutable prepared chunks."""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SUPPORTED_LANGUAGES = {"fr", "ar", "es", "en"}
REQUIRED_FIELDS = {"id", "question", "query_language", "answerable", "cross_lingual", "expected_sources"}
MOJIBAKE_CODEPOINTS = {0x00C2, 0x00C3, 0x00D8, 0x00D9}
ARABIC_RANGES = ((0x0600, 0x06FF), (0x0750, 0x077F), (0x08A0, 0x08FF))


def contains_arabic(text: str) -> bool:
    return any(start <= ord(char) <= end for char in text for start, end in ARABIC_RANGES)


def likely_mojibake(text: str) -> bool:
    """Detect common UTF-8-as-CP1252 artifacts without rejecting Arabic."""
    return any(ord(char) in MOJIBAKE_CODEPOINTS for char in text)


def validate_question_text(text: str, language: str) -> list[str]:
    errors = []
    if likely_mojibake(text):
        errors.append("contains likely UTF-8/CP1252 mojibake")
    if language == "ar":
        if not contains_arabic(text):
            errors.append("Arabic question contains no Arabic Unicode characters")
        if text and sum(char.isascii() for char in text) > len(text) * 0.75:
            errors.append("Arabic question is primarily ASCII/mojibake text")
    return errors


def normalize_question(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def is_cross_language_hit(result: dict, question: dict) -> bool:
    """Return whether a retrieved result is valid ground truth in another language.

    A same-language expected source is intentionally not a cross-lingual hit,
    even when the question's ``cross_lingual`` flag is true.
    """
    if result.get("language") == question.get("query_language"):
        return False
    return any(result.get("document_id") == source.get("document_id") and
               result.get("page") == source.get("page") and
               result.get("language") == source.get("language")
               for source in question.get("expected_sources", []))


def validate(question_path: Path, chunks_path: Path) -> tuple[list[str], dict]:
    errors: list[str] = []
    questions = json.loads(question_path.read_text(encoding="utf-8"))
    chunks_data = json.loads(chunks_path.read_text(encoding="utf-8"))
    if not isinstance(questions, list):
        return ["Question file root must be a JSON list"], {}
    source_pages: dict[tuple[object, object], set[str | None]] = {}
    for chunk in chunks_data.get("chunks", []):
        metadata = chunk["metadata"]
        key = (metadata.get("document_id"), metadata.get("page"))
        source_pages.setdefault(key, set()).add(metadata.get("language"))
    document_ids = {document_id for document_id, _ in source_pages}
    chunk_ids = {c.get("chunk_id") for c in chunks_data.get("chunks", [])}
    ids: set[str] = set()
    normalized_questions: set[str] = set()
    for index, question in enumerate(questions, start=1):
        label = f"question {index}"
        if not isinstance(question, dict):
            errors.append(f"{label}: must be an object")
            continue
        missing = REQUIRED_FIELDS - question.keys()
        if missing:
            errors.append(f"{label}: missing fields {sorted(missing)}")
        question_id = question.get("id")
        if question_id in ids:
            errors.append(f"{label}: duplicate id {question_id}")
        ids.add(question_id)
        text = question.get("question")
        if not isinstance(text, str) or not text.strip():
            errors.append(f"{label}: question must be non-empty text")
        else:
            for text_error in validate_question_text(text, question.get("query_language")):
                errors.append(f"{label}: {text_error}")
            normalized = normalize_question(text)
            if normalized in normalized_questions:
                errors.append(f"{label}: duplicate question after normalization")
            normalized_questions.add(normalized)
        if question.get("query_language") not in SUPPORTED_LANGUAGES:
            errors.append(f"{label}: unsupported query_language {question.get('query_language')!r}")
        if not isinstance(question.get("answerable"), bool):
            errors.append(f"{label}: answerable must be boolean")
        sources = question.get("expected_sources")
        if not isinstance(sources, list):
            errors.append(f"{label}: expected_sources must be a list")
            sources = []
        if question.get("answerable") is True and not sources:
            errors.append(f"{label}: answerable question needs an expected source")
        if question.get("answerable") is False and sources:
            errors.append(f"{label}: unanswerable question must have no expected source")
        seen_sources: set[tuple[object, object]] = set()
        for source in sources:
            if not isinstance(source, dict) or {"document_id", "page", "language"} - source.keys():
                errors.append(f"{label}: each expected source needs document_id, page, and language")
                continue
            key = (source["document_id"], source["page"])
            if key in seen_sources:
                errors.append(f"{label}: duplicate expected source {key}")
            seen_sources.add(key)
            if source["document_id"] not in document_ids:
                errors.append(f"{label}: unknown document_id {source['document_id']}")
            elif key not in source_pages:
                errors.append(f"{label}: source page does not exist {key}")
            else:
                if source["language"] not in SUPPORTED_LANGUAGES:
                    errors.append(f"{label}: unsupported source language {source['language']!r}")
                actual_languages = source_pages[key]
                if source["language"] not in actual_languages:
                    errors.append(f"{label}: source language {source['language']!r} does not match chunks metadata {sorted(actual_languages)!r} for {key}")
        for chunk_id in question.get("expected_chunk_ids", []):
            if chunk_id not in chunk_ids:
                errors.append(f"{label}: unknown expected_chunk_id {chunk_id}")
    answerable = [q for q in questions if q.get("answerable") is True]
    same_language_capable = sum(any(source.get("language") == q.get("query_language")
                                    for source in q.get("expected_sources", [])) for q in answerable)
    cross_language_capable = sum(any(source.get("language") != q.get("query_language")
                                     for source in q.get("expected_sources", [])) for q in answerable)
    stats = {"total_questions": len(questions), "answerable": len(answerable),
             "unanswerable": len(questions) - len(answerable),
             "by_language": dict(Counter(q.get("query_language") for q in questions)),
             "by_topic": dict(Counter(q.get("topic", "unspecified") for q in questions)),
             "same_language_capable": same_language_capable,
             "cross_language_capable": cross_language_capable,
             "unique_source_documents": len({s["document_id"] for q in answerable
                                              for s in q.get("expected_sources", [])})}
    return errors, stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", type=Path, default=PROJECT_ROOT / "evaluation" / "retrieval_questions.json")
    parser.add_argument("--chunks", type=Path, default=PROJECT_ROOT / "data" / "processed" / "chunks.json")
    args = parser.parse_args()
    try:
        errors, stats = validate(args.questions, args.chunks)
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"Validation failed: {exc}")
        return 1
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    if errors:
        print("Errors:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("Validation passed with 0 errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
