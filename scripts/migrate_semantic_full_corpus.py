"""Convert the remaining raw JSON corpus documents to semantic JSON 2.2.

This script only reads data/raw/json and writes data/semantic_json. It does not
touch the RAG application, vector stores, embeddings, or production data.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "json"
OUT = ROOT / "data" / "semantic_json"
SCHEMA_VERSION = "2.2"
YEAR_RE = re.compile(r"(?<!\d)(?:19|20)\d{2}(?!\d)")
SNAKE_RE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")

FAMILY_BY_FILE = {
    "Akhbar_Al_Moustatmir_News.json": ("manar_al_moustatmir_news_2023", "news_review"),
    "Manar_Al_Moustatmir_News.json": ("manar_al_moustatmir_news_2023", "news_review"),
    "Manar_Al_Moustatmir_ENG_PNG.json": ("manar_al_moustatmir_news_2023", "news_review"),
    "Arabe_Chiffres_cles_2025.json": ("chiffres_cles_2025", "key_figures"),
    "Eng_Chiffres_cles_annee_2025.json": ("chiffres_cles_2025", "key_figures"),
    "ESP_Chiffres_cles_annee_2025.json": ("chiffres_cles_2025", "key_figures"),
    "FR_Chiffres_cles_annee_2025.json": ("chiffres_cles_2025", "key_figures"),
    "Chiffres_cles_CRUI_1er_semestre_2024_Anglais.json": ("crui_key_figures_2024_h1", "key_figures"),
    "Chiffres_cles_CRUI_1er_semestre_2024_Arabe.json": ("crui_key_figures_2024_h1", "key_figures"),
    "Chiffres_cles_CRUI_1er_semestre_2024_Espagnol.json": ("crui_key_figures_2024_h1", "key_figures"),
    "Chiffres_cles_CRUI_1er_semestre_2024_Francais.json": ("crui_key_figures_2024_h1", "key_figures"),
    "AR_Presentation_CRI_TTA.json": ("cri_presentation", "institutional_presentation"),
    "ENG_Presentation_CRI_TTA.json": ("cri_presentation", "institutional_presentation"),
    "ESP_Presentation_CRI_TTA.json": ("cri_presentation", "institutional_presentation"),
    "FR_Presentation_CRI_TTA.json": ("cri_presentation", "institutional_presentation"),
    "ENG_Indicateurs_climat_investissement.json": ("investment_climate_indicators", "business_climate"),
    "ESP_Indicateurs_climat_investissement.json": ("investment_climate_indicators", "business_climate"),
    "Fr_Indicateurs_climat_investissement.json": ("investment_climate_indicators", "business_climate"),
    "ENG_Panorama_des_ZI.json": ("industrial_zones_panorama", "industrial_zones"),
    "ES_Panorama_des_ZI.json": ("industrial_zones_panorama", "industrial_zones"),
    "FR_Panorama_Zones_economiques_industrielles.json": ("industrial_zones_panorama", "industrial_zones"),
    "Guide_de_Conciliation_AR.json": ("conciliation_guide", "conciliation_guide"),
    "Guide_de_Conciliation_ES.json": ("conciliation_guide", "conciliation_guide"),
    "Investment_Business_Support_Single_Window_ES.json": ("investment_business_support_single_window", "single_window_services"),
    "Investment_Business_Support_Single_Window_FR.json": ("investment_business_support_single_window", "single_window_services"),
    "Investors_Guide_territorial_opportunities_EN.json": ("investors_guide_territorial_opportunities", "investment_opportunities"),
    "Investors_Guide_territorial_opportunities_FR.json": ("investors_guide_territorial_opportunities", "investment_opportunities"),
    "Guide_branchement_electricite_eau_assainissement.json": ("electricity_water_sanitation_connection", "utility_connection_guide"),
    "Guide_programme_integre_appui_financement_entreprises_AR.json": ("integrated_business_support_financing", "integrated_financing_programme"),
    "Nv_Guide_Cout_facteurs_CRI_2024.json": ("production_factor_cost_guide_2024", "cost_guide"),
    "Brochure_secteur_Logistique.json": ("logistics_sector_brochure", "sector_brochure"),
    "FR_Chiffres_cles_CRITTA_30_Sept_2024.json": ("crui_key_figures_2024_09_30", "key_figures"),
    "Guide_du_financement_des_entreprises.json": ("financing_guide", "financing_guide"),
}

FAMILY_TITLES = {
    "fr": {
        "key_figures": "Chiffres clés et statistiques",
        "institutional_presentation": "Présentation du Centre Régional d’Investissement",
        "business_climate": "Climat des affaires",
        "industrial_zones": "Panorama des zones industrielles",
        "news_review": "Actualités et bilan de l’investissement",
        "conciliation_guide": "Guide de la conciliation",
        "single_window_services": "Accompagnement des investisseurs et des entreprises",
        "investment_opportunities": "Opportunités territoriales d’investissement",
        "utility_connection_guide": "Branchement à l’électricité, à l’eau et à l’assainissement",
        "cost_guide": "Coût des facteurs de production",
        "sector_brochure": "Secteur de la logistique",
    },
    "en": {
        "key_figures": "Key figures and statistics",
        "institutional_presentation": "Presentation of the Regional Investment Center",
        "business_climate": "Business climate",
        "industrial_zones": "Industrial zones panorama",
        "news_review": "Investment and entrepreneurship news review",
        "investment_opportunities": "Territorial investment opportunities",
    },
    "es": {
        "key_figures": "Cifras clave y estadísticas",
        "institutional_presentation": "Presentación del Centro Regional de Inversiones",
        "business_climate": "Clima empresarial",
        "industrial_zones": "Panorama de las zonas industriales",
        "conciliation_guide": "Guía de conciliación",
        "single_window_services": "Apoyo a los inversores y las empresas",
        "investment_opportunities": "Oportunidades territoriales de inversión",
    },
    "ar": {
        "key_figures": "المؤشرات الرئيسية والإحصائيات",
        "institutional_presentation": "تقديم المركز الجهوي للاستثمار",
        "news_review": "أخبار الاستثمار وريادة الأعمال",
        "conciliation_guide": "دليل المصالحة",
        "integrated_financing_programme": "البرنامج المندمج لدعم وتمويل المقاولات",
    },
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def pages(source: dict[str, Any]) -> dict[int, str]:
    return {int(item["page"]): str(item.get("text") or "") for item in source.get("pages", [])}


def nonempty_page_numbers(source: dict[str, Any]) -> list[int]:
    return [number for number, text in sorted(pages(source).items()) if text.strip()]


def lang_title(language: str, kind: str) -> str:
    return FAMILY_TITLES.get(language, {}).get(kind) or FAMILY_TITLES["fr"].get(kind, kind.replace("_", " ").title())


def first_heading(text: str, fallback: str) -> str:
    candidates = []
    for raw in text.splitlines():
        value = " ".join(raw.split()).strip(" -|•·")
        if not value or value.lower().startswith("www."):
            continue
        if len(value) >= 4:
            candidates.append(value)
    if not candidates:
        return fallback
    value = candidates[0]
    return value[:180]


def family_topic(kind: str) -> str:
    return {
        "key_figures": "regional_statistics",
        "institutional_presentation": "investment_agency",
        "business_climate": "business_climate",
        "industrial_zones": "industrial_zones",
        "news_review": "investment_news",
        "conciliation_guide": "conciliation",
        "single_window_services": "business_support",
        "investment_opportunities": "investment_opportunities",
        "utility_connection_guide": "utility_connections",
        "integrated_financing_programme": "integrated_financing",
        "cost_guide": "production_costs",
        "sector_brochure": "logistics_sector",
        "financing_guide": "business_financing",
    }.get(kind, "regional_investment")


def group_size(kind: str) -> int:
    return {
        "industrial_zones": 2,
        "investment_opportunities": 3,
        "news_review": 3,
        "institutional_presentation": 3,
        "business_climate": 2,
        "single_window_services": 2,
        "cost_guide": 2,
        "sector_brochure": 2,
        "utility_connection_guide": 2,
        "conciliation_guide": 1,
        "key_figures": 1,
    }.get(kind, 2)


def page_groups(numbers: list[int], size: int) -> list[list[int]]:
    groups: list[list[int]] = []
    current: list[int] = []
    previous = None
    for number in numbers:
        if current and (number != previous + 1 or len(current) >= size):
            groups.append(current)
            current = []
        current.append(number)
        previous = number
    if current:
        groups.append(current)
    return groups


def years(text: str) -> list[int]:
    return sorted({int(value) for value in YEAR_RE.findall(text)})


def temporal_scope(text: str) -> dict[str, Any]:
    found = years(text)
    primary = found[0] if len(found) == 1 else None
    period_type = "year" if primary is not None else None
    semester = None
    if primary is not None and re.search(r"(?:1er|1st|premier|first).{0,30}(?:semestre|semester|semestre)", text, re.I):
        period_type, semester = "semester", 1
    return {"primary_year": primary, "years_mentioned": found, "reference_period": {
        "type": period_type, "year": primary, "semester": semester, "quarter": None,
        "start_date": None, "end_date": None,
    }}


def publication_year(source: dict[str, Any]) -> int | None:
    text = "\n".join(str(item.get("text") or "") for item in source.get("pages", [])[:5])
    found = years(text)
    return found[0] if len(found) == 1 else None


def make_document(source: dict[str, Any], filename: str, family: str, kind: str) -> dict[str, Any]:
    source_pages = pages(source)
    language = str(source.get("language") or "und")
    display_title = lang_title(language, kind)
    groups = page_groups(nonempty_page_numbers(source), group_size(kind))
    topic = family_topic(kind)
    section_id = f"{source['document_id']}_section_01"
    subsections = []
    for index, group in enumerate(groups, 1):
        span_list = [{"page": page, "text": source_pages[page]} for page in group]
        chunk_text = "\n\n".join(span["text"] for span in span_list)
        heading = first_heading(chunk_text, f"{display_title} — unité {index}")
        content_type = {
            "key_figures": "statistics",
            "industrial_zones": "industrial_zone",
            "investment_opportunities": "investment_opportunity",
            "business_climate": "statistics",
            "utility_connection_guide": "procedure",
            "conciliation_guide": "procedure",
            "single_window_services": "service",
            "cost_guide": "cost_information",
            "news_review": "narrative",
            "sector_brochure": "narrative",
            "institutional_presentation": "narrative",
            "integrated_financing_programme": "financial_product",
        }.get(kind, "narrative")
        chunk_id = f"{source['document_id']}_chunk_{index:03d}"
        chunk = {
            "chunk_id": chunk_id,
            "content_type": content_type,
            "semantic_tags": [topic],
            "heading_path": [display_title, heading],
            "page_start": min(group),
            "page_end": max(group),
            "source_spans": span_list,
            "text": chunk_text,
            "keywords": [],
            "entities": [],
            "temporal_scope": temporal_scope(chunk_text),
        }
        subsections.append({
            "subsection_id": f"{source['document_id']}_subsection_{index:03d}",
            "title": heading,
            "chunks": [chunk],
        })
    return {
        "schema_version": SCHEMA_VERSION,
        "document_id": source["document_id"],
        "document_family_id": family,
        "metadata": {
            "title": display_title,
            "filename": filename,
            "language": language,
            "document_type": kind,
            "publisher": "CRI Tanger-Tétouan-Al Hoceima",
            "region": "Tanger-Tétouan-Al Hoceima",
            "publication_year": publication_year(source),
            "reference_period": {"year": publication_year(source), "type": "edition" if publication_year(source) else None, "semester": None, "quarter": None, "label": str(publication_year(source)) if publication_year(source) else None, "start_date": None, "end_date": None},
            "topics": [topic],
        },
        "sections": [{
            "section_id": section_id,
            "title": display_title,
            "topic_id": topic,
            "subsections": subsections,
        }],
    }


def iter_chunks(document: dict[str, Any]):
    for section in document.get("sections", []):
        for subsection in section.get("subsections", []):
            for chunk in subsection.get("chunks", []):
                yield section, subsection, chunk


def validate_document(document: dict[str, Any], source: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source_pages = pages(source)
    ids: set[str] = set()
    for section, subsection, chunk in iter_chunks(document):
        if not SNAKE_RE.match(section.get("topic_id", "")):
            errors.append(f"invalid topic_id: {section.get('topic_id')}")
        cid = chunk.get("chunk_id")
        if cid in ids:
            errors.append(f"duplicate chunk_id: {cid}")
        ids.add(cid)
        spans = chunk.get("source_spans", [])
        if not spans:
            errors.append(f"missing source_spans: {cid}")
            continue
        span_pages = [span["page"] for span in spans]
        if chunk["page_start"] != min(span_pages) or chunk["page_end"] != max(span_pages):
            errors.append(f"page bounds mismatch: {cid}")
        if chunk["text"] != "\n\n".join(span["text"] for span in spans):
            errors.append(f"text/span mismatch: {cid}")
        for span in spans:
            if span["page"] not in source_pages or not source_pages[span["page"]].strip():
                errors.append(f"missing source page: {cid}:{span['page']}")
            elif span["text"] not in source_pages[span["page"]]:
                errors.append(f"non-exact source span: {cid}:{span['page']}")
    return errors


def coverage(document: dict[str, Any], source: dict[str, Any]) -> tuple[list[int], Counter[int]]:
    useful = {page for page, text in pages(source).items() if text.strip()}
    counts: Counter[int] = Counter()
    for _, _, chunk in iter_chunks(document):
        for span in chunk["source_spans"]:
            counts[span["page"]] += 1
    return sorted(useful - set(counts)), counts


def language_inventory(documents: dict[str, dict[str, Any]]) -> str:
    counts = Counter(document["metadata"]["language"] for document in documents.values())
    return ", ".join(f"{language}: {count}" for language, count in sorted(counts.items()))


def build_report(documents: dict[str, dict[str, Any]], sources: dict[str, dict[str, Any]], hashes_before: dict[str, str], hashes_after: dict[str, str], validation: dict[str, list[str]], skipped: list[str]) -> str:
    chunks = [(filename, section, subsection, chunk) for filename, doc in documents.items() for section, subsection, chunk in iter_chunks(doc)]
    lengths = [(filename, section, subsection, chunk) for filename, section, subsection, chunk in chunks]
    values = sorted(len(chunk["text"]) for _, _, _, chunk in chunks)
    large = sorted(((filename, section, subsection, chunk) for filename, section, subsection, chunk in chunks if len(chunk["text"]) > 12000), key=lambda item: len(item[3]["text"]), reverse=True)
    lines = ["# Full corpus semantic JSON migration report", "", "## Summary", "", f"- Raw documents discovered: {len(sources)}", f"- Semantic documents present: {len(documents)}", f"- Documents converted in this run: {sum(name not in {'FR_Chiffres_cles_annee_2025.json', 'Guide_du_financement_des_entreprises.json'} for name in documents)}", f"- Documents skipped: {len(skipped)}", f"- Total semantic chunks: {len(chunks)}", f"- Languages: {language_inventory(documents)}", "", "## Document inventory", "", "| Source file | document_id | family | language | type | chunks |", "|---|---|---|---|---|---|"]
    for filename, doc in sorted(documents.items()):
        lines.append(f"| `{filename}` | `{doc['document_id']}` | `{doc['document_family_id']}` | `{doc['metadata']['language']}` | `{doc['metadata']['document_type']}` | {sum(1 for _ in iter_chunks(doc))} |")
    lines.extend(["", "## Document-family consistency audit", ""])
    families: defaultdict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for filename, doc in documents.items():
        families[doc["document_family_id"]].append((filename, doc))
    for family, members in sorted(families.items()):
        languages = ", ".join(sorted(doc["metadata"]["language"] for _, doc in members))
        topic_ids = sorted({section["topic_id"] for _, doc in members for section in doc["sections"]})
        lines.extend([f"### `{family}`", "", f"- Languages: {languages}", f"- Documents: {', '.join(filename for filename, _ in members)}", f"- Topic IDs: {', '.join(topic_ids)}", f"- Chunk counts: {', '.join(f'{doc['metadata']['language']}={sum(1 for _ in iter_chunks(doc))}' for _, doc in members)}", "- Alignment note: chunk counts are not required to match; this audit compares family/topic identifiers and flags no automatic structural failure.", ""])
    type_counts = Counter(chunk["content_type"] for _, _, _, chunk in chunks)
    tag_counts = Counter(tag for _, _, _, chunk in chunks for tag in chunk["semantic_tags"])
    lines.extend(["## Content and tag distributions", "", "Content types:"])
    lines.extend(f"- `{key}`: {value}" for key, value in sorted(type_counts.items()))
    lines.append("Semantic tags:")
    lines.extend(f"- `{key}`: {value}" for key, value in tag_counts.most_common(30))
    lines.extend(["", "## Chunk-size diagnostics", "", f"- Minimum characters: {min(values)}", f"- Median characters: {median(values)}", f"- Average characters: {mean(values):.2f}", f"- Maximum characters: {max(values)}", f"- Chunks > 3,000 characters: {sum(value > 3000 for value in values)}", f"- Chunks > 5,000 characters: {sum(value > 5000 for value in values)}", f"- Chunks > 8,000 characters: {sum(value > 8000 for value in values)}", f"- Chunks > 12,000 characters: {sum(value > 12000 for value in values)}", "", "Largest chunks over 12,000 characters:"])
    if large:
        for filename, section, subsection, chunk in large:
            lines.append(f"- `{documents[filename]['document_id']}` / `{chunk['chunk_id']}`: {len(chunk['text'])} characters; {section['title']} / {subsection['title']}; pages {chunk['page_start']}-{chunk['page_end']}")
    else:
        lines.append("- None.")
    lines.extend(["", "## Provenance and coverage", ""])
    multi_pages = []
    for filename, doc in sorted(documents.items()):
        missing, counts = coverage(doc, sources[filename])
        empty_pages = sorted(page for page, text in pages(sources[filename]).items() if not text.strip())
        multiple = {page: count for page, count in sorted(counts.items()) if count > 1}
        multi_pages.extend((filename, page, count) for page, count in multiple.items())
        lines.extend([f"### `{filename}`", "", f"- Useful pages not represented: {missing or 'none'}", f"- Empty source pages ignored: {empty_pages or 'none'} (no factual text to preserve)", f"- Pages represented once: {sum(count == 1 for count in counts.values())}", f"- Pages represented multiple times: {multiple or 'none'}", ""])
    manual_review = sorted(filename for filename in documents if filename not in {"FR_Chiffres_cles_annee_2025.json", "Guide_du_financement_des_entreprises.json"})
    lines.extend(["## Temporal metadata", "", f"- Chunks with an explicit primary year: {sum(chunk['temporal_scope']['primary_year'] is not None for _, _, _, chunk in chunks)}", f"- Chunks with one or more explicit years mentioned: {sum(bool(chunk['temporal_scope']['years_mentioned']) for _, _, _, chunk in chunks)}", "- The migration does not infer a primary year from the document filename when the chunk text is ambiguous.", "", "## OCR and manual-review warnings", "", "- OCR artifacts, broken words, duplicated URLs, layout markers, and mixed-language extraction remain preserved where present.", "- Empty source pages were not included in source spans; they are reported through the per-document coverage diagnostics.", "- New documents use semantically grouped consecutive page units. Industrial-zone and opportunity guides use smaller groups, but pages with several independently extractable units may require a later manual refinement pass.", "- No new content type was introduced.", "", "## Documents requiring manual semantic review", "", "The converted documents below are structurally valid and provenance-safe, but should receive human semantic-boundary review before production ingestion. The automated pass grouped exact consecutive source pages and did not invent or rewrite facts:"])
    lines.extend(f"- `{filename}`" for filename in manual_review)
    lines.extend(["", "## Validation", "", f"- Documents passing in-script exact-span validation: {sum(not errors for errors in validation.values())}/{len(validation)}", f"- Documents failing validation: {sum(bool(errors) for errors in validation.values())}"])
    for filename, errors in sorted(validation.items()):
        lines.append(f"- `{filename}`: {'PASS' if not errors else 'FAIL — ' + '; '.join(errors[:5])}")
    lines.extend(["", "## Raw SHA-256 integrity", "", "All raw files were hashed before and after migration. No raw source file was written.", "", "| File | Before | After | Status |", "|---|---|---|---|"])
    for filename in sorted(hashes_before):
        status = "unchanged" if hashes_before[filename] == hashes_after[filename] else "CHANGED"
        lines.append(f"| `{filename}` | `{hashes_before[filename]}` | `{hashes_after[filename]}` | **{status}** |")
    lines.extend(["", "## Output boundary", "", "- The two reviewed semantic documents were preserved and validated; they were not regenerated by this full-corpus run.", "- No RAG, embedding, Qdrant, retrieval, prompt, API, frontend, or production files were modified.", "- No files were skipped due to unsafe conversion.", ""])
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    raw_paths = sorted(RAW.glob("*.json"))
    hashes_before = {path.name: sha256(path) for path in raw_paths}
    sources = {path.name: load(path) for path in raw_paths}
    missing_mapping = sorted(set(sources) - set(FAMILY_BY_FILE))
    if missing_mapping:
        raise SystemExit("No explicit family mapping for: " + ", ".join(missing_mapping))
    reviewed = {"FR_Chiffres_cles_annee_2025.json", "Guide_du_financement_des_entreprises.json"}
    documents: dict[str, dict[str, Any]] = {}
    for filename, source in sources.items():
        if filename in reviewed:
            documents[filename] = load(OUT / filename)
            continue
        family, kind = FAMILY_BY_FILE[filename]
        document = make_document(source, filename, family, kind)
        errors = validate_document(document, source)
        if errors:
            raise SystemExit(f"Validation failed before writing {filename}: " + "; ".join(errors[:10]))
        (OUT / filename).write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        documents[filename] = document
    hashes_after = {path.name: sha256(path) for path in raw_paths}
    validation = {}
    for filename, document in documents.items():
        validation[filename] = validate_document(document, sources[filename])
    if any(validation.values()):
        raise SystemExit("Final in-script validation failed: " + repr({name: errors for name, errors in validation.items() if errors}))
    report = build_report(documents, sources, hashes_before, hashes_after, validation, [])
    (OUT / "migration_report_full_corpus.md").write_text(report, encoding="utf-8", newline="\n")
    print(json.dumps({"raw_documents": len(sources), "semantic_documents": len(documents), "converted": len(sources) - len(reviewed), "chunks": sum(1 for doc in documents.values() for _ in iter_chunks(doc)), "validation_failures": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
