"""Legacy phase-1 semantic JSON migration helpers.

The active migration entry point is ``migrate_semantic_phase2_2.py``. This file
continues to provide shared loading/page helpers and delegates direct execution
to the schema-2.2 migration so it cannot regenerate an obsolete schema.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = PROJECT_ROOT / "data" / "raw" / "json" / "FR_Chiffres_cles_annee_2025.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "semantic_json"

FAMILY_INVENTORY = [
    ("cri_presentation", "CRI TTA presentation", "fr, en, es, ar", "presentation", "No explicit publication period identified from filenames/content."),
    ("crui_key_figures_2024_h1", "CRUI key figures, first semester 2024", "fr, en, es, ar", "statistics", "Reference period is the first semester of 2024."),
    ("chiffres_cles_2025", "2025 key figures", "fr, en, es, ar", "annual_key_figures", "Primary reference year is 2025; individual pages can mention other dates."),
    ("investment_climate_indicators", "Investment climate indicators", "fr, en, es", "business_climate_report", "No single publication year reliably identified from filenames/content."),
    ("industrial_zones_panorama", "Industrial/economic zones panorama", "fr, en, es", "industrial_zones_panorama", "No single publication year reliably identified from filenames/content."),
    ("manar_al_moustatmir_news_2023", "Manar Al Moustatmir News, issue 1", "fr, en, ar", "news_or_annual_review", "The three files have matching 2023 issue structure; family assignment is based on content/title correspondence."),
    ("conciliation_guide", "Conciliation guide", "ar, es", "guide", "Multilingual family inferred from matching guide title and structure."),
    ("investment_business_support_single_window", "Investment and business support single window", "fr, es", "service_guide", "Multilingual family inferred from matching title and structure."),
    ("investors_guide_territorial_opportunities", "Investors guide to territorial opportunities", "fr, en", "investors_guide", "Multilingual family inferred from matching title and subject."),
    ("financing_guide", "Guide du financement des entreprises", "fr", "financing_guide", "French-only guide; source content identifies 2022 in the opening material."),
    ("electricity_water_sanitation_connection", "Large-account utility connection guide", "fr", "procedure_guide", "French-only procedural guide."),
    ("integrated_business_support_financing", "Integrated business support and financing programme", "ar", "financial_product_or_programme", "Arabic-only programme document; no family counterpart identified."),
    ("production_factor_cost_guide_2024", "Cost of production factors", "fr", "cost_information_guide", "Reference/edition year is 2024."),
    ("logistics_sector_brochure", "Logistics sector brochure", "fr", "sector_brochure", "No single publication year reliably identified from filename/content."),
]


def load_source(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or not isinstance(document.get("pages"), list):
        raise ValueError("Source must contain a pages list")
    return document


def page_map(document: dict[str, Any]) -> dict[int, str]:
    return {int(page["page"]): str(page.get("text") or "") for page in document["pages"]}


def make_chunk(
    pages: dict[int, str],
    page_numbers: list[int],
    chunk_id: str,
    content_type: str,
    heading_path: list[str],
    keywords: list[str],
    entities: list[str],
) -> dict[str, Any]:
    missing = [page for page in page_numbers if page not in pages]
    if missing:
        raise ValueError(f"Missing source pages for {chunk_id}: {missing}")
    source_texts = [pages[page] for page in page_numbers]
    if not any(text.strip() for text in source_texts):
        raise ValueError(f"Chunk {chunk_id} contains no source text")
    return {
        "chunk_id": chunk_id,
        "content_type": content_type,
        "heading_path": heading_path,
        "page_start": min(page_numbers),
        "page_end": max(page_numbers),
        "text": "\n\n".join(source_texts),
        "keywords": keywords,
        "entities": entities,
    }


def build_semantic_document(source: dict[str, Any]) -> dict[str, Any]:
    document_id = source["document_id"]
    if document_id != "fr_chiffres_cles_annee_2025":
        raise ValueError("Phase 1 is intentionally limited to the French 2025 key-figures document")
    pages = page_map(source)
    family_id = "chiffres_cles_2025"

    def chunk(*args: Any, **kwargs: Any) -> dict[str, Any]:
        return make_chunk(pages, *args, **kwargs)

    sections = [
        {
            "section_id": "fr_chiffres_cles_annee_2025_sec_01",
            "title": "2025 investment dynamics",
            "topic": "regional investment overview",
            "subsections": [{
                "subsection_id": "fr_chiffres_cles_annee_2025_sec_01_sub_01",
                "title": "Annual overview",
                "chunks": [chunk([1], "fr_chiffres_cles_annee_2025_p01_c01", "narrative", ["2025 investment dynamics", "Annual overview"], ["2025", "investment dynamics", "Tanger-Tétouan-Al Hoceima"], ["Tanger-Tétouan-Al Hoceima", "Investangier"])],
            }],
        },
        {
            "section_id": "fr_chiffres_cles_annee_2025_sec_02",
            "title": "Business creation",
            "topic": "business creation and sector distribution",
            "subsections": [{
                "subsection_id": "fr_chiffres_cles_annee_2025_sec_02_sub_01",
                "title": "New companies and sector breakdown",
                "chunks": [
                    chunk([2], "fr_chiffres_cles_annee_2025_p02_c01", "statistics", ["Business creation", "New companies"], ["business creation", "new companies", "2025", "OMPIC"], ["OMPIC", "Tanger-Tétouan-Al Hoceima"]),
                    chunk([3], "fr_chiffres_cles_annee_2025_p03_c01", "table", ["Business creation", "Sector distribution"], ["sector distribution", "commerce", "services", "industry", "transport"], ["Commerce", "Services divers", "BTP", "Industries", "Transports"]),
                ],
            }],
        },
        {
            "section_id": "fr_chiffres_cles_annee_2025_sec_03",
            "title": "CRUI report",
            "topic": "Regional Unified Investment Commission activity",
            "subsections": [{
                "subsection_id": "fr_chiffres_cles_annee_2025_sec_03_sub_01",
                "title": "CRUI activity and approved investment files",
                "chunks": [
                    chunk([4], "fr_chiffres_cles_annee_2025_p04_c01", "statistics", ["CRUI report", "CRUI activity"], ["CRUI", "meetings", "processing time"], ["CRUI", "Commission Régionale Unifiée d’Investissement"]),
                    chunk([5], "fr_chiffres_cles_annee_2025_p05_c01", "statistics", ["CRUI report", "Approved investment files"], ["approved investment files", "approved investment", "projected jobs"], ["CRUI", "Commission Régionale Unifiée d’Investissement"]),
                    chunk([6], "fr_chiffres_cles_annee_2025_p06_c01", "table", ["CRUI report", "Sector distribution of approved files"], ["energy", "industry", "tourism", "services", "approved files"], ["CRUI", "Énergie", "Industrie", "Tourisme", "Services"]),
                ],
            }],
        },
        {
            "section_id": "fr_chiffres_cles_annee_2025_sec_04",
            "title": "Sector investment dynamics",
            "topic": "industrial, tourism, and energy investment",
            "subsections": [
                {
                    "subsection_id": "fr_chiffres_cles_annee_2025_sec_04_sub_01",
                    "title": "Industrial investment",
                    "chunks": [chunk([7], "fr_chiffres_cles_annee_2025_p07_c01", "industrial_zone", ["Sector investment dynamics", "Industrial investment"], ["industrial investment", "industrial zones", "projects", "jobs"], ["Tangier Free Zone", "ZI Gzenaya", "Tangier Tech", "Tangier Automotive City", "Tetouan Park"])],
                },
                {
                    "subsection_id": "fr_chiffres_cles_annee_2025_sec_04_sub_02",
                    "title": "Tourism investment",
                    "chunks": [chunk([8], "fr_chiffres_cles_annee_2025_p08_c01", "investment_opportunity", ["Sector investment dynamics", "Tourism investment"], ["tourism", "establishments", "hotel rooms", "investment"], ["Tanger-Assilah", "Fahs Anjra", "M’Diq-Fnideq", "Tétouan", "Chefchaouen", "Al Hoceima", "Larache"])],
                },
                {
                    "subsection_id": "fr_chiffres_cles_annee_2025_sec_04_sub_03",
                    "title": "Energy investment",
                    "chunks": [chunk([9], "fr_chiffres_cles_annee_2025_p09_c01", "statistics", ["Sector investment dynamics", "Energy investment"], ["energy", "solar", "wind", "thermal", "installed capacity"], ["Énergie"] )],
                },
            ],
        },
        {
            "section_id": "fr_chiffres_cles_annee_2025_sec_05",
            "title": "Business support and entrepreneurship",
            "topic": "business support, financing, conciliation, and innovation",
            "subsections": [
                {
                    "subsection_id": "fr_chiffres_cles_annee_2025_sec_05_sub_01",
                    "title": "Business support services",
                    "chunks": [chunk([10], "fr_chiffres_cles_annee_2025_p10_c01", "service", ["Business support and entrepreneurship", "Business support services"], ["business support", "entrepreneurship", "financing access", "post-investment follow-up"], ["CRI TTA", "TPME"] )],
                },
                {
                    "subsection_id": "fr_chiffres_cles_annee_2025_sec_05_sub_02",
                    "title": "PIAFE financing",
                    "chunks": [chunk([11], "fr_chiffres_cles_annee_2025_p11_c01", "statistics", ["Business support and entrepreneurship", "PIAFE financing results"], ["PIAFE", "financing", "financed files"], ["PIAFE", "Programme Intégré d’Appui et de Financement des Entreprises"] )],
                },
                {
                    "subsection_id": "fr_chiffres_cles_annee_2025_sec_05_sub_03",
                    "title": "Conciliation and dispute resolution",
                    "chunks": [chunk([12], "fr_chiffres_cles_annee_2025_p12_c01", "service", ["Business support and entrepreneurship", "Conciliation and dispute resolution"], ["conciliation", "dispute resolution", "resolution rate"], ["CRI TTA"] )],
                },
                {
                    "subsection_id": "fr_chiffres_cles_annee_2025_sec_05_sub_04",
                    "title": "Open innovation competition",
                    "chunks": [chunk([13], "fr_chiffres_cles_annee_2025_p13_c01", "statistics", ["Business support and entrepreneurship", "Open innovation competition results"], ["open innovation", "TDC", "projects", "mentors", "winners"], ["Territory Development Challenge", "MJ BIKE", "Beeka Athletic", "ECOTIDETECH"] )],
                },
            ],
        },
        {
            "section_id": "fr_chiffres_cles_annee_2025_sec_06",
            "title": "Promotion and partnerships",
            "topic": "territorial promotion, MRE support, TPME support, and strategic partnerships",
            "subsections": [
                {
                    "subsection_id": "fr_chiffres_cles_annee_2025_sec_06_sub_01",
                    "title": "Territorial promotion and investment opportunities",
                    "chunks": [chunk([14], "fr_chiffres_cles_annee_2025_p14_c01", "investment_opportunity", ["Promotion and partnerships", "Territorial promotion and investment opportunities"], ["territorial promotion", "international events", "FDI", "investment opportunities"], ["Doing Business in TTA Region", "CCIS", "AIM 2025", "Power-to-X"] )],
                },
                {
                    "subsection_id": "fr_chiffres_cles_annee_2025_sec_06_sub_02",
                    "title": "Support for Moroccans of the World",
                    "chunks": [chunk([15], "fr_chiffres_cles_annee_2025_p15_c01", "service", ["Promotion and partnerships", "Support for Moroccans of the World"], ["MRE", "welcome", "orientation", "investment support"], ["CRI", "MRE", "Mohamed Bourkha", "Vegetaland"] )],
                },
                {
                    "subsection_id": "fr_chiffres_cles_annee_2025_sec_06_sub_03",
                    "title": "TPME investment support programme",
                    "chunks": [chunk([16], "fr_chiffres_cles_annee_2025_p16_c01", "service", ["Promotion and partnerships", "TPME investment support programme"], ["investment support", "eligibility conditions", "premiums", "TPME", "information caravan"], ["TPME", "CRI", "Ouezzane", "Tanger", "Tétouan", "Al Hoceima", "Chefchaouen", "Fahs-Anjra", "Larache"] )],
                },
                {
                    "subsection_id": "fr_chiffres_cles_annee_2025_sec_06_sub_04",
                    "title": "Strategic partnership with IFC",
                    "chunks": [chunk([17], "fr_chiffres_cles_annee_2025_p17_c01", "investment_opportunity", ["Promotion and partnerships", "Strategic partnership with IFC"], ["IFC", "green investment", "business climate", "partnership"], ["IFC", "CRI TTA", "SECO", "Swiss Cooperation"] )],
                },
            ],
        },
        {
            "section_id": "fr_chiffres_cles_annee_2025_sec_07",
            "title": "Closing message",
            "topic": "territorial investment message",
            "subsections": [{
                "subsection_id": "fr_chiffres_cles_annee_2025_sec_07_sub_01",
                "title": "Closing slogan",
                "chunks": [chunk([18], "fr_chiffres_cles_annee_2025_p18_c01", "narrative", ["Closing message", "Closing slogan"], ["Investangier", "investment", "region"], ["Investangier"] )],
            }],
        },
    ]

    return {
        "schema_version": "2.0",
        "document_id": document_id,
        "document_family_id": family_id,
        "metadata": {
            "title": "L’année 2025 — Dynamique d’investissement",
            "filename": source["filename"],
            "language": source.get("language"),
            "document_type": "annual_key_figures",
            "publisher": "CRI Tanger-Tétouan-Al Hoceima",
            "region": "Tanger-Tétouan-Al Hoceima",
            "publication_year": 2025,
            "reference_period": {
                "year": 2025,
                "type": "year",
                "semester": None,
                "quarter": None,
                "label": "2025",
                "start_date": None,
                "end_date": None,
            },
            "topics": [
                "business creation",
                "CRUI investment activity",
                "industrial investment",
                "tourism investment",
                "energy investment",
                "business support",
                "financing",
                "territorial promotion",
                "strategic partnerships",
            ],
        },
        "sections": sections,
    }


def iter_chunks(document: dict[str, Any]):
    for section in document["sections"]:
        for subsection in section["subsections"]:
            for chunk in subsection["chunks"]:
                yield section, subsection, chunk


def validate_semantic_document(document: dict[str, Any], source: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_root = {"schema_version", "document_id", "document_family_id", "metadata", "sections"}
    errors.extend(f"missing root field: {field}" for field in sorted(required_root - set(document)))
    if document.get("schema_version") != "2.0":
        errors.append("schema_version must be 2.0")
    if document.get("document_id") != source.get("document_id"):
        errors.append("document_id was not preserved")
    metadata = document.get("metadata", {})
    for field in ("title", "filename", "language", "document_type", "publisher", "region", "publication_year", "reference_period", "topics"):
        if field not in metadata:
            errors.append(f"missing metadata field: {field}")
    source_pages = page_map(source)
    represented_pages: set[int] = set()
    seen_ids: set[str] = set()
    allowed_types = {"narrative", "statistics", "procedure", "faq", "financial_product", "investment_opportunity", "industrial_zone", "cost_information", "contact_information", "legal_information", "service", "eligibility_conditions", "table"}
    for section, subsection, chunk in iter_chunks(document):
        for field in ("chunk_id", "content_type", "heading_path", "page_start", "page_end", "text", "keywords", "entities"):
            if field not in chunk:
                errors.append(f"{chunk.get('chunk_id', '<unknown>')}: missing {field}")
        chunk_id = chunk.get("chunk_id")
        if chunk_id in seen_ids:
            errors.append(f"duplicate chunk_id: {chunk_id}")
        seen_ids.add(chunk_id)
        if chunk.get("content_type") not in allowed_types:
            errors.append(f"{chunk_id}: unsupported content_type {chunk.get('content_type')}")
        start, end = chunk.get("page_start"), chunk.get("page_end")
        if not isinstance(start, int) or not isinstance(end, int) or start > end:
            errors.append(f"{chunk_id}: invalid page range")
            continue
        pages = set(range(start, end + 1))
        if any(page not in source_pages for page in pages):
            errors.append(f"{chunk_id}: page range includes a missing source page")
        represented_pages.update(pages)
        expected_text = "\n\n".join(source_pages[page] for page in range(start, end + 1))
        if chunk.get("text") != expected_text:
            errors.append(f"{chunk_id}: text is not an exact concatenation of its source pages")
    useful_pages = {page for page, text in source_pages.items() if text.strip()}
    if useful_pages != represented_pages:
        errors.append(f"represented useful pages {sorted(represented_pages)} do not equal source useful pages {sorted(useful_pages)}")
    return errors


def make_report(source: dict[str, Any], semantic: dict[str, Any], source_path: Path, validation_errors: list[str]) -> str:
    chunks = list(iter_chunks(semantic))
    lines = [
        "# Semantic JSON migration report — phase 1",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "Only one representative document was converted. All 33 source JSON files were inspected. No file in `data/raw/json` was written or modified.",
        "",
        "## Corpus inventory",
        "",
        f"- Source JSON files inspected: 33",
        "- Languages by file: French 13, English 7, Spanish 7, Arabic 6",
        "- Main recurring families: CRI presentation; CRUI first-semester 2024 key figures; 2025 key figures; investment-climate indicators; industrial-zones panorama; Manar Al Moustatmir News; conciliation guides; investment/business support single-window guides; territorial-opportunity investor guides.",
        "- Standalone/single-language subjects: financing guide, utility-connection procedure guide, integrated business-support/financing programme, production-factor cost guide, logistics brochure.",
        "",
        "## Document-family inventory",
        "",
        "| Proposed family ID | Corresponding subject | Languages | Type | Period/uncertainty |",
        "|---|---|---|---|---|",
    ]
    lines.extend(f"| `{family}` | {title} | {languages} | `{doc_type}` | {period} |" for family, title, languages, doc_type, period in FAMILY_INVENTORY)
    lines.extend([
        "",
        "Family IDs are proposed from filename/title/content correspondence. They should be reviewed before converting the remaining documents, especially the Manar/Akhbar news files and files with OCR-heavy titles.",
        "",
        "## Representative document",
        "",
        f"- Source file: `{source_path.relative_to(PROJECT_ROOT).as_posix()}`",
        f"- Document ID: `{source['document_id']}` (preserved exactly)",
        f"- Document family: `{semantic['document_family_id']}`",
        f"- Detected title: `{semantic['metadata']['title']}`",
        f"- Language: `{semantic['metadata']['language']}`",
        f"- Document type: `{semantic['metadata']['document_type']}`",
        "- Publisher: `CRI Tanger-Tétouan-Al Hoceima` (the requested corpus default; the source identifies the CRI/Investangier institution)",
        "- Region: `Tanger-Tétouan-Al Hoceima`",
        "- Publication year: `2025`, supported by the cover/title and repeated 2025 references",
        "- Primary reference period: year 2025",
        "- Reference-period caveat: page 14 includes events from 2023–2026 and page 16 reports a mid-February 2026 balance; those page-level dates remain in source text and are not promoted to the document-level period.",
        "",
        "## Sections and subsections",
        "",
    ])
    for section in semantic["sections"]:
        lines.append(f"### {section['title']}")
        lines.append("")
        for subsection in section["subsections"]:
            lines.append(f"- {subsection['title']}: " + ", ".join(f"`{chunk['chunk_id']}` (pages {chunk['page_start']}-{chunk['page_end']})" for chunk in subsection["chunks"]))
        lines.append("")
    lines.extend([
        "## Chunk/page mapping",
        "",
        f"- Generated semantic chunks: **{len(chunks)}**",
        "",
        "| Chunk ID | Content type | Page(s) | Semantic location |",
        "|---|---|---:|---|",
    ])
    lines.extend(f"| `{chunk[2]['chunk_id']}` | `{chunk[2]['content_type']}` | {chunk[2]['page_start']}-{chunk[2]['page_end']} | {chunk[0]['title']} → {chunk[1]['title']} |" for chunk in chunks)
    lines.extend([
        "",
        "Every useful source page (1–18) is represented exactly once. Chunk text is copied from the corresponding original page text and joined only with a blank line when multiple pages are used; no translation or generated summary was applied.",
        "",
        "## Uncertainty and classification notes",
        "",
        "- The document-level publication year and annual reference period are reliable from the title/cover, but the document contains page-level historical/future event dates.",
        "- Page 7 combines industrial investment statistics and named industrial zones; `industrial_zone` was selected because the zone entities are central to the page.",
        "- Page 8 combines tourism statistics and territorial investment information; it is classified as `investment_opportunity`.",
        "- Page 11 reports PIAFE financing results but does not describe product terms, so it is classified as `statistics`.",
        "- Page 13 reports open-innovation competition results, so it is classified as `statistics`, not as a financial product.",
        "- Page 16 mentions eligibility conditions and premiums but does not enumerate the conditions; it is classified as `service` rather than asserting eligibility facts.",
        "- No FAQ, contact-information, legal-information, procedure, or cost-information chunk was identified in this representative document.",
        "- No aggressive OCR cleanup was applied. Source text contains layout markers, URLs, page-number artifacts, and possible OCR irregularities; these remain preserved.",
        "",
        "## Validation",
        "",
        "- JSON parsing: passed",
        "- UTF-8 read/write: passed",
        "- Required schema fields: " + ("passed" if not validation_errors else "failed"),
        "- Document ID preservation: passed",
        "- Useful-page coverage: " + ("passed" if not validation_errors else "see errors"),
        "- Exact source-page text preservation: " + ("passed" if not validation_errors else "see errors"),
    ])
    if validation_errors:
        lines.extend(["", "Validation errors:", ""] + [f"- {error}" for error in validation_errors])
    else:
        lines.extend(["", "No validation errors."])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    source_path = args.source.resolve()
    output_dir = args.output_dir.resolve()
    source = load_source(source_path)
    semantic = build_semantic_document(source)
    errors = validate_semantic_document(semantic, source)
    if errors:
        raise SystemExit("Validation failed:\n" + "\n".join(errors))
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / source_path.name
    report_path = output_dir / "migration_report_phase1.md"
    if output_path.exists() and report_path.exists():
        raise SystemExit("Refusing to overwrite existing phase-1 output files")
    if not output_path.exists():
        output_path.write_text(json.dumps(semantic, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    report_path.write_text(make_report(source, semantic, source_path, errors), encoding="utf-8", newline="\n")
    print(json.dumps({"output": str(output_path), "report": str(report_path), "chunks": sum(1 for _ in iter_chunks(semantic)), "validation": "passed"}, ensure_ascii=False))


if __name__ == "__main__":
    from migrate_semantic_phase2_2 import main as current_main
    current_main()
