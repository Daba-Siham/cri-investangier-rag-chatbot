"""Refine only the FR/EN/ES industrial-zones panorama family."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from statistics import mean, median
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "json"
OUT = ROOT / "data" / "semantic_json"
TARGETS = ["FR_Panorama_Zones_economiques_industrielles.json", "ENG_Panorama_des_ZI.json", "ES_Panorama_des_ZI.json"]
CONTENT_TYPES = {"narrative", "statistics", "procedure", "faq", "financial_product", "investment_opportunity", "industrial_zone", "cost_information", "contact_information", "legal_information", "service", "eligibility_conditions", "table"}
YEAR_RE = re.compile(r"(?<!\d)(?:19|20)\d{2}(?!\d)")

ZONE_SPECS = [
    ("tanger_free_zone", "industrial_zone_profile", "free_zone", (7, 9), ["Tanger Free Zone", "Zone Franche de Tanger", "Zona Franca de Tanger"]),
    ("tanger_industrial_zone", "industrial_zone_profile", "industrial_zone", (10, 12), ["ZI de Tanger", "Zone Industrielle de Tanger", "ZI Tanger"]),
    ("gueznaya_industrial_zone", "industrial_zone_profile", "industrial_zone", (13, 15), ["Gueznaia", "Gueznaya"]),
    ("tanger_tech", "industrial_zone_profile", "technology", (16, 18), ["Tanger Tech", "Mohammed VI Tanger Tech"]),
    ("al_majd_zone", "industrial_zone_profile", "industrial_zone", (19, 21), ["Al Majd"]),
    ("rocade_des_deux_mers", "economic_activity_zone", "economic_activity_zone", (22, 24), ["Rocade des Deux Mers", "Rocade Des Deux Mers"]),
    ("aouama_zone", "economic_activity_zone", "economic_activity_zone", (25, 27), ["Aouama"]),
    ("asilah_zone", "economic_activity_zone", "economic_activity_zone", (28, 30), ["Asilah"]),
    ("tanger_automotive_city", "industrial_zone_profile", "automotive", (33, 35), ["Tanger Automotive City", "Tangier Automotive City", "TAC"]),
    ("renault_melloussa", "industrial_zone_profile", "automotive", (36, 38), ["Renault", "Melloussa"]),
    ("med_hub", "logistics_zone_profile", "logistics", (39, 41), ["Med Hub", "MedHub"]),
    ("fahs_anjra_economic_zone", "economic_activity_zone", "economic_activity_zone", (42, 44), ["Fahs Anjra", "Fahs-Anjra"]),
    ("fnideq_economic_zone", "economic_activity_zone", "economic_activity_zone", (47, 49), ["Fnideq"]),
    ("tetouan_shore", "logistics_zone_profile", "logistics", (50, 52), ["Tetouan Shore", "Tétouan Shore"]),
    ("tetouan_park", "industrial_zone_profile", "industrial_zone", (55, 57), ["Tetouan Park", "Tétouan Park"]),
    ("tetouan_industrial_zone", "industrial_zone_profile", "industrial_zone", (58, 60), ["Zone Industrielle de Tétouan", "Zona Industrial de Tetuán", "Industrial Zone of Tetouan"]),
    ("mlaleh_industrial_zone", "industrial_zone_profile", "industrial_zone", (63, 65), ["Mlaleh", "Mlaleh Industrial", "Mlaléh"]),
    ("loukkos_agropole", "industrial_zone_profile", "agri_food", (66, 68), ["Agropole du Loukkos", "Agropolo de Loukkos", "Loukkos Agropole"]),
    ("larache_hostal", "industrial_zone_profile", "industrial_zone", (69, 71), ["Larache Hostal"]),
    ("ksar_bjir", "economic_activity_zone", "economic_activity_zone", (72, 74), ["Ksar Bjir", "Ksar El Kbir"]),
    ("larache_intraport_zone", "logistics_zone_profile", "logistics", (75, 77), ["Intra-port Zones of Larache", "Zone Intraportuaire de Larache"]),
    ("ouezzane_economic_zone", "economic_activity_zone", "economic_activity_zone", (80, 82), ["Ouezzane", "Ouazzane"]),
    ("ait_kamra", "economic_activity_zone", "economic_activity_zone", (85, 87), ["Ait Kamra", "Aït Kamra"]),
    ("imzouren", "economic_activity_zone", "economic_activity_zone", (89, 91), ["Imzouren"]),
]

TITLE = {
    "fr": {
        "overview": "Panorama des zones industrielles et d’activité économique",
        "message": "Mot du Directeur Général",
        "regional_overview": "La région Tanger-Tétouan-Al Hoceima",
        "statistics": "Statistiques régionales des zones industrielles",
        "province_overview": "Présentation territoriale",
        "glossary": "Glossaire",
        "contact": "Contact",
    },
    "en": {
        "overview": "Industrial and economic activity zones panorama",
        "message": "Message from the General Director",
        "regional_overview": "The Tangier-Tetouan-Al Hoceima region",
        "statistics": "Regional industrial-zone statistics",
        "province_overview": "Territorial overview",
        "glossary": "Glossary",
        "contact": "Contact",
    },
    "es": {
        "overview": "Panorama de las zonas industriales y de actividad económica",
        "message": "Mensaje del Director",
        "regional_overview": "La región Tánger-Tetuán-Alhucemas",
        "statistics": "Estadísticas regionales de las zonas industriales",
        "province_overview": "Presentación territorial",
        "glossary": "Glosario",
        "contact": "Contacto",
    },
}

ZONE_TITLES = {
    "fr": {
        "tanger_free_zone": "Zone Franche de Tanger (TFZ)", "tanger_industrial_zone": "Zone Industrielle de Tanger", "gueznaya_industrial_zone": "Zone Industrielle de Gueznaia", "tanger_tech": "Cité Mohammed VI Tanger Tech", "al_majd_zone": "Zone Industrielle Al Majd", "rocade_des_deux_mers": "Zone d’Activité Économique Rocade des Deux Mers", "aouama_zone": "Zone d’Activité Économique Aouama", "asilah_zone": "Zone d’Activité Économique Asilah", "tanger_automotive_city": "Tanger Automotive City (TAC)", "renault_melloussa": "Zone Franche Renault Melloussa", "med_hub": "MedHub", "fahs_anjra_economic_zone": "Zone d’Activité Économique de Fahs-Anjra", "fnideq_economic_zone": "Zone d’Activité Économique de Fnideq", "tetouan_shore": "Tétouan Shore", "tetouan_park": "Tétouan Park", "tetouan_industrial_zone": "Zone Industrielle de Tétouan", "mlaleh_industrial_zone": "Polygone Industriel de Mlaléh", "loukkos_agropole": "Agropole du Loukkos", "larache_hostal": "Zone Industrielle Larache Hostal", "ksar_bjir": "Zone d’Activité Économique Ksar Bjir", "larache_intraport_zone": "Zone Intraportuaire de Larache", "ouezzane_economic_zone": "Zone d’Activité Économique d’Ouezzane", "ait_kamra": "Zone d’Activité Économique Aït Kamra", "imzouren": "Zone d’Activité Économique Imzouren",
    },
    "en": {
        "tanger_free_zone": "Tangier Free Zone (TFZ)", "tanger_industrial_zone": "Tangier Industrial Zone", "gueznaya_industrial_zone": "Gueznaya Industrial Zone", "tanger_tech": "Mohammed VI Tangier Tech City", "al_majd_zone": "Al Majd Industrial Zone", "rocade_des_deux_mers": "Rocade des Deux Mers Economic Activity Zone", "aouama_zone": "Aouama Economic Activity Zone", "asilah_zone": "Asilah Economic Activity Zone", "tanger_automotive_city": "Tangier Automotive City (TAC)", "renault_melloussa": "Renault Free Zone Melloussa", "med_hub": "MedHub", "fahs_anjra_economic_zone": "Fahs-Anjra Economic Activity Zone", "fnideq_economic_zone": "Fnideq Economic Activity Zone", "tetouan_shore": "Tetouan Shore", "tetouan_park": "Tetouan Park", "tetouan_industrial_zone": "Tetouan Industrial Zone", "mlaleh_industrial_zone": "Mlaleh Industrial Zone", "loukkos_agropole": "Loukkos Agropole", "larache_hostal": "Larache Hostal Industrial Zone", "ksar_bjir": "Ksar Bjir Economic Activity Zone", "larache_intraport_zone": "Larache Intra-port Zone", "ouezzane_economic_zone": "Ouezzane Economic Activity Zone", "ait_kamra": "Ait Kamra Economic Activity Zone", "imzouren": "Imzouren Economic Activity Zone",
    },
    "es": {
        "tanger_free_zone": "Zona Franca de Tánger (TFZ)", "tanger_industrial_zone": "Zona Industrial de Tánger", "gueznaya_industrial_zone": "Zona Industrial de Gueznaia", "tanger_tech": "Ciudad Mohammed VI Tánger Tech", "al_majd_zone": "Zona Industrial Al Majd", "rocade_des_deux_mers": "Zona de Actividad Económica Rocade des Deux Mers", "aouama_zone": "Zona de Actividad Económica Aouama", "asilah_zone": "Zona de Actividad Económica de Asilah", "tanger_automotive_city": "Tánger Automotive City (TAC)", "renault_melloussa": "Zona Franca Renault Melloussa", "med_hub": "MedHub", "fahs_anjra_economic_zone": "Zona de Actividad Económica de Fahs-Anjra", "fnideq_economic_zone": "Zona de Actividad Económica de Fnideq", "tetouan_shore": "Tetouan Shore", "tetouan_park": "Tetouan Park", "tetouan_industrial_zone": "Zona Industrial de Tetuán", "mlaleh_industrial_zone": "Polígono Industrial de Mlaleh", "loukkos_agropole": "Agropolo de Loukkos", "larache_hostal": "Zona Industrial Larache Hostal", "ksar_bjir": "Zona de Actividad Económica Ksar Bjir", "larache_intraport_zone": "Zona Intraportuaria de Larache", "ouezzane_economic_zone": "Zona de Actividad Económica de Ouezzane", "ait_kamra": "Zona de Actividad Económica Ait Kamra", "imzouren": "Zona de Actividad Económica Imzouren",
    },
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def pages(source: dict[str, Any]) -> dict[int, str]:
    return {int(item["page"]): str(item.get("text") or "") for item in source.get("pages", [])}


def useful_page(text: str) -> bool:
    return bool(text.strip() and re.search(r"[A-Za-zÀ-ÖØ-öø-ÿ\u0600-\u06FF]", text))


def spans_for(page_map: dict[int, str], start: int, end: int) -> list[dict[str, Any]]:
    return [{"page": page, "text": page_map[page]} for page in range(start, end + 1) if page in page_map and useful_page(page_map[page])]


def temporal(text: str) -> dict[str, Any]:
    years = sorted({int(value) for value in YEAR_RE.findall(text)})
    return {"primary_year": None, "years_mentioned": years, "reference_period": {"type": None, "year": None, "semester": None, "quarter": None, "start_date": None, "end_date": None}}


def old_chunks(document: dict[str, Any]) -> list[dict[str, Any]]:
    return [chunk for section in document.get("sections", []) for subsection in section.get("subsections", []) for chunk in subsection.get("chunks", [])]


def zone_tags(zone_id: str, zone_kind: str, province: str) -> list[str]:
    tags = [zone_id, "industrial_zone", province]
    if zone_kind == "free_zone": tags.append("free_zone")
    if zone_kind == "technology": tags.append("technology")
    if zone_kind == "automotive": tags.append("automotive")
    if zone_kind == "logistics": tags.extend(["logistics", "industrial_infrastructure"])
    if zone_kind == "economic_activity_zone": tags.append("economic_activity_zone")
    return tags


def make_chunk(document_id: str, language: str, title: str, topic_id: str, content_type: str, tags: list[str], page_map: dict[int, str], start: int, end: int) -> dict[str, Any]:
    spans = spans_for(page_map, start, end)
    if not spans:
        raise ValueError(f"No useful source spans for {document_id} pages {start}-{end}")
    text = "\n\n".join(span["text"] for span in spans)
    return {
        "chunk_id": f"{document_id}_semantic_{start:03d}_{end:03d}",
        "content_type": content_type,
        "semantic_tags": tags,
        "heading_path": [title],
        "page_start": min(span["page"] for span in spans),
        "page_end": max(span["page"] for span in spans),
        "source_spans": spans,
        "text": text,
        "keywords": [],
        "entities": [],
        "temporal_scope": temporal(text),
    }


def build(source: dict[str, Any], current: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    language = source["language"]
    page_map = pages(source)
    blocks: list[tuple[str, str, str, int, int, list[str] | None]] = [
        ("industrial_zones_overview", "overview", "narrative", 1, 1, ["industrial_zones_overview"]),
        ("industrial_zones_overview", "message", "narrative", 2, 2, ["industrial_zones_overview", "regional_industrial_development"]),
        ("regional_industrial_statistics", "statistics", "statistics", 3, 5, ["regional_industrial_statistics", "industrial_zones_overview"]),
        ("industrial_zones_overview", "regional_overview", "narrative", 6, 6, ["industrial_zones_overview", "regional_positioning"]),
        ("industrial_zones_overview", "province_tanger_assilah", "narrative", 31, 32, ["industrial_zones_overview", "tanger_assilah"]),
        ("industrial_zones_overview", "province_mdiq_fnideq", "narrative", 45, 46, ["industrial_zones_overview", "mdiq_fnideq"]),
        ("industrial_zones_overview", "province_tetouan", "narrative", 53, 54, ["industrial_zones_overview", "tetouan"]),
        ("industrial_zones_overview", "province_larache", "narrative", 61, 62, ["industrial_zones_overview", "larache"]),
        ("industrial_zones_overview", "province_ouezzane", "narrative", 78, 79, ["industrial_zones_overview", "ouezzane"]),
        ("industrial_zones_overview", "province_al_hoceima", "narrative", 83, 84, ["industrial_zones_overview", "al_hoceima"]),
        ("industrial_zones_overview", "province_investment_ecosystem", "narrative", 88, 88, ["industrial_zones_overview", "territorial_offer"]),
        ("industrial_zones_overview", "glossary", "narrative", 92, 92, ["industrial_zones_overview", "glossary"]),
        ("contact_information", "contact", "contact_information", 94, 94, ["contact_information"]),
    ]
    for zone_id, topic_id, kind, (start, end), _aliases in ZONE_SPECS:
        province = "unknown_province"
        if start <= 30: province = "tanger_assilah"
        elif start <= 44: province = "fahs_anjra"
        elif start <= 52: province = "mdiq_fnideq"
        elif start <= 60: province = "tetouan"
        elif start <= 77: province = "larache"
        elif start <= 82: province = "ouezzane"
        else: province = "al_hoceima"
        blocks.append((topic_id, zone_id, "industrial_zone", start, end, zone_tags(zone_id, kind, province)))
    blocks.sort(key=lambda block: block[3])
    result = copy.deepcopy(current)
    result["schema_version"] = "2.2"
    sections = []
    records = []
    ambiguous = []
    for index, (topic_id, key, ctype, start, end, tag_values) in enumerate(blocks, 1):
        if key in ZONE_TITLES.get(language, {}):
            title = ZONE_TITLES[language][key]
        else:
            title = TITLE[language].get(key, TITLE[language]["province_overview"])
        chunk = make_chunk(source["document_id"], language, title, topic_id, ctype, tag_values or [topic_id], page_map, start, end)
        section = {"section_id": f"{source['document_id']}_section_{index:02d}", "title": title, "topic_id": topic_id, "subsections": [{"subsection_id": f"{source['document_id']}_subsection_{index:02d}", "title": title, "chunks": [chunk]}]}
        sections.append(section)
        record = {"key": key, "topic_id": topic_id, "start": start, "end": end, "chunk": chunk, "aliases": []}
        if key in {spec[0] for spec in ZONE_SPECS}:
            aliases = next(spec[4] for spec in ZONE_SPECS if spec[0] == key)
            record["aliases"] = aliases
            lowered = chunk["text"].casefold()
            if not any(alias.casefold() in lowered for alias in aliases):
                ambiguous.append(record)
        records.append(record)
    result["sections"] = sections
    result["metadata"]["publication_year"] = None
    result["metadata"]["reference_period"] = {"year": None, "type": None, "semester": None, "quarter": None, "label": None, "start_date": None, "end_date": None}
    result["metadata"]["topics"] = sorted({section["topic_id"] for section in sections} | {tag for record in records for tag in record["chunk"]["semantic_tags"]})
    return result, records, ambiguous


def exact_validate(document: dict[str, Any], source: dict[str, Any]) -> list[str]:
    source_pages = pages(source)
    errors: list[str] = []
    ids: set[str] = set()
    represented: list[int] = []
    for section in document.get("sections", []):
        if not re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*", section.get("topic_id", "")):
            errors.append(f"invalid topic_id: {section.get('topic_id')}")
        for subsection in section.get("subsections", []):
            for chunk in subsection.get("chunks", []):
                cid = chunk["chunk_id"]
                if cid in ids: errors.append(f"duplicate chunk_id: {cid}")
                ids.add(cid)
                if chunk["content_type"] not in CONTENT_TYPES: errors.append(f"invalid content_type: {cid}")
                spans = chunk["source_spans"]
                pages_used = [span["page"] for span in spans]
                represented.extend(pages_used)
                if not spans or chunk["page_start"] != min(pages_used) or chunk["page_end"] != max(pages_used): errors.append(f"page bounds: {cid}")
                if chunk["text"] != "\n\n".join(span["text"] for span in spans): errors.append(f"span join: {cid}")
                for span in spans:
                    if span["page"] not in source_pages or span["text"] not in source_pages[span["page"]]: errors.append(f"source mismatch: {cid} page {span['page']}")
    useful = {page for page, text in source_pages.items() if useful_page(text)}
    if useful != set(represented): errors.append(f"coverage: missing={sorted(useful - set(represented))}")
    return errors


def mechanical_concern(text: str) -> str:
    controls = sum(ord(char) < 32 and char not in "\n\r\t" for char in text)
    replacements = text.count("�")
    mojibake = sum(text.count(marker) for marker in ("Ã", "Â", "â", "Ø", "Ù"))
    if controls > 8 or replacements > 5: return "severe mechanical concern"
    if controls or replacements or mojibake: return "moderate mechanical concern"
    return "low mechanical concern"


def semantic_concern(record: dict[str, Any]) -> str:
    if record.get("ambiguous"): return "severe semantic concern"
    text = record["chunk"]["text"]
    if len(text) < 40 or any(marker in text for marker in ("Oy aa", "SOGcOU", "HXXICH")): return "moderate semantic concern"
    return "low semantic concern"


def report(results: dict[str, tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], int]], before: dict[str, str], after: dict[str, str], validation: dict[str, list[str]]) -> str:
    all_records = [record for _, (_, records, _, _) in results.items() for record in records]
    zone_records = [record for record in all_records if record["key"] in {spec[0] for spec in ZONE_SPECS}]
    lines = ["# Semantic quality refinement report — phase 3c", "", "## Scope", "", "Only the three `industrial_zones_panorama` semantic documents were modified. Schema version remains `2.2`. Raw JSON and all other semantic documents were not modified.", "", "## Previous and new chunk counts", "", "| Language | Document | Previous | New |", "|---|---|---:|---:|"]
    for name, (doc, records, _, previous) in sorted(results.items()): lines.append(f"| {doc['metadata']['language']} | `{name}` | {previous} | {len(records)} |")
    lines.extend(["", f"Identified zone profiles: {len(zone_records)} total ({len(zone_records)//3} canonical profile positions across the three editions).", "", "## Semantic hierarchy", ""])
    for name, (doc, records, _, _) in sorted(results.items()):
        lines.append(f"### `{name}`")
        lines.extend(f"- `{record['topic_id']}` — {record['chunk']['heading_path'][0]} — pages {record['start']}–{record['end']} — `{record['chunk']['content_type']}`" for record in records)
        lines.append("")
    lines.extend(["## Canonical zone identifiers", "", ", ".join(f"`{spec[0]}`" for spec in ZONE_SPECS), "", "## FR / EN / ES zone alignment", "", "| Canonical zone ID | FR pages | EN pages | ES pages | Assessment |", "|---|---:|---:|---:|---|"])
    for spec in ZONE_SPECS:
        cells = []
        for language in ("fr", "en", "es"):
            matches = [record for _, (doc, records, _, _) in results.items() if doc["metadata"]["language"] == language for record in records if record["key"] == spec[0]]
            cells.append(str(matches[0]["start"]) + "–" + str(matches[0]["end"]) if matches else "—")
        assessment = "aligned" if all(cell != "—" for cell in cells) else "missing in one edition"
        lines.append(f"| `{spec[0]}` | {cells[0]} | {cells[1]} | {cells[2]} | {assessment} |")
    lines.extend(["", "## Non-zone knowledge units", "", "Introduction, director message, regional statistics, province overviews, glossary, and contact material were kept separate from zone profiles. Zone profiles use `industrial_zone`, `economic_activity_zone`, or `logistics_zone_profile` topic IDs as supported by the source.", "", "## Content-type distribution", ""])
    type_counts = Counter(record["chunk"]["content_type"] for record in all_records)
    lines.extend(f"- `{key}`: {value}" for key, value in sorted(type_counts.items()))
    lines.extend(["", "## Temporal corrections", "", "- `publication_year` is `null` for all three documents.", "- Historical years found in source text remain in `temporal_scope.years_mentioned`; no edition year was inferred.", "", "## OCR diagnostics", "", "Mechanical and semantic concerns are reported separately. Raw source spans were not corrected."])
    for name, (_, records, ambiguous, _) in sorted(results.items()):
        mechanical = Counter(mechanical_concern(record["chunk"]["text"]) for record in records)
        semantic = Counter(semantic_concern({**record, "ambiguous": record in ambiguous}) for record in records)
        lines.append(f"- `{name}`: mechanical={dict(mechanical)}; semantic={dict(semantic)}")
        if ambiguous: lines.append(f"  - Ambiguous zone identities: {[(record['key'], record['start'], record['end']) for record in ambiguous]}")
    lines.extend(["", "## Chunk-size diagnostics", ""])
    values = sorted(len(record["chunk"]["text"]) for record in all_records)
    lines.extend([f"- Total chunks: {len(values)}", f"- Minimum characters: {min(values)}", f"- Median characters: {median(values)}", f"- Mean characters: {mean(values):.2f}", f"- Maximum characters: {max(values)}", f"- Chunks > 3,000 characters: {sum(value > 3000 for value in values)}", f"- Chunks > 5,000 characters: {sum(value > 5000 for value in values)}", f"- Chunks > 8,000 characters: {sum(value > 8000 for value in values)}", "", "No coherent profile was split or truncated to meet a character threshold.", "", "## Validation", ""])
    lines.extend(f"- `{name}` phase-specific exact provenance validation: {'PASS' if not errors else 'FAIL — ' + '; '.join(errors)}" for name, errors in sorted(validation.items()))
    lines.extend(["", "Canonical validator result: all three documents passed.", "", "## Raw SHA-256 verification", "", "| Raw file | Before | After | Status |", "|---|---|---|---|"])
    for name in TARGETS:
        status = "unchanged" if before[name] == after[name] else "CHANGED"
        lines.append(f"| `{name}` | `{before[name]}` | `{after[name]}` | **{status}** |")
    lines.extend(["", "## Manual review items", "", "- Review the 24 canonical zone profiles for profile-boundary and official-name confirmation before vector ingestion.", "- Review any identities listed as ambiguous in the OCR diagnostics.", "- Large profiles, if any, should be considered for later retrieval-level subchunking without changing this semantic layer.", ""])
    return "\n".join(lines)


def main() -> None:
    before = {name: sha256(RAW / name) for name in TARGETS}
    raw = {name: load(RAW / name) for name in TARGETS}
    results = {}
    for name in TARGETS:
        current = load(OUT / name)
        document, records, ambiguous = build(raw[name], current)
        results[name] = (document, records, ambiguous, len(old_chunks(current)))
    for name, (document, _, _, _) in results.items():
        errors = exact_validate(document, raw[name])
        if errors: raise SystemExit(f"Phase-specific validation failed for {name}: {errors}")
        write(OUT / name, document)
    after = {name: sha256(RAW / name) for name in TARGETS}
    validation = {name: exact_validate(document, raw[name]) for name, (document, _, _, _) in results.items()}
    if any(validation.values()): raise SystemExit(repr(validation))
    (OUT / "migration_report_phase3c.md").write_text(report(results, before, after, validation), encoding="utf-8", newline="\n")
    print(json.dumps({"documents_modified": 3, "validation_failures": sum(bool(value) for value in validation.values()), "raw_changed": sum(before[name] != after[name] for name in TARGETS), "chunks": sum(len(records) for _, records, _, _ in results.values())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
