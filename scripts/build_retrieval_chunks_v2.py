"""Build deterministic, Qdrant-free retrieval records from semantic JSON 2.2."""
from __future__ import annotations

import hashlib
import json
import re
import statistics
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "semantic_json"
OUT = ROOT / "data" / "retrieval_v2"
JSONL = OUT / "retrieval_chunks.jsonl"
MANIFEST = OUT / "retrieval_manifest.json"
REPORT = OUT / "retrieval_build_report.md"
THRESHOLD = 4500
TARGET = 3000
TOKENIZER_MODEL = "intfloat/multilingual-e5-base"
MAX_EMBEDDING_TOKENS = 500
TOKEN_TARGET = 380


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def all_chunks(doc):
    for section in doc.get("sections", []):
        for subsection in section.get("subsections", []):
            for chunk in subsection.get("chunks", []):
                yield section, subsection, chunk


def validate_semantic(doc, path):
    errors = []
    if doc.get("schema_version") != "2.2":
        errors.append("schema_version != 2.2")
    ids = []
    for section, subsection, chunk in all_chunks(doc):
        ids.append(chunk.get("chunk_id"))
        required = ["chunk_id", "content_type", "semantic_tags", "heading_path", "page_start", "page_end", "source_spans", "text", "temporal_scope"]
        for key in required:
            if key not in chunk:
                errors.append(f"{path.name}:{chunk.get('chunk_id')}: missing {key}")
        if not isinstance(chunk.get("semantic_tags"), list) or not all(isinstance(item, str) for item in chunk.get("semantic_tags", [])):
            errors.append(f"{path.name}:{chunk.get('chunk_id')}: invalid semantic_tags")
        spans = chunk.get("source_spans")
        if not isinstance(spans, list) or not spans:
            errors.append(f"{path.name}:{chunk.get('chunk_id')}: invalid source_spans")
            continue
        if chunk.get("text", "") != "\n\n".join(item.get("text", "") for item in spans):
            errors.append(f"{path.name}:{chunk.get('chunk_id')}: source text mismatch")
        pages = [item.get("page") for item in spans]
        if chunk.get("page_start") != min(pages) or chunk.get("page_end") != max(pages):
            errors.append(f"{path.name}:{chunk.get('chunk_id')}: page bounds")
    if len(ids) != len(set(ids)):
        errors.append(f"{path.name}: duplicate semantic chunk IDs")
    return errors


def trim_span(text: str, start: int, end: int):
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    return start, end


def paragraph_spans(text: str):
    spans = []
    cursor = 0
    for match in re.finditer(r"\n\s*\n+", text):
        start, end = trim_span(text, cursor, match.start())
        if start < end:
            spans.append((start, end))
        cursor = match.end()
    start, end = trim_span(text, cursor, len(text))
    if start < end:
        spans.append((start, end))
    return spans or [(0, len(text))]


def sentence_spans(text: str, start: int, end: int):
    segment = text[start:end]
    result = []
    cursor = 0
    for match in re.finditer(r"(?<=[.!?؟。])\s+", segment):
        a, b = trim_span(segment, cursor, match.start())
        if a < b:
            result.append((start + a, start + b))
        cursor = match.end()
    a, b = trim_span(segment, cursor, len(segment))
    if a < b:
        result.append((start + a, start + b))
    return result or [(start, end)]


def atomic_spans(text: str):
    atoms = paragraph_spans(text)
    if len(atoms) == 1 and len(text) > TARGET * 1.4:
        atoms = sentence_spans(text, *atoms[0])
    return atoms


def make_segments(text: str):
    """Return exact slices as (text, start, end, is_subchunk)."""
    if len(text) <= THRESHOLD:
        return [(text, 0, len(text), False)]
    atoms = atomic_spans(text)
    groups = []
    start = end = None
    for atom_start, atom_end in atoms:
        if start is None:
            start, end = atom_start, atom_end
            continue
        if atom_end - start > TARGET and end - start >= 1200:
            groups.append((start, end, True))
            start, end = atom_start, atom_end
        else:
            end = atom_end
    if start is not None:
        groups.append((start, end, True))
    if len(groups) == 1 and len(text) > THRESHOLD:
        lines = []
        for match in re.finditer(r"[^\n]+", text):
            a, b = trim_span(text, match.start(), match.end())
            if a < b:
                lines.append((a, b))
        if len(lines) > 1:
            groups = []
            start = end = None
            for atom_start, atom_end in lines:
                if start is None:
                    start, end = atom_start, atom_end
                elif atom_end - start > TARGET and end - start >= 1200:
                    groups.append((start, end, True))
                    start, end = atom_start, atom_end
                else:
                    end = atom_end
            if start is not None:
                groups.append((start, end, True))
    return [(text[start:end], start, end, sub) for start, end, sub in groups if text[start:end].strip()]


def page_mapping(parent, start_offset: int, end_offset: int):
    pages = []
    cursor = 0
    for span in parent["source_spans"]:
        a = cursor
        b = cursor + len(span["text"])
        cursor = b + 2
        if b > start_offset and a < end_offset:
            pages.append(span["page"])
    if pages:
        return sorted(set(pages)), "exact"
    return list(range(parent["page_start"], parent["page_end"] + 1)), "parent"


def has_evidence(text: str):
    return bool(re.search(r"\d", text) or re.search(r"(?:€|\$|£|dh|mad|%|km|ha|\+?\d[\d\s().-]{5,})", text, re.I) or "@" in text or re.search(r"https?://|www\.", text, re.I))


def classify_indexability(text: str, heading: str, content_type: str):
    cleaned = norm(text)
    heading_clean = norm(heading)
    ratio = SequenceMatcher(None, cleaned.casefold(), heading_clean.casefold()).ratio() if heading_clean else 0
    useful_types = {"contact_information", "statistics", "cost_information", "table", "faq", "procedure", "financial_product", "investment_opportunity", "industrial_zone", "service", "eligibility_conditions"}
    if (cleaned.casefold() == heading_clean.casefold() or (len(cleaned) < 400 and ratio >= 0.94)) and content_type not in useful_types:
        return False, "heading_only"
    words = re.findall(r"[\w\u0600-\u06ff]+", cleaned, re.UNICODE)
    if content_type not in useful_types and len(cleaned) <= 120 and len(words) <= 8 and not has_evidence(cleaned):
        return False, "navigation_only"
    if content_type not in useful_types and len(cleaned) <= 220 and re.fullmatch(r"[\w\s&/()'’,-]+", cleaned) and not has_evidence(cleaned):
        return False, "boilerplate_only"
    if len(cleaned) < 200 and (has_evidence(cleaned) or content_type in useful_types):
        return True, "short_but_informative"
    return True, "semantic_content"


def embedding_token_count(heading: str, body: str, tokenizer) -> int:
    """Count the exact future input, including E5 prefix and special tokens."""
    return len(tokenizer.encode(f"passage: {heading}\n{body}", add_special_tokens=True, truncation=False))


def word_spans(text: str, start: int, end: int):
    return [(m.start(), m.end()) for m in re.finditer(r"\S+", text[start:end])]


def safe_units(text: str, heading: str, tokenizer):
    """Create increasingly fine, original-offset units only when needed."""
    def refine(start, end):
        if embedding_token_count(heading, text[start:end], tokenizer) <= MAX_EMBEDDING_TOKENS:
            return [(start, end)]
        sentences = sentence_spans(text, start, end)
        if len(sentences) > 1:
            result = []
            for child_start, child_end in sentences:
                result.extend(refine(child_start, child_end))
            return result
        lines = [(start + m.start(), start + m.end()) for m in re.finditer(r"[^\n]+", text[start:end])]
        if len(lines) > 1:
            result = []
            for child_start, child_end in lines:
                result.extend(refine(child_start, child_end))
            return result
        words = [(start + a, start + b) for a, b in word_spans(text, start, end)]
        if len(words) > 1:
            return words
        return [(start, end)]

    refined = []
    for start, end in atomic_spans(text):
        refined.extend(refine(start, end))
    return refined


def token_refine(records, tokenizer):
    """Split only indexable records whose actual E5 input exceeds the budget."""
    before = list(records)
    refined = []
    split_details = []
    for record in before:
        if not record["indexable"] or record["embedding_token_count"] <= MAX_EMBEDDING_TOKENS:
            refined.append(record)
            continue
        heading = record["embedding_text"].split("\n", 1)[0]
        body = record["text"]
        units = safe_units(body, heading, tokenizer)
        groups = []
        start = end = None
        for unit_start, unit_end in units:
            if start is None:
                start, end = unit_start, unit_end
                continue
            candidate = body[start:unit_end]
            if embedding_token_count(heading, candidate, tokenizer) > TOKEN_TARGET and end > start:
                groups.append((start, end))
                start, end = unit_start, unit_end
            else:
                end = unit_end
        if start is not None:
            groups.append((start, end))
        if len(groups) <= 1:
            groups = [(0, len(body))]
        if len(groups) > 1:
            split_details.append((record, len(groups)))
        for suffix_index, (local_start, local_end) in enumerate(groups):
            child = dict(record)
            child["parent_start_offset"] = record["parent_start_offset"] + local_start
            child["parent_end_offset"] = record["parent_start_offset"] + local_end
            child["text"] = body[local_start:local_end]
            child["embedding_text"] = f"{heading}\n{child['text']}"
            child["embedding_token_count"] = embedding_token_count(heading, child["text"], tokenizer)
            mapped_pages, mapped_precision = page_mapping({"source_spans": record["source_spans"], "page_start": record["page_start"], "page_end": record["page_end"]}, child["parent_start_offset"], child["parent_end_offset"])
            child["source_pages"] = mapped_pages
            child["page_start"] = min(mapped_pages)
            child["page_end"] = max(mapped_pages)
            child["page_mapping_precision"] = mapped_precision
            if len(groups) > 1:
                letter = chr(ord("a") + suffix_index) if suffix_index < 26 else f"x{suffix_index + 1}"
                child["retrieval_chunk_id"] = f"{record['retrieval_chunk_id']}{letter}"
                child["is_subchunk"] = True
            refined.append(child)
    grouped = {}
    for record in refined:
        grouped.setdefault(record["parent_semantic_chunk_id"], []).append(record)
    for records_for_parent in grouped.values():
        count = len(records_for_parent)
        for index, record in enumerate(records_for_parent):
            record["retrieval_chunk_index"] = index
            record["retrieval_chunk_count"] = count
    return refined, before, split_details


def build_records(docs, tokenizer):
    records = []
    parents = []
    repeated = Counter()
    for path, doc in docs:
        meta = doc["metadata"]
        for section, subsection, parent in all_chunks(doc):
            parents.append(parent["chunk_id"])
            body = parent["text"]
            heading = " > ".join(parent.get("heading_path") or [subsection.get("title") or section.get("title") or meta.get("title", "")])
            for line in body.splitlines():
                clean = norm(line)
                if 20 <= len(clean) <= 180:
                    repeated[clean] += 1
            parts = make_segments(body)
            count = len(parts)
            for i, (segment, start_offset, end_offset, is_subchunk) in enumerate(parts, 1):
                pages, precision = page_mapping(parent, start_offset, end_offset)
                content_type = parent.get("content_type")
                indexable, reason = classify_indexability(segment, heading, content_type)
                ref = parent.get("temporal_scope", {}).get("reference_period", {}) or {}
                records.append({
                    "retrieval_chunk_id": f"{parent['chunk_id']}__r{i:03d}",
                    "parent_semantic_chunk_id": parent["chunk_id"],
                    "document_id": doc["document_id"],
                    "document_family_id": doc["document_family_id"],
                    "filename": meta.get("filename", path.name),
                    "language": meta.get("language"),
                    "document_title": meta.get("title"),
                    "topic_id": section.get("topic_id"),
                    "content_type": content_type,
                    "semantic_tags": parent.get("semantic_tags", []),
                    "heading_path": parent.get("heading_path", []),
                    "page_start": min(pages),
                    "page_end": max(pages),
                    "source_pages": pages,
                    "source_spans": parent.get("source_spans", []),
                    "page_mapping_precision": precision,
                    "temporal_scope": parent.get("temporal_scope", {}),
                    "primary_year": parent.get("temporal_scope", {}).get("primary_year"),
                    "years_mentioned": parent.get("temporal_scope", {}).get("years_mentioned", []),
                    "reference_period_type": ref.get("type"),
                    "reference_period_year": ref.get("year"),
                    "reference_period_end_date": ref.get("end_date"),
                    "retrieval_chunk_index": i - 1,
                    "retrieval_chunk_count": count,
                    "is_subchunk": is_subchunk,
                    "parent_start_offset": start_offset,
                    "parent_end_offset": end_offset,
                    "indexable": indexable,
                    "indexability_reason": reason,
                    "text": segment,
                    "embedding_text": f"passage: {heading}\n{segment}",
                    "embedding_token_count": embedding_token_count(heading, segment, tokenizer),
                })
    return records, parents, repeated


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_MODEL)
    previous_jsonl_hash = sha(JSONL) if JSONL.exists() else None
    previous_manifest = json.loads(MANIFEST.read_text(encoding="utf8")) if MANIFEST.exists() else {}
    previous_count = previous_manifest.get("retrieval_chunk_count")
    docs, errors = [], []
    for path in sorted(SOURCE.glob("*.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf8"))
        except Exception as exc:
            errors.append(f"{path.name}: invalid UTF-8/JSON: {exc}")
            continue
        if doc.get("schema_version") != "2.2":
            continue
        errors.extend(validate_semantic(doc, path))
        docs.append((path, doc))
    if errors:
        raise SystemExit("\n".join(errors[:50]))
    records, parents, repeated = build_records(docs, tokenizer)
    records, before_token_records, token_split_details = token_refine(records, tokenizer)
    with JSONL.open("w", encoding="utf8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    jsonl_hash = sha(JSONL)

    parent_map = {p["chunk_id"]: p for _, doc in docs for _, _, p in all_chunks(doc)}
    record_errors = []
    for record in records:
        parent = parent_map.get(record["parent_semantic_chunk_id"])
        if parent is None:
            record_errors.append(record["retrieval_chunk_id"] + ": missing parent")
            continue
        for field in ["content_type", "semantic_tags", "heading_path", "temporal_scope", "source_spans"]:
            if record[field] != parent[field]:
                record_errors.append(record["retrieval_chunk_id"] + f": inherited {field} mismatch")
        if not set(record["source_pages"]).issubset(set(range(parent["page_start"], parent["page_end"] + 1))):
            record_errors.append(record["retrieval_chunk_id"] + ": page outside parent bounds")
        if not record["text"].strip():
            record_errors.append(record["retrieval_chunk_id"] + ": empty text")
        if not isinstance(record["indexable"], bool) or not isinstance(record["indexability_reason"], str):
            record_errors.append(record["retrieval_chunk_id"] + ": invalid indexability fields")
        if record["indexable"] and not record["embedding_text"].strip():
            record_errors.append(record["retrieval_chunk_id"] + ": empty embedding_text")
        if record["page_mapping_precision"] == "exact":
            expected, _ = page_mapping(parent, record["parent_start_offset"], record["parent_end_offset"])
            if expected != record["source_pages"]:
                record_errors.append(record["retrieval_chunk_id"] + ": offset/page mapping mismatch")
        if record["indexable"] and record["embedding_token_count"] > MAX_EMBEDDING_TOKENS:
            record_errors.append(record["retrieval_chunk_id"] + ": indexable embedding exceeds safe token budget")
    if record_errors:
        raise SystemExit("\n".join(record_errors[:50]))

    sizes = [len(record["text"]) for record in records]
    before_token_sizes = [record["embedding_token_count"] for record in before_token_records]
    after_token_sizes = [record["embedding_token_count"] for record in records]
    oversized_before = [record for record in before_token_records if record["indexable"] and record["embedding_token_count"] > MAX_EMBEDDING_TOKENS]
    oversized_after = [record for record in records if record["indexable"] and record["embedding_token_count"] > MAX_EMBEDDING_TOKENS]
    oversized_families = Counter(record["document_family_id"] for record in oversized_before)
    oversized_languages = Counter(record["language"] for record in oversized_before)
    oversized_types = Counter(record["content_type"] for record in oversized_before)
    languages = Counter(record["language"] for record in records)
    types = Counter(record["content_type"] for record in records)
    families = Counter(record["document_family_id"] for record in records)
    precision = Counter(record["page_mapping_precision"] for record in records)
    reasons = Counter(record["indexability_reason"] for record in records)
    non_indexable = [record for record in records if not record["indexable"]]
    short_counts = {"<50": sum(x < 50 for x in sizes), "<100": sum(x < 100 for x in sizes), "<200": sum(x < 200 for x in sizes)}
    short_indexable = sum(len(record["text"]) < 200 and record["indexable"] for record in records)
    covered = {record["parent_semantic_chunk_id"] for record in records}
    splitparents = Counter(record["parent_semantic_chunk_id"] for record in records)
    indexable_parents = {record["parent_semantic_chunk_id"] for record in records if record["indexable"]}
    parent_mapping_records = [record for record in records if record["page_mapping_precision"] == "parent"]
    parent_mapping_by_family = Counter(record["document_family_id"] for record in parent_mapping_records)
    parent_mapping_by_language = Counter(record["language"] for record in parent_mapping_records)
    non_indexable_by_family = Counter(record["document_family_id"] for record in non_indexable)

    manifest = {
        "retrieval_schema_version": "2.0", "source_schema_version": "2.2", "source_semantic_document_count": len(docs), "source_semantic_chunk_count": len(parents), "retrieval_chunk_count": len(records), "previous_retrieval_chunk_count": previous_count,
        "unsplit_count": sum(v == 1 for v in splitparents.values()), "split_count": sum(v > 1 for v in splitparents.values()), "parents_producing_multiple_chunks": sum(v > 1 for v in splitparents.values()), "parents_covered": len(covered), "parents_with_at_least_one_indexable_record": len(indexable_parents), "parents_with_only_non_indexable_records": len(set(parents) - indexable_parents),
        "language_distribution": dict(sorted(languages.items())), "content_type_distribution": dict(sorted(types.items())), "document_family_distribution": dict(sorted(families.items())), "indexable_record_count": len(records) - len(non_indexable), "non_indexable_record_count": len(non_indexable), "indexability_reason_distribution": dict(sorted(reasons.items())), "non_indexable_by_family": dict(sorted(non_indexable_by_family.items())), "short_record_counts": short_counts, "short_records_still_indexable": short_indexable,
        "retrieval_text_characters": {"min": min(sizes), "median": statistics.median(sizes), "mean": statistics.mean(sizes), "max": max(sizes), ">3000": sum(x > 3000 for x in sizes), ">4500": sum(x > 4500 for x in sizes), ">5000": sum(x > 5000 for x in sizes), ">8000": sum(x > 8000 for x in sizes), ">12000": sum(x > 12000 for x in sizes)},
        "e5_token_budget": {"tokenizer_model": TOKENIZER_MODEL, "model_max_length": 512, "safe_max_embedding_tokens": MAX_EMBEDDING_TOKENS, "token_target_for_oversized_records": TOKEN_TARGET, "records_before_token_refinement": len(before_token_records), "records_after_token_refinement": len(records), "indexable_records": sum(record["indexable"] for record in records), "non_indexable_records": sum(not record["indexable"] for record in records), "max_embedding_token_count": max(after_token_sizes), "median_embedding_token_count": statistics.median(after_token_sizes), "mean_embedding_token_count": statistics.mean(after_token_sizes), "records_over_500_before": sum(record["embedding_token_count"] > 500 for record in before_token_records), "records_over_500_after": sum(record["embedding_token_count"] > 500 for record in records), "records_over_512_before": sum(record["embedding_token_count"] > 512 for record in before_token_records), "records_over_512_after": sum(record["embedding_token_count"] > 512 for record in records), "records_additionally_split": len(token_split_details), "oversized_before_by_language": dict(sorted(oversized_languages.items())), "oversized_before_by_family": dict(sorted(oversized_families.items())), "oversized_before_by_content_type": dict(sorted(oversized_types.items()))},
        "page_mapping_precision_counts": dict(sorted(precision.items())), "parent_mapping_by_family": dict(sorted(parent_mapping_by_family.items())), "parent_mapping_by_language": dict(sorted(parent_mapping_by_language.items())), "embedding_convention": "passage: <heading context>\\n<body text>", "qdrant_ingestion_performed": False, "jsonl_sha256": jsonl_hash, "determinism_test": {"status": "PASS" if previous_jsonl_hash == jsonl_hash else "PENDING_SECOND_RUN", "previous_hash": previous_jsonl_hash, "current_hash": jsonl_hash},
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf8")

    lines = ["# Phase 4A — Retrieval chunk build report", "", "## Scope", "", "Built deterministic retrieval records from all schema-2.2 semantic JSON documents. Semantic JSON, raw JSON, Qdrant, embeddings, loaders, retrievers, prompts, and production collections were not modified.", "", f"- Semantic documents: {len(docs)}", f"- Semantic parents: {len(parents)}", f"- Retrieval records: {len(records)}", f"- Previous retrieval-record count: {previous_count}", f"- Parents covered: {len(covered)} / {len(parents)}", f"- Parents with at least one indexable record: {len(indexable_parents)} / {len(parents)}", f"- Parents with only non-indexable records: {len(set(parents) - indexable_parents)}", f"- Unsplit parents: {sum(v == 1 for v in splitparents.values())}", f"- Split parents: {sum(v > 1 for v in splitparents.values())}", "", "## Offset-based page mapping", "", "Split segments retain original character offsets in the semantic parent text. Page mapping uses those offsets against ordered source spans and never searches reconstructed segment text.", "", f"- Exact mappings: {precision.get('exact', 0)}", f"- Parent mappings: {precision.get('parent', 0)}", "", "### Remaining parent mappings", ""]
    if parent_mapping_records:
        for record in parent_mapping_records:
            lines.append(f"- `{record['retrieval_chunk_id']}` — family `{record['document_family_id']}`, language `{record['language']}`, parent `{record['parent_semantic_chunk_id']}`; offset interval did not intersect a source span.")
    else:
        lines.append("- None.")
    lines += ["", "## Indexability gate", "", "Indexability is conservative and does not use character count alone. Short factual, statistical, cost, contact, project, FAQ, and eligibility records remain indexable.", "", f"- Indexable records: {len(records) - len(non_indexable)}", f"- Non-indexable records: {len(non_indexable)}", f"- Short indexable records (<200 chars): {short_indexable}", "", "### Indexability reason distribution", ""]
    for reason, count in sorted(reasons.items()):
        lines.append(f"- `{reason}`: {count}")
    lines += ["", "### Non-indexable records", ""]
    if non_indexable:
        for record in non_indexable:
            lines.append(f"- `{record['retrieval_chunk_id']}` — `{record['indexability_reason']}`, {len(record['text'])} chars, family `{record['document_family_id']}`; text: `{norm(record['text'])[:160]}`")
    else:
        lines.append("- None.")
    lines += ["", "## Retrieval design", "", "Parents at or below 4,500 characters remain intact. Larger parents are split using original-offset paragraph/sentence/line boundaries toward approximately 3,000 characters. No generic overlap is applied at clean boundaries. Each record retains full parent source spans for Phase 4A provenance.", "", "## E5 token-budget validation", "", f"- Tokenizer/model: `{TOKENIZER_MODEL}`", "- Model maximum sequence length: 512 tokens", f"- Safe maximum: {MAX_EMBEDDING_TOKENS} tokens, counted with `add_special_tokens=True` and including the literal `passage: ` prefix and heading context", f"- Oversized indexable records before refinement (>500): {len(oversized_before)}", f"- Oversized indexable records after refinement (>500): {len(oversized_after)}", f"- Records over 512 before: {sum(record['embedding_token_count'] > 512 for record in before_token_records)}", f"- Records over 512 after: {sum(record['embedding_token_count'] > 512 for record in records)}", f"- Records additionally split: {len(token_split_details)}", f"- Final maximum embedding token count: {max(after_token_sizes)}", f"- Final median embedding token count: {statistics.median(after_token_sizes):.1f}", f"- Final mean embedding token count: {statistics.mean(after_token_sizes):.1f}", "", "### Records split for token budget", ""]
    if token_split_details:
        for record, count in token_split_details:
            lines.append(f"- `{record['retrieval_chunk_id']}` — {record['embedding_token_count']} tokens before; produced {count} deterministic descendants.")
    else:
        lines.append("- None.")
    lines += ["", "## Chunk-size diagnostics", "", f"- Minimum: {min(sizes)}", f"- Median: {statistics.median(sizes):.1f}", f"- Mean: {statistics.mean(sizes):.1f}", f"- Maximum: {max(sizes)}", f"- <50: {short_counts['<50']}", f"- <100: {short_counts['<100']}", f"- <200: {short_counts['<200']}", f"- >3,000: {sum(x > 3000 for x in sizes)}", f"- >4,500: {sum(x > 4500 for x in sizes)}", f"- >5,000: {sum(x > 5000 for x in sizes)}", f"- >8,000: {sum(x > 8000 for x in sizes)}", f"- >12,000: {sum(x > 12000 for x in sizes)}", "", "## Boilerplate diagnostics", "", "Repeated source lines were counted but not removed. No aggressive boilerplate suppression was applied to embedding_text.", ""]
    for line, count in repeated.most_common(20):
        if count >= 5:
            lines.append(f"- `{line[:180]}` — {count} parent occurrences")
    lines += ["", "## Phase-4B Qdrant payload planning", "", "Phase 4A JSONL retains full source_spans. A compact future Qdrant payload should include: retrieval_chunk_id, parent_semantic_chunk_id, document_id, document_family_id, filename, language, document_title, topic_id, content_type, semantic_tags, heading_path, page_start, page_end, source_pages, page_mapping_precision, primary_year, years_mentioned, reference_period_type, reference_period_year, reference_period_end_date, retrieval_chunk_index, retrieval_chunk_count, is_subchunk, indexable, and text. Full source_spans should remain in the semantic/provenance layer and be resolved separately rather than duplicated into every production payload.", "", "## Validation", "", f"Semantic input validation: PASS for {len(docs)} schema-2.2 documents.", f"Retrieval coverage: {'PASS' if len(covered) == len(parents) else 'FAIL'} — {len(covered)} parents covered / {len(parents)}.", f"Retrieval IDs: {'PASS' if len({r['retrieval_chunk_id'] for r in records}) == len(records) else 'FAIL'}.", f"Metadata inheritance and bounds: {'PASS' if not record_errors else 'FAIL'}.", f"Indexability fields: {'PASS' if all(isinstance(r['indexable'], bool) and isinstance(r['indexability_reason'], str) for r in records) else 'FAIL'}.", f"Indexable embedding text: {'PASS' if all(r['embedding_text'].strip() for r in records if r['indexable']) else 'FAIL'}.", f"Offset-based exact mapping consistency: {'PASS' if not record_errors else 'FAIL'}.", f"Exact page mappings: {'PASS' if precision.get('parent', 0) == 0 and precision.get('exact', 0) == len(records) else 'FAIL'} — {precision.get('exact', 0)} exact, {precision.get('parent', 0)} parent.", f"E5 safe token budget: {'PASS' if not oversized_after else 'FAIL'} — all indexable embedding inputs are <= {MAX_EMBEDDING_TOKENS} tokens.", f"Determinism SHA-256: {'PASS' if previous_jsonl_hash == jsonl_hash else 'PENDING_SECOND_RUN'} — current `{jsonl_hash}`.", "", "## Output artifacts", "", f"- `{JSONL.relative_to(ROOT)}`", f"- `{MANIFEST.relative_to(ROOT)}`", f"- `{REPORT.relative_to(ROOT)}`", "", "Qdrant ingestion: **not performed**. Production embeddings: **not calculated**."]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf8")
    print(json.dumps({"documents": len(docs), "parents": len(parents), "records": len(records), "jsonl_sha256": sha(JSONL), "manifest_sha256": sha(MANIFEST)}))


if __name__ == "__main__":
    main()
