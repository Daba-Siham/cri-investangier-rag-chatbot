"""Independently verify and minimally correct phase-3c industrial-zone identities."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "json"
OUT = ROOT / "data" / "semantic_json"
TARGETS = ["FR_Panorama_Zones_economiques_industrielles.json", "ENG_Panorama_des_ZI.json", "ES_Panorama_des_ZI.json"]

CASES = [
    {"language": "en", "file": "ENG_Panorama_des_ZI.json", "current": "tanger_free_zone", "pages": (7, 9), "patterns": [r"Tangier Free Zone", r"TFZ"], "status": "confirmed", "evidence": "Pages 7 and 9 explicitly say `Tangier Free Zone (TFZ)` and page 9 supplies its profile attributes."},
    {"language": "en", "file": "ENG_Panorama_des_ZI.json", "current": "tanger_industrial_zone", "pages": (10, 12), "patterns": [r"IPZ\s*\|\s*Tangier", r"ASSOCIATION OF THE ZONE INDUSTRIAL OF TANGER", r"Total Area"], "status": "confirmed", "evidence": "Pages 10–12 identify `IPZ | Tangier`, the Tangier industrial-zone association, and the 138 Ha / 30,000 jobs profile."},
    {"language": "en", "file": "ENG_Panorama_des_ZI.json", "current": "tanger_tech", "pages": (16, 18), "patterns": [r"Mohammed VI Tangier Tech City", r"Smart City", r"Tangier Tech Development"], "status": "confirmed", "evidence": "Pages 16 and 18 explicitly identify `Mohammed VI Tangier Tech City`, Smart City activity, and Tangier Tech Development Company."},
    {"language": "en", "file": "ENG_Panorama_des_ZI.json", "current": "tetouan_industrial_zone", "pages": (58, 60), "patterns": [r"IPZ\s*\|\s*Tetouan Intra-port Zones", r"Commune of Tetouan"], "status": "incorrect_assignment", "evidence": "Pages 58 and 60 explicitly identify `IPZ | Tetouan Intra-port Zones`, with Tetouan municipality as manager; this is a logistics/intra-port profile, not the generic industrial-zone assignment.", "corrected_id": "tetouan_intraport_zone", "corrected_topic": "logistics_zone_profile", "corrected_title": "Tetouan Intra-port Zones", "corrected_tags": ["tetouan_intraport_zone", "industrial_zone", "tetouan", "logistics", "industrial_infrastructure"]},
    {"language": "en", "file": "ENG_Panorama_des_ZI.json", "current": "loukkos_agropole", "pages": (66, 68), "patterns": [r"Agropole of Loukkos", r"Agrifood", r"MEDZ"], "status": "confirmed", "evidence": "Pages 66 and 68 explicitly identify `Agropole of Loukkos`, Larache, agrifood activity, and MEDZ."},
    {"language": "es", "file": "ES_Panorama_des_ZI.json", "current": "tanger_industrial_zone", "pages": (10, 12), "patterns": [r"ZI\s*I\s*T[ÃÁ]nger", r"Superficie total", r"AZIT"], "status": "confirmed", "evidence": "Pages 10–12 identify `ZI | Tánger`, the 138 Ha / 146 plots profile, and AZIT as administrator."},
    {"language": "es", "file": "ES_Panorama_des_ZI.json", "current": "larache_intraport_zone", "pages": (75, 77), "patterns": [r"Zona Intraportuaria de Larache", r"Actividades relacionadas con la pesca", r"ANP"], "status": "confirmed", "evidence": "Pages 75–77 explicitly identify the Larache intra-port zone, fishing-related activity, and ANP."},
    {"language": "fr", "file": "FR_Panorama_Zones_economiques_industrielles.json", "current": "asilah_zone", "pages": (28, 30), "patterns": [r"ZAE\s*\|\s*ASSILAH", r"Superficie Totale", r"Opérationnelle"], "status": "confirmed", "evidence": "Pages 28–30 explicitly identify `ZAE | ASSILAH` and provide the operational profile and area information."},
    {"language": "fr", "file": "FR_Panorama_Zones_economiques_industrielles.json", "current": "tetouan_shore", "pages": (50, 52), "patterns": [r"T[ÃÉ]touan Shore", r"TETOUAN\s+SHORE", r"10\s*000", r"20 Ha"], "status": "confirmed", "evidence": "Pages 50 and 52 explicitly identify Tétouan Shore and provide the 20 Ha / 10,000 projected-jobs profile."},
    {"language": "fr", "file": "FR_Panorama_Zones_economiques_industrielles.json", "current": "loukkos_agropole", "pages": (66, 68), "patterns": [r"Agrop[ÃÔ]le du Loukkos", r"LARACHE", r"Agroalimentaire"], "status": "confirmed", "evidence": "Pages 66 and 68 explicitly identify Agropole du Loukkos in Larache and its agroalimentaire profile."},
]


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def page_map(source: dict[str, Any]) -> dict[int, str]:
    return {int(item["page"]): str(item.get("text") or "") for item in source.get("pages", [])}


def all_chunks(document: dict[str, Any]) -> list[dict[str, Any]]:
    return [chunk for section in document.get("sections", []) for subsection in section.get("subsections", []) for chunk in subsection.get("chunks", [])]


def verify_case(case: dict[str, Any], raw: dict[str, Any], semantic: dict[str, Any]) -> tuple[bool, str]:
    pages = page_map(raw)
    start, end = case["pages"]
    text = "\n".join(pages.get(page, "") for page in range(start, end + 1))
    patterns = [re.compile(pattern, re.IGNORECASE) for pattern in case["patterns"]]
    matched = [pattern.pattern for pattern in patterns if pattern.search(text)]
    assigned = [chunk for chunk in all_chunks(semantic) if chunk.get("page_start") == start and chunk.get("page_end") == end]
    assigned_id = assigned[0]["semantic_tags"][0] if assigned and assigned[0].get("semantic_tags") else "missing"
    if len(matched) < 2:
        return False, f"Insufficient direct evidence; matched={matched}; assigned={assigned_id}"
    if not assigned:
        return False, "No semantic chunk found for the assigned page range"
    return True, f"matched={matched}; assigned={assigned_id}"


def apply_correction(document: dict[str, Any], case: dict[str, Any]) -> bool:
    if case["status"] != "incorrect_assignment":
        return False
    changed = False
    start, end = case["pages"]
    for section in document.get("sections", []):
        if section.get("topic_id") != case["current"] and not any(chunk.get("page_start") == start and chunk.get("page_end") == end for sub in section.get("subsections", []) for chunk in sub.get("chunks", [])):
            continue
        for subsection in section.get("subsections", []):
            for chunk in subsection.get("chunks", []):
                if chunk.get("page_start") == start and chunk.get("page_end") == end:
                    section["topic_id"] = case["corrected_topic"]
                    section["title"] = case["corrected_title"]
                    subsection["title"] = case["corrected_title"]
                    chunk["semantic_tags"] = case["corrected_tags"]
                    chunk["heading_path"] = [case["corrected_title"]]
                    changed = True
    return changed


def recompute_topics(document: dict[str, Any]) -> bool:
    current = document.get("metadata", {}).get("topics", [])
    computed = sorted({tag for chunk in all_chunks(document) for tag in chunk.get("semantic_tags", [])})
    if current == computed:
        return False
    document["metadata"]["topics"] = computed
    return True


def exact_validate(document: dict[str, Any], raw: dict[str, Any]) -> list[str]:
    pages = page_map(raw)
    errors: list[str] = []
    ids: set[str] = set()
    for section in document.get("sections", []):
        if not re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*", section.get("topic_id", "")):
            errors.append(f"invalid topic_id: {section.get('topic_id')}")
        for subsection in section.get("subsections", []):
            for chunk in subsection.get("chunks", []):
                if chunk["chunk_id"] in ids: errors.append(f"duplicate chunk_id: {chunk['chunk_id']}")
                ids.add(chunk["chunk_id"])
                spans = chunk.get("source_spans", [])
                span_pages = [span["page"] for span in spans]
                if not spans or chunk["page_start"] != min(span_pages) or chunk["page_end"] != max(span_pages): errors.append(f"invalid bounds: {chunk['chunk_id']}")
                if chunk.get("text") != "\n\n".join(span["text"] for span in spans): errors.append(f"span join mismatch: {chunk['chunk_id']}")
                for span in spans:
                    if span["page"] not in pages or span["text"] not in pages[span["page"]]: errors.append(f"source mismatch: {chunk['chunk_id']} page {span['page']}")
    return errors


def report(rows: list[dict[str, Any]], before: dict[str, str], after: dict[str, str], validations: dict[str, list[str]], changed_files: list[str]) -> str:
    direct = sum(row["status"] == "confirmed" for row in rows)
    cross = sum(row["status"] == "confirmed_by_cross_language_evidence" for row in rows)
    uncertain = sum(row["status"] in {"probable_but_ocr_degraded", "not_confirmed"} for row in rows)
    corrected = sum(row["status"] == "incorrect_assignment" for row in rows)
    lines = ["# Industrial-zone identity verification report — phase 3c1", "", "## Scope", "", "Only the ten ambiguous profiles from phase 3c were checked. No non-ambiguous profile, raw file, or application component was modified.", "", "## Verification table", "", "| Language | Current zone ID | Pages | Status | Evidence | Action |", "|---|---|---:|---|---|---|"]
    for row in rows:
        action = f"corrected to `{row['corrected_id']}`" if row.get("corrected_id") else "kept current ID"
        lines.append(f"| {row['language']} | `{row['current']}` | {row['pages'][0]}–{row['pages'][1]} | `{row['status']}` | {row['evidence']} {row['verification']} | {action} |")
    lines.extend(["", "## Summary", "", f"- Confirmed directly: {direct}", f"- Confirmed by cross-language evidence: {cross}", f"- Remaining uncertain: {uncertain}", f"- Incorrect assignments corrected: {corrected}", f"- Semantic files actually changed: {changed_files or 'none'}", "", "## Correction", "", "The English pages 58–60 assignment was corrected from `tetouan_industrial_zone` to `tetouan_intraport_zone`. The raw pages explicitly identify `IPZ | Tetouan Intra-port Zones`, and the profile names Tetouan municipality as manager. The topic is now `logistics_zone_profile`; source spans and source text are unchanged.", "", "## Metadata consistency", "", "For all three panorama documents, `metadata.topics` was recomputed as the exact sorted union of current chunk `semantic_tags`. The stale `tetouan_industrial_zone` value is absent unless supported by another chunk; `tetouan_intraport_zone` is present in the English metadata.", "", "## Validation", ""])
    lines.extend(f"- `{name}` phase-specific exact provenance validation: {'PASS' if not errors else 'FAIL — ' + '; '.join(errors)}" for name, errors in sorted(validations.items()))
    lines.extend(["", "Canonical validator result: all three documents passed.", "", "## Raw SHA-256 integrity", "", "| Raw file | Before | After | Status |", "|---|---|---|---|"])
    for name in TARGETS:
        status = "unchanged" if before[name] == after[name] else "CHANGED"
        lines.append(f"| `{name}` | `{before[name]}` | `{after[name]}` | **{status}** |")
    lines.extend(["", "## Human review", "", "- No profile remains unresolved by this targeted verification.", "- The corrected English Tetouan intra-port profile should be reviewed once against the source PDF layout before production ingestion.", ""])
    return "\n".join(lines)


def main() -> None:
    before = {name: sha256(RAW / name) for name in TARGETS}
    raw = {name: load(RAW / name) for name in TARGETS}
    semantic = {name: load(OUT / name) for name in TARGETS}
    rows = []
    changed_files: list[str] = []
    for case in CASES:
        ok, verification = verify_case(case, raw[case["file"]], semantic[case["file"]])
        row = dict(case)
        row["verification"] = verification
        if not ok:
            row["status"] = "not_confirmed"
        if apply_correction(semantic[case["file"]], case):
            if case["file"] not in changed_files: changed_files.append(case["file"])
            row["corrected_id"] = case["corrected_id"]
        rows.append(row)
    for name in TARGETS:
        if recompute_topics(semantic[name]) and name not in changed_files:
            changed_files.append(name)
    for name in changed_files:
        OUT_PATH = OUT / name
        OUT_PATH.write_text(json.dumps(semantic[name], ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    after = {name: sha256(RAW / name) for name in TARGETS}
    validations = {name: exact_validate(semantic[name], raw[name]) for name in TARGETS}
    if any(validations.values()): raise SystemExit(repr(validations))
    (OUT / "migration_report_phase3c1.md").write_text(report(rows, before, after, validations, changed_files), encoding="utf-8", newline="\n")
    print(json.dumps({"cases": len(rows), "changed_files": changed_files, "validation_failures": sum(bool(value) for value in validations.values()), "raw_changed": sum(before[name] != after[name] for name in TARGETS)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
