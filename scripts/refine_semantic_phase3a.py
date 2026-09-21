"""Align canonical concepts for the two multilingual statistical families."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "json"
OUT = ROOT / "data" / "semantic_json"

KEY_2025 = [
    "regional_investment_overview",
    "business_creation",
    "business_creation",
    "crui_activity",
    "crui_activity",
    "crui_activity",
    "sector_investment",
    "sector_investment",
    "sector_investment",
    "business_support",
    "business_support",
    "business_support",
    "business_support",
    "territorial_promotion",
    "territorial_promotion",
    "territorial_promotion",
    "territorial_promotion",
    "closing_message",
]

KEY_2025_TAGS = [
    ["regional_investment_overview"],
    ["business_creation"],
    ["business_creation", "sector_distribution"],
    ["crui_activity"],
    ["crui_activity", "approved_projects", "investment_amount", "projected_jobs"],
    ["crui_activity", "sector_distribution"],
    ["sector_investment", "industrial_investment"],
    ["sector_investment", "tourism_investment"],
    ["sector_investment", "energy_investment"],
    ["business_support"],
    ["business_support", "piafe"],
    ["business_support", "conciliation"],
    ["business_support", "open_innovation"],
    ["territorial_promotion"],
    ["territorial_promotion", "mre_support"],
    ["territorial_promotion", "tpme_support"],
    ["territorial_promotion", "strategic_partnership"],
    ["closing_message"],
]

CRUI_TOPICS = [
    "crui_activity",
    "projects_reviewed",
    "sector_distribution",
    "industrial_investment",
    "crui_activity",
    "approved_projects",
    "closing_message",
]

CRUI_TAGS = [
    ["crui_activity"],
    ["projects_reviewed"],
    ["sector_distribution", "investment_amount"],
    ["sector_distribution", "industrial_investment", "investment_amount", "projected_jobs"],
    ["crui_activity"],
    ["approved_projects", "investment_amount", "projected_jobs"],
    ["closing_message"],
]

TARGETS_2025 = {
    "FR_Chiffres_cles_annee_2025.json",
    "Eng_Chiffres_cles_annee_2025.json",
    "ESP_Chiffres_cles_annee_2025.json",
    "Arabe_Chiffres_cles_2025.json",
}
TARGETS_CRUI = {
    "Chiffres_cles_CRUI_1er_semestre_2024_Francais.json",
    "Chiffres_cles_CRUI_1er_semestre_2024_Anglais.json",
    "Chiffres_cles_CRUI_1er_semestre_2024_Espagnol.json",
    "Chiffres_cles_CRUI_1er_semestre_2024_Arabe.json",
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def chunks(document: dict[str, Any]) -> list[dict[str, Any]]:
    return [chunk for section in document["sections"] for subsection in section["subsections"] for chunk in subsection["chunks"]]


def source_title(chunk: dict[str, Any]) -> str:
    path = chunk.get("heading_path") or []
    return path[-1] if path else "Semantic unit"


def one_chunk_section(document: dict[str, Any], chunk: dict[str, Any], index: int, topic_id: str) -> dict[str, Any]:
    title = source_title(chunk)
    chunk["heading_path"] = [title]
    return {
        "section_id": f"{document['document_id']}_section_{index:02d}",
        "title": title,
        "topic_id": topic_id,
        "subsections": [{
            "subsection_id": f"{document['document_id']}_subsection_{index:02d}",
            "title": title,
            "chunks": [chunk],
        }],
    }


def refine_2025(document: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(document)
    result["schema_version"] = "2.2"
    all_chunks = chunks(result)
    if len(all_chunks) != len(KEY_2025):
        raise ValueError(f"2025 chunk count mismatch for {document['document_id']}: {len(all_chunks)}")
    if document["document_id"] == "fr_chiffres_cles_annee_2025":
        section_specs = [
            ("Dynamique d’investissement 2025", "regional_investment_overview", 1),
            ("Création d’entreprises", "business_creation", 2),
            ("Bilan de la CRUI", "crui_activity", 3),
            ("Dynamique des investissements sectoriels", "sector_investment", 3),
            ("Accompagnement des entreprises et entrepreneuriat", "business_support", 4),
            ("Promotion et partenariats", "territorial_promotion", 4),
            ("Message de clôture", "closing_message", 1),
        ]
        sections = []
        offset = 0
        for chunk, tags in zip(all_chunks, KEY_2025_TAGS):
            chunk["semantic_tags"] = tags
        for index, (title, topic_id, count) in enumerate(section_specs, 1):
            selected = all_chunks[offset:offset + count]
            offset += count
            for chunk in selected:
                chunk["heading_path"] = [title, source_title(chunk)]
            sections.append({
                "section_id": f"{document['document_id']}_sec_{index:02d}",
                "title": title,
                "topic_id": topic_id,
                "subsections": [{
                    "subsection_id": f"{document['document_id']}_sub_{index:02d}",
                    "title": title,
                    "chunks": selected,
                }],
            })
        result["sections"] = sections
        result["metadata"]["topics"] = sorted({tag for tags in KEY_2025_TAGS for tag in tags})
        result["metadata"]["publication_year"] = 2025
        result["metadata"]["reference_period"] = {"year": 2025, "type": "year", "semester": None, "quarter": None, "label": "2025", "start_date": None, "end_date": None}
        return result
    sections = []
    for index, (chunk, topic_id, tags) in enumerate(zip(all_chunks, KEY_2025, KEY_2025_TAGS), 1):
        chunk["semantic_tags"] = tags
        sections.append(one_chunk_section(result, chunk, index, topic_id))
    result["sections"] = sections
    result["metadata"]["topics"] = sorted({tag for tags in KEY_2025_TAGS for tag in tags})
    result["metadata"]["publication_year"] = 2025
    result["metadata"]["reference_period"] = {"year": 2025, "type": "year", "semester": None, "quarter": None, "label": "2025", "start_date": None, "end_date": None}
    return result


def refine_crui(document: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(document)
    result["schema_version"] = "2.2"
    all_chunks = chunks(result)
    if len(all_chunks) != len(CRUI_TOPICS):
        raise ValueError(f"CRUI chunk count mismatch for {document['document_id']}: {len(all_chunks)}")
    sections = []
    for index, (chunk, topic_id, tags) in enumerate(zip(all_chunks, CRUI_TOPICS, CRUI_TAGS), 1):
        chunk["semantic_tags"] = tags
        temporal = chunk.get("temporal_scope", {})
        years = temporal.get("years_mentioned", [])
        chunk["temporal_scope"] = {
            "primary_year": 2024,
            "years_mentioned": years,
            "reference_period": {
                "type": "semester", "year": 2024, "semester": 1,
                "quarter": None, "start_date": None, "end_date": None,
            },
        }
        sections.append(one_chunk_section(result, chunk, index, topic_id))
    result["sections"] = sections
    result["metadata"]["publication_year"] = None
    result["metadata"]["reference_period"] = {
        "year": 2024, "type": "semester", "semester": 1, "quarter": None,
        "label": {"fr": "1er semestre 2024", "en": "First semester 2024", "es": "Primer semestre de 2024", "ar": "النصف الأول من سنة 2024"}.get(result["metadata"]["language"], "2024 S1"),
        "start_date": None, "end_date": None,
    }
    result["metadata"]["topics"] = sorted({tag for tags in CRUI_TAGS for tag in tags})
    return result


def validate_exact(document: dict[str, Any], raw: dict[str, Any]) -> list[str]:
    source_pages = {int(page["page"]): str(page.get("text") or "") for page in raw.get("pages", [])}
    errors = []
    ids = set()
    for section in document.get("sections", []):
        topic = section.get("topic_id", "")
        if not topic or topic.startswith(document["document_id"]):
            errors.append(f"invalid topic_id: {topic}")
        for subsection in section.get("subsections", []):
            for chunk in subsection.get("chunks", []):
                cid = chunk["chunk_id"]
                if cid in ids:
                    errors.append(f"duplicate chunk_id: {cid}")
                ids.add(cid)
                spans = chunk["source_spans"]
                pages = [span["page"] for span in spans]
                if chunk["page_start"] != min(pages) or chunk["page_end"] != max(pages):
                    errors.append(f"page bounds: {cid}")
                if chunk["text"] != "\n\n".join(span["text"] for span in spans):
                    errors.append(f"span join: {cid}")
                for span in spans:
                    if span["page"] not in source_pages or span["text"] not in source_pages[span["page"]]:
                        errors.append(f"source mismatch: {cid} page {span['page']}")
    return errors


def report(before: dict[str, str], after: dict[str, str], documents: dict[str, dict[str, Any]], validation: dict[str, list[str]]) -> str:
    lines = ["# Semantic quality refinement report — phase 3a", "", "## Scope", "", "Only the `chiffres_cles_2025` and `crui_key_figures_2024_h1` families were modified. Schema version remains `2.2`. Raw JSON files and all other semantic families were not modified.", "", "## Documents modified", ""]
    lines.extend(f"- `{name}` — `{doc['document_id']}` — family `{doc['document_family_id']}` — {sum(1 for _ in chunks(doc))} chunks" for name, doc in sorted(documents.items()))
    lines.extend(["", "## Canonical concepts aligned", "", "2025 key figures: `regional_investment_overview`, `business_creation`, `crui_activity`, `sector_investment`, `industrial_investment`, `tourism_investment`, `energy_investment`, `business_support`, `piafe`, `conciliation`, `open_innovation`, `territorial_promotion`, `mre_support`, `tpme_support`, `strategic_partnership`, `closing_message`.", "", "CRUI H1 2024: `crui_activity`, `projects_reviewed`, `sector_distribution`, `industrial_investment`, `investment_amount`, `approved_projects`, `projected_jobs`, `closing_message`.", "", "## Topic ID and semantic-tag changes", "", "The translated 2025 documents were changed from one generic `regional_statistics` section to one source-language section per aligned semantic unit. The CRUI translations were changed from one generic `regional_statistics` section to aligned page-level semantic units. Human-readable titles and original chunk text remain in each source language.", "", "The French 2025 document retained its reviewed semantic section structure; its chunk tags were normalized to the same canonical vocabulary.", "", "## Temporal and metadata corrections", "", "- All four CRUI documents now have document-level `reference_period.type = semester`, `year = 2024`, and `semester = 1`.", "- All CRUI chunks now carry the same H1 2024 semester scope while preserving explicit years mentioned in their source text.", "- CRUI `publication_year` is `null`; the source supports a reference period, not an independently stated publication year.", "- All 2025 documents retain `publication_year = 2025` and a year-2025 reference period because the edition is explicitly identified as 2025.", "", "## Differences not safely aligned", "", "- Source layouts and wording differ across languages, so chunk counts and display headings were not copied across documents.", "- Historical years appearing inside CRUI pages remain in `years_mentioned`; they were not replaced with 2024.", "- The French reviewed document contains richer existing section-level distinctions than the translated automated outputs; alignment uses canonical IDs and tags without copying French text.", "", "## Validation", ""])
    lines.extend(f"- `{name}`: {'PASS' if not errors else 'FAIL — ' + '; '.join(errors)}" for name, errors in sorted(validation.items()))
    lines.extend(["", "## Raw-file integrity", "", "| Raw file | Before SHA-256 | After SHA-256 | Status |", "|---|---|---|---|"])
    for name in sorted(before):
        status = "unchanged" if before[name] == after[name] else "CHANGED"
        lines.append(f"| `{name}` | `{before[name]}` | `{after[name]}` | **{status}** |")
    lines.extend(["", "All eight target documents retain exact source spans and page provenance. No raw JSON file was written.", ""])
    return "\n".join(lines)


def main() -> None:
    names = sorted(TARGETS_2025 | TARGETS_CRUI)
    raw_hashes_before = {name: sha256(RAW / name) for name in names}
    raw = {name: load(RAW / name) for name in names}
    documents = {}
    for name in names:
        current = load(OUT / name)
        documents[name] = refine_2025(current) if name in TARGETS_2025 else refine_crui(current)
    for name, document in documents.items():
        errors = validate_exact(document, raw[name])
        if errors:
            raise SystemExit(f"Validation failed before writing {name}: {errors}")
        write(OUT / name, document)
    raw_hashes_after = {name: sha256(RAW / name) for name in names}
    validation = {name: validate_exact(document, raw[name]) for name, document in documents.items()}
    if any(validation.values()):
        raise SystemExit(repr(validation))
    (OUT / "migration_report_phase3a.md").write_text(report(raw_hashes_before, raw_hashes_after, documents, validation), encoding="utf-8", newline="\n")
    print(json.dumps({"documents_modified": len(documents), "validation_failures": sum(bool(value) for value in validation.values()), "raw_changed": sum(raw_hashes_before[name] != raw_hashes_after[name] for name in names)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
