"""Phase 4D context assembly and exact citation resolution for retriever v2."""
from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_JSONL = ROOT / "data" / "retrieval_v2" / "retrieval_chunks.jsonl"
DEFAULT_MANIFEST = ROOT / "data" / "retrieval_v2" / "retrieval_manifest.json"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def page_label(pages: Iterable[int]) -> str:
    values = sorted(dict.fromkeys(int(page) for page in pages))
    if not values:
        return "p. ?"
    if len(values) == 1:
        return f"p. {values[0]}"
    if values == list(range(values[0], values[-1] + 1)):
        return f"pp. {values[0]}–{values[-1]}"
    return "pp. " + ", ".join(str(page) for page in values)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", text.casefold(), flags=re.UNICODE)).strip()


class ProvenanceStore:
    """Immutable lookup over the finalized retrieval JSONL artifact."""

    def __init__(self, jsonl_path: Path = DEFAULT_JSONL, manifest_path: Path = DEFAULT_MANIFEST):
        self.jsonl_path = Path(jsonl_path)
        self.manifest_path = Path(manifest_path)
        self.manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        actual = _sha256(self.jsonl_path)
        expected = str(self.manifest.get("jsonl_sha256", "")).upper()
        if not expected or actual != expected:
            raise RuntimeError(f"Retrieval artifact SHA-256 mismatch: expected {expected}, got {actual}")
        self.jsonl_sha256 = actual
        self.records: dict[str, dict[str, Any]] = {}
        self.by_parent: dict[str, list[dict[str, Any]]] = defaultdict(list)
        with self.jsonl_path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                record = json.loads(line)
                rid = record.get("retrieval_chunk_id")
                if not rid or rid in self.records:
                    raise RuntimeError(f"Duplicate or missing retrieval_chunk_id at line {line_number}")
                self.records[rid] = record
                self.by_parent[record["parent_semantic_chunk_id"]].append(record)
        for children in self.by_parent.values():
            children.sort(key=lambda item: (item.get("retrieval_chunk_index", 0), item["retrieval_chunk_id"]))

    def get(self, retrieval_chunk_id: str) -> dict[str, Any]:
        try:
            return self.records[retrieval_chunk_id]
        except KeyError as exc:
            raise RuntimeError(f"Retrieval chunk is absent from provenance JSONL: {retrieval_chunk_id}") from exc

    @staticmethod
    def _parent_text(record: dict[str, Any]) -> str:
        return "\n\n".join(span["text"] for span in record.get("source_spans", []))

    def clipped_source_spans(self, record: dict[str, Any]) -> list[dict[str, Any]]:
        start = int(record.get("parent_start_offset", 0))
        end = int(record.get("parent_end_offset", 0))
        if start < 0 or end <= start:
            raise RuntimeError(f"Invalid parent offsets for {record['retrieval_chunk_id']}: {start}:{end}")
        spans = record.get("source_spans") or []
        if not spans:
            raise RuntimeError(f"Missing source_spans for {record['retrieval_chunk_id']}")
        cursor = 0
        clipped: list[dict[str, Any]] = []
        for source_span in spans:
            source_text = source_span.get("text", "")
            a, b = cursor, cursor + len(source_text)
            overlap_start, overlap_end = max(start, a), min(end, b)
            if overlap_start < overlap_end:
                text = source_text[overlap_start - a:overlap_end - a]
                if not text:
                    raise RuntimeError(f"Empty clipped source span for {record['retrieval_chunk_id']}")
                if text not in source_text:
                    raise RuntimeError(f"Clipped source span is not source-exact for {record['retrieval_chunk_id']}")
                clipped.append({"page": int(source_span["page"]), "text": text})
            cursor = b + 2
        if not clipped:
            raise RuntimeError(f"Offsets do not intersect source_spans for {record['retrieval_chunk_id']}")
        parent_text = self._parent_text(record)
        expected_body = parent_text[start:end]
        reconstructed = "\n\n".join(span["text"] for span in clipped)
        # Leading/trailing separators can be selected by an exact character range;
        # source text itself remains exact, so only separator whitespace is ignored here.
        if reconstructed.strip() != expected_body.strip():
            raise RuntimeError(f"Clipped spans do not reconstruct body for {record['retrieval_chunk_id']}")
        return clipped


class ContextBuilderV2:
    """Turn Phase 4C results into bounded evidence and citations."""

    EXPAND_TYPES = {"procedure", "faq", "table", "financial_product", "investment_opportunity", "industrial_zone"}

    def __init__(self, store: ProvenanceStore | None = None, max_evidence_units: int = 6,
                 max_context_characters: int = 12000, expand_siblings: bool = True):
        self.store = store or ProvenanceStore()
        self.max_evidence_units = max_evidence_units
        self.max_context_characters = max_context_characters
        self.expand_siblings = expand_siblings

    @staticmethod
    def _check_identity(result: dict[str, Any], source: dict[str, Any]) -> None:
        for field in ("parent_semantic_chunk_id", "document_id", "document_family_id", "language"):
            if result.get(field) is not None and result.get(field) != source.get(field):
                raise RuntimeError(f"Provenance mismatch for {result.get('retrieval_chunk_id')}: {field}")

    def _evidence(self, result: dict[str, Any], evidence_id: str, expanded: bool = False) -> dict[str, Any]:
        rid = result.get("retrieval_chunk_id")
        if not rid:
            raise RuntimeError("Retriever result has no retrieval_chunk_id")
        source = self.store.get(rid)
        self._check_identity(result, source)
        clipped = self.store.clipped_source_spans(source)
        pages = sorted(dict.fromkeys(span["page"] for span in clipped))
        source_pages = set(source.get("source_pages") or [])
        if not set(pages).issubset(source_pages):
            raise RuntimeError(f"Citation pages escape source_pages for {rid}")
        return {
            "evidence_id": evidence_id,
            "retrieval_chunk_id": rid,
            "parent_semantic_chunk_id": source["parent_semantic_chunk_id"],
            "document_id": source["document_id"],
            "document_family_id": source["document_family_id"],
            "filename": source["filename"],
            "document_title": source["document_title"],
            "language": source["language"],
            "topic_id": source["topic_id"],
            "content_type": source["content_type"],
            "semantic_tags": source.get("semantic_tags", []),
            "heading_path": source.get("heading_path", []),
            "page_start": pages[0],
            "page_end": pages[-1],
            "source_pages": pages,
            "text": source["text"],
            "source_spans": clipped,
            "dense_score": result.get("dense_score"),
            "ranking_score": result.get("ranking_score"),
            "expanded_from_sibling": expanded,
            "retrieval_chunk_index": source.get("retrieval_chunk_index"),
            "retrieval_chunk_count": source.get("retrieval_chunk_count"),
            "temporal_scope": source.get("temporal_scope"),
        }

    def _sibling_candidates(self, result: dict[str, Any]) -> list[dict[str, Any]]:
        source = self.store.get(result["retrieval_chunk_id"])
        if not self.expand_siblings or source.get("content_type") not in self.EXPAND_TYPES:
            return []
        children = self.store.by_parent[source["parent_semantic_chunk_id"]]
        index = int(source.get("retrieval_chunk_index", 0))
        adjacent = [child for child in children if abs(int(child.get("retrieval_chunk_index", 0)) - index) == 1]
        # One sibling is enough to restore a continuation without flooding context.
        adjacent.sort(key=lambda child: (int(child.get("retrieval_chunk_index", 0)) < index, child["retrieval_chunk_id"]))
        return adjacent[:1]

    def build(self, retrieval_results: Any, query: str = "", query_language: str | None = None) -> dict[str, Any]:
        if isinstance(retrieval_results, dict):
            retrieval_results = retrieval_results.get("results", [])
        selected = list(retrieval_results or [])
        evidence: list[dict[str, Any]] = []
        duplicate_count = 0
        primary_received = len(selected)
        primary_dropped_budget = 0
        primary_dropped_capacity = 0
        primary_ids: list[str] = []
        primary_kept_ids: list[str] = []
        total = 0

        # Stage A is deliberately separate: selected Phase-4C evidence always
        # gets priority over optional context expansion.
        for result in selected:
            if len(evidence) >= self.max_evidence_units:
                primary_dropped_capacity += 1
                continue
            item = self._evidence(result, f"E{len(evidence) + 1}", False)
            rendered = self._render_evidence(item)
            primary_ids.append(item["retrieval_chunk_id"])
            if total and total + len(rendered) > self.max_context_characters:
                primary_dropped_budget += 1
                continue
            if not total and len(rendered) > self.max_context_characters:
                raise RuntimeError(f"Single evidence unit exceeds context budget: {item['retrieval_chunk_id']}")
            evidence.append(item)
            primary_kept_ids.append(item["retrieval_chunk_id"])
            total += len(rendered)

        selected_ids = set(primary_ids)
        seen_primary_text = {_normalize(self.store.get(rid).get("text", "")) for rid in primary_ids}
        seen_sibling_text: set[str] = set()
        siblings_considered = 0
        siblings_added = 0
        siblings_skipped_capacity = 0
        siblings_skipped_budget = 0
        siblings_skipped_nonindexable = 0
        sibling_ids: list[str] = []

        # Stage B uses only remaining capacity/budget. A sibling can never
        # displace a primary result admitted above.
        if evidence:
            for result in selected:
                for sibling in self._sibling_candidates(result):
                    siblings_considered += 1
                    sibling_id = sibling["retrieval_chunk_id"]
                    sibling_source = self.store.get(sibling_id)
                    if not sibling_source.get("indexable", False):
                        siblings_skipped_nonindexable += 1
                        continue
                    if sibling_id in selected_ids or sibling_id in sibling_ids:
                        duplicate_count += 1
                        continue
                    if len(evidence) >= self.max_evidence_units:
                        siblings_skipped_capacity += 1
                        continue
                    norm = _normalize(sibling_source.get("text", ""))
                    if not norm or norm in seen_primary_text or norm in seen_sibling_text:
                        duplicate_count += 1
                        continue
                    sibling_result = {
                        **sibling,
                        "dense_score": result.get("dense_score"),
                        "ranking_score": result.get("ranking_score"),
                    }
                    item = self._evidence(sibling_result, f"E{len(evidence) + 1}", True)
                    rendered = self._render_evidence(item)
                    if total + len(rendered) > self.max_context_characters:
                        siblings_skipped_budget += 1
                        continue
                    evidence.append(item)
                    sibling_ids.append(sibling_id)
                    seen_sibling_text.add(norm)
                    siblings_added += 1
                    total += len(rendered)

        kept = evidence
        for index, item in enumerate(kept, 1):
            item["evidence_id"] = f"E{index}"
        citations = [self._citation(item, f"C{index}") for index, item in enumerate(kept, 1)]
        context = "\n\n".join(self._render_evidence(item) for item in kept)
        return {
            "query": query,
            "query_language": query_language,
            "context_text": context,
            "evidence": kept,
            "citations": citations,
            "diagnostics": {
                "retrieved_results": len(selected),
                "final_evidence_units": len(kept),
                "primary_results_received": primary_received,
                "primary_results_kept": len(primary_kept_ids),
                "primary_results_dropped_budget": primary_dropped_budget,
                "primary_results_dropped_capacity": primary_dropped_capacity,
                "primary_retrieval_chunk_ids": primary_ids,
                "primary_ids_preserved": primary_kept_ids,
                "optional_sibling_ids_added": sibling_ids,
                "siblings_considered": siblings_considered,
                "siblings_added": siblings_added,
                "siblings_skipped_capacity": siblings_skipped_capacity,
                "siblings_skipped_budget": siblings_skipped_budget,
                "siblings_skipped_nonindexable": siblings_skipped_nonindexable,
                "duplicates_removed": duplicate_count,
                "context_characters": len(context),
                "context_budget": self.max_context_characters,
                "provenance_validation": "PASS",
            },
        }

    @staticmethod
    def _render_evidence(item: dict[str, Any]) -> str:
        heading = " > ".join(item.get("heading_path") or [])
        topic = item.get("topic_id") or ""
        return (f"[{item['evidence_id']}]\n"
                f"Document: {item['document_title']}\n"
                f"Language: {item['language']}\n"
                f"Pages: {page_label(item['source_pages'])}\n"
                f"Topic: {topic}\n"
                f"Heading: {heading}\n"
                f"Content:\n{item['text']}")

    @staticmethod
    def _citation(item: dict[str, Any], citation_id: str) -> dict[str, Any]:
        return {
            "citation_id": citation_id,
            "evidence_id": item["evidence_id"],
            "retrieval_chunk_id": item["retrieval_chunk_id"],
            "document_id": item["document_id"],
            "document_family_id": item["document_family_id"],
            "filename": item["filename"],
            "document_title": item["document_title"],
            "language": item["language"],
            "page_start": item["page_start"],
            "page_end": item["page_end"],
            "source_pages": item["source_pages"],
            "source_spans": item["source_spans"],
        }


def render_citation(citation: dict[str, Any]) -> str:
    return f"[{citation['citation_id']}] {citation['document_title']}, {page_label(citation['source_pages'])}"
