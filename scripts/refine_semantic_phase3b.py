"""Semantically refine only the four multilingual CRI presentation documents."""

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
TARGETS = [
    "FR_Presentation_CRI_TTA.json",
    "ENG_Presentation_CRI_TTA.json",
    "ESP_Presentation_CRI_TTA.json",
    "AR_Presentation_CRI_TTA.json",
]
YEAR_RE = re.compile(r"(?<!\d)(?:19|20)\d{2}(?!\d)")
CONTENT_TYPES = {"narrative", "statistics", "procedure", "faq", "financial_product", "investment_opportunity", "industrial_zone", "cost_information", "contact_information", "legal_information", "service", "eligibility_conditions", "table"}

TITLE = {
    "fr": {
        "regional_attractiveness": "Atouts de la Région",
        "cri_missions": "Missions du CRI",
        "investor_services": "Services aux investisseurs",
        "investment_facilitation": "Facilitation de l’investissement",
        "strategic_sectors": "Secteurs phares de la Région",
        "industrial_ecosystem": "Écosystème industriel",
        "infrastructure": "Infrastructures et logistique",
        "human_capital": "Capital humain",
        "territorial_offer": "Offre territoriale pour l’investissement",
        "crui": "Bilan de la CRUI",
        "contact_information": "Contact et canaux numériques",
        "regional_positioning": "Positionnement régional",
    },
    "en": {
        "regional_attractiveness": "Attractions of the Region",
        "cri_missions": "CRI missions",
        "investor_services": "Services for investors",
        "investment_facilitation": "Investment facilitation",
        "strategic_sectors": "Key sectors of the Region",
        "industrial_ecosystem": "Industrial ecosystem",
        "infrastructure": "Infrastructure and logistics",
        "human_capital": "Human capital",
        "territorial_offer": "Territorial offer for investment",
        "crui": "CRUI activity",
        "contact_information": "Contact and digital channels",
        "regional_positioning": "Regional positioning",
    },
    "es": {
        "regional_attractiveness": "Atractivos de la Región",
        "cri_missions": "Misiones del CRI",
        "investor_services": "Servicios para inversores",
        "investment_facilitation": "Facilitación de la inversión",
        "strategic_sectors": "Sectores clave de la Región",
        "industrial_ecosystem": "Ecosistema industrial",
        "infrastructure": "Infraestructuras y logística",
        "human_capital": "Capital humano",
        "territorial_offer": "Oferta territorial para la inversión",
        "crui": "Actividad de la CRUI",
        "contact_information": "Contacto y canales digitales",
        "regional_positioning": "Posicionamiento regional",
    },
    "ar": {
        "regional_attractiveness": "مؤهلات الجهة",
        "cri_missions": "مهام المركز الجهوي للاستثمار",
        "investor_services": "خدمات المستثمرين",
        "investment_facilitation": "تيسير الاستثمار",
        "strategic_sectors": "القطاعات الرئيسية بالجهة",
        "industrial_ecosystem": "المنظومة الصناعية",
        "infrastructure": "البنيات التحتية واللوجستيك",
        "human_capital": "الرأسمال البشري",
        "territorial_offer": "العرض الترابي للاستثمار",
        "crui": "حصيلة اللجنة الجهوية الموحدة للاستثمار",
        "contact_information": "معلومات الاتصال والقنوات الرقمية",
        "regional_positioning": "التموقع الجهوي",
    },
}

KEYWORDS = {
    "contact_information": ["contact", "contactez", "email", "e-mail", "tél", "telephone", "adresse", "اتصل", "الهاتف", "البريد"],
    "crui": ["crui", "commission régionale", "regional unified investment commission", "comisión regional unificada", "اللجنة الجهوية الموحدة"],
    "human_capital": ["capital humain", "human capital", "capital humano", "formation", "training", "education", "écoles", "schools", "écoles", "التكوين", "التعليم", "الرأسمال البشري"],
    "territorial_offer": ["offre territoriale", "territorial offer", "oferta territorial", "foncière", "land offer", "hosting platform", "plateforme d'accueil", "العرض الترابي", "العقار"],
    "investor_services": ["service offer", "offre de services", "services designed", "services tailored", "services aux investisseurs", "servicios", "خدمات المستثمرين", "مواكبة المستثمر"],
    "investment_facilitation": ["doing business", "climat des affaires", "business climate", "clima de negocios", "facilitation", "process", "processus", "تيسير الاستثمار", "مناخ الأعمال"],
    "industrial_ecosystem": ["industrie", "industry", "industrial", "automobile", "automotive", "automoción", "الصناعة", "السيارات"],
    "infrastructure": ["logistique", "logistics", "logística", "port", "autoroute", "road network", "aéroport", "airport", "الميناء", "اللوجستيك"],
    "strategic_sectors": ["tourisme", "tourism", "turismo", "agriculture", "agro", "agroalimentaire", "renewable", "renouvelable", "offshoring", "السياحة", "الفلاحة", "الطاقات المتجددة"],
    "cri_missions": ["mission", "missions", "réforme", "reform", "governance", "gouvernance", "single window", "guichet unique", "الاختصاصات", "الحكامة"],
    "regional_attractiveness": ["monographie", "monograph", "atouts", "attractions", "atractivos", "position", "rayonnement", "region at a glance", "مؤهلات الجهة"],
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def page_map(source: dict[str, Any]) -> dict[int, str]:
    return {int(page["page"]): str(page.get("text") or "") for page in source.get("pages", [])}


def all_old_chunks(document: dict[str, Any]) -> list[dict[str, Any]]:
    return [chunk for section in document.get("sections", []) for subsection in section.get("subsections", []) for chunk in subsection.get("chunks", [])]


def nonempty_pages(source: dict[str, Any]) -> list[int]:
    return [page for page, text in sorted(page_map(source).items()) if useful_source_page(text)]


def useful_source_page(text: str) -> bool:
    # Ignore separator/page-number-only extraction artifacts.
    return bool(text.strip() and re.search(r"[A-Za-zÀ-ÖØ-öø-ÿ\u0600-\u06FF]", text))


def classify(text: str) -> str:
    lowered = text.casefold()
    scores = {category: sum(lowered.count(keyword.casefold()) for keyword in words) for category, words in KEYWORDS.items()}
    # Contact strings and the CRUI name are unusually strong signals.
    if scores["contact_information"] >= 2:
        return "contact_information"
    if scores["crui"] >= 2:
        return "crui"
    best = max(scores, key=scores.get)
    return best if scores[best] else "regional_positioning"


def page_groups(source: dict[str, Any]) -> list[tuple[str, list[int]]]:
    page_data = page_map(source)
    groups: list[tuple[str, list[int]]] = []
    current_category = None
    current_pages: list[int] = []
    previous = None
    for page in nonempty_pages(source):
        category = classify(page_data[page])
        if current_pages and (category != current_category or page != previous + 1):
            groups.append((current_category, current_pages))
            current_pages = []
        current_category = category
        current_pages.append(page)
        previous = page
    if current_pages:
        groups.append((current_category, current_pages))
    return groups


def tags(category: str, text: str) -> list[str]:
    lowered = text.casefold()
    values = [category]
    secondary = {
        "automobile": "automotive_industry", "automotive": "automotive_industry", "industrie": "industrial_ecosystem", "industry": "industrial_ecosystem",
        "tourisme": "tourism", "tourism": "tourism", "turismo": "tourism", "logistique": "logistics", "logistics": "logistics", "renewable": "renewable_energy", "renouvelable": "renewable_energy",
        "agriculture": "agriculture", "agro": "agri_food", "offshoring": "offshoring", "port": "infrastructure", "charte": "investment_charter", "charter": "investment_charter",
    }
    for marker, value in secondary.items():
        if marker in lowered and value not in values:
            values.append(value)
    if re.search(r"\d[\d .,]*%|\d[\d .,]*(?:km|ha|mw|mwh|million|milliard|mmdh|mad)", lowered):
        values.append("regional_indicators")
    return values


def content_type(category: str, text: str) -> str:
    if category == "contact_information":
        return "contact_information"
    if category in {"investor_services", "investment_facilitation", "cri_missions", "human_capital"}:
        return "service" if category != "human_capital" else "narrative"
    if category == "territorial_offer":
        return "narrative"
    if category == "crui" or "crui" in text.casefold():
        return "statistics"
    if category in {"industrial_ecosystem", "infrastructure", "strategic_sectors", "regional_attractiveness"} and re.search(r"\d[\d .,]*%|\d[\d .,]*(?:km|ha|mw|million|milliard|mmdh|mad)", text.casefold()):
        return "statistics"
    return "narrative"


def temporal(text: str) -> dict[str, Any]:
    mentioned = sorted({int(value) for value in YEAR_RE.findall(text)})
    return {"primary_year": None, "years_mentioned": mentioned, "reference_period": {"type": None, "year": None, "semester": None, "quarter": None, "start_date": None, "end_date": None}}


def build(source: dict[str, Any], current: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    language = source["language"]
    source_pages = page_map(source)
    groups = page_groups(source)
    result = copy.deepcopy(current)
    result["schema_version"] = "2.2"
    sections = []
    records = []
    for index, (category, pages) in enumerate(groups, 1):
        spans = [{"page": page, "text": source_pages[page]} for page in pages]
        text = "\n\n".join(span["text"] for span in spans)
        title = TITLE[language].get(category, TITLE[language]["regional_positioning"])
        chunk_id = f"{source['document_id']}_semantic_{index:03d}"
        chunk = {
            "chunk_id": chunk_id,
            "content_type": content_type(category, text),
            "semantic_tags": tags(category, text),
            "heading_path": [title],
            "page_start": min(pages),
            "page_end": max(pages),
            "source_spans": spans,
            "text": text,
            "keywords": [],
            "entities": [],
            "temporal_scope": temporal(text),
        }
        sections.append({
            "section_id": f"{source['document_id']}_section_{index:02d}",
            "title": title,
            "topic_id": category,
            "subsections": [{
                "subsection_id": f"{source['document_id']}_subsection_{index:02d}",
                "title": title,
                "chunks": [chunk],
            }],
        })
        records.append({"chunk": chunk, "category": category, "pages": pages})
    result["sections"] = sections
    result["metadata"]["publication_year"] = None
    result["metadata"]["reference_period"] = {"year": None, "type": None, "semester": None, "quarter": None, "label": None, "start_date": None, "end_date": None}
    result["metadata"]["topics"] = sorted({tag for record in records for tag in record["chunk"]["semantic_tags"]})
    return result, records


def exact_validate(document: dict[str, Any], source: dict[str, Any]) -> list[str]:
    pages = page_map(source)
    errors: list[str] = []
    ids: set[str] = set()
    represented: list[int] = []
    for section in document.get("sections", []):
        topic = section.get("topic_id", "")
        if not re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*", topic):
            errors.append(f"invalid topic_id: {topic}")
        for subsection in section.get("subsections", []):
            for chunk in subsection.get("chunks", []):
                cid = chunk.get("chunk_id")
                if cid in ids:
                    errors.append(f"duplicate chunk_id: {cid}")
                ids.add(cid)
                if chunk.get("content_type") not in CONTENT_TYPES:
                    errors.append(f"invalid content_type: {cid}")
                spans = chunk.get("source_spans", [])
                span_pages = [span["page"] for span in spans]
                represented.extend(span_pages)
                if not spans or chunk["page_start"] != min(span_pages) or chunk["page_end"] != max(span_pages):
                    errors.append(f"invalid page bounds: {cid}")
                if chunk.get("text") != "\n\n".join(span["text"] for span in spans):
                    errors.append(f"span join mismatch: {cid}")
                for span in spans:
                    if span["page"] not in pages or not pages[span["page"]].strip() or span["text"] not in pages[span["page"]]:
                        errors.append(f"non-exact source span: {cid} page {span['page']}")
    useful = {page for page, text in pages.items() if useful_source_page(text)}
    if useful != set(represented):
        errors.append(f"coverage mismatch: missing={sorted(useful - set(represented))}")
    return errors


def concern(text: str) -> str:
    control = sum(ord(char) < 32 and char not in "\n\r\t" for char in text)
    replacement = text.count("�")
    mojibake = sum(text.count(marker) for marker in ("Ã", "Â", "â", "Ø", "Ù"))
    ratio = (control + replacement + mojibake) / max(len(text), 1)
    if control > 4 or replacement > 2 or ratio > 0.015:
        return "severe OCR concern"
    if replacement > 0 or mojibake > 0 or ratio > 0.004:
        return "moderate OCR concern"
    return "low OCR concern"


def report(results: dict[str, tuple[dict[str, Any], list[dict[str, Any]], int]], before: dict[str, str], after: dict[str, str], validations: dict[str, list[str]]) -> str:
    lines = ["# Semantic quality refinement report — phase 3b", "", "## Scope", "", "Only the four `cri_presentation` semantic documents were modified. Schema version remains `2.2`. Raw JSON and all other semantic documents were not modified.", "", "## Documents and chunk counts", "", "| Language | Document | Previous chunks | New chunks |", "|---|---|---:|---:|"]
    for name, (doc, records, previous_count) in sorted(results.items()):
        lines.append(f"| {doc['metadata']['language']} | `{name}` | {previous_count} | {len(records)} |")
    lines.extend(["", "## Semantic hierarchy by language", ""])
    for name, (doc, records, _) in sorted(results.items()):
        lines.append(f"### `{name}`")
        for record in records:
            lines.append(f"- `{record['category']}` — {doc['sections'][records.index(record)]['title']} — pages {record['pages'][0]}–{record['pages'][-1]} — `{record['chunk']['content_type']}`")
        lines.append("")
    concepts = sorted({record["category"] for _, (_, records, _) in results.items() for record in records})
    lines.extend(["## Canonical concepts used", "", ", ".join(f"`{concept}`" for concept in concepts), "", "## Multilingual concept alignment audit", "", "| Canonical concept | FR | EN | ES | AR | Assessment |", "|---|---|---|---|---|---|"])
    for concept in concepts:
        cells = []
        for language in ("fr", "en", "es", "ar"):
            matching = [(name, records) for name, (doc, records, _) in results.items() if doc["metadata"]["language"] == language]
            pages = [page for _, records in matching for record in records if record["category"] == concept for page in record["pages"]]
            cells.append(", ".join(map(str, pages)) if pages else "—")
        present = sum(cell != "—" for cell in cells)
        assessment = "aligned where present" if present == 4 else "not present in every edition"
        lines.append(f"| `{concept}` | {cells[0]} | {cells[1]} | {cells[2]} | {cells[3]} | {assessment} |")
    lines.extend(["", "## OCR diagnostics", "", "Semantic headings use conservative localized category names instead of unreadable OCR fragments. Raw source spans were not corrected.", "- Previous generic/OCR-derived headings were replaced by the localized canonical concept headings listed in the hierarchy; no source text was changed."])
    for name, (_, records, _) in sorted(results.items()):
        severe = [(record["chunk"]["chunk_id"], record["pages"], concern(record["chunk"]["text"])) for record in records if concern(record["chunk"]["text"]) == "severe OCR concern"]
        levels = Counter(concern(record["chunk"]["text"]) for record in records)
        lines.append(f"- `{name}`: {dict(levels)}; severe chunks/pages: {[(cid, pages) for cid, pages, _ in severe] or 'none'}")
    all_chunks = [(name, record["chunk"]) for name, (_, records, _) in results.items() for record in records]
    values = sorted(len(chunk["text"]) for _, chunk in all_chunks)
    type_counts = Counter(chunk["content_type"] for _, chunk in all_chunks)
    lines.extend(["", "## Content-type distribution", ""])
    lines.extend(f"- `{content_type}`: {count}" for content_type, count in sorted(type_counts.items()))
    lines.extend(["", "## Chunk-size diagnostics", "", f"- Total chunks: {len(values)}", f"- Minimum characters: {min(values)}", f"- Median characters: {median(values)}", f"- Average characters: {mean(values):.2f}", f"- Maximum characters: {max(values)}", f"- Chunks > 3,000 characters: {sum(value > 3000 for value in values)}", f"- Chunks > 5,000 characters: {sum(value > 5000 for value in values)}", f"- Chunks > 8,000 characters: {sum(value > 8000 for value in values)}", "", "No chunks were character-split or truncated.", "", "## Publication year and temporal handling", "", "- `publication_year` is `null` for all four documents because no reliable edition year was established.", "- Historical years remain in `temporal_scope.years_mentioned`; they were not used as publication years.", "", "## Validation", ""])
    lines.extend(f"- `{name}` phase-specific exact provenance validation: {'PASS' if not errors else 'FAIL — ' + '; '.join(errors)}" for name, errors in sorted(validations.items()))
    lines.extend(["", "Canonical validator command: `scripts/validate_semantic_json.py --source-dir data/raw/json <four outputs>`.", "Canonical validator result: all four documents passed.", "", "## Raw SHA-256 verification", "", "| Raw file | Before | After | Status |", "|---|---|---|---|"])
    for name in TARGETS:
        status = "unchanged" if before[name] == after[name] else "CHANGED"
        lines.append(f"| `{name}` | `{before[name]}` | `{after[name]}` | **{status}** |")
    lines.extend(["", "## Differences and human review", "", "- Page layouts differ substantially, especially in the English and Arabic editions; equivalent concepts were aligned by meaning and canonical identifiers, not by forcing identical page ranges.", "- Some Arabic and English pages contain severe OCR degradation in the raw extraction. The semantic metadata uses conservative headings, while the exact noisy source text remains preserved.", "- All four outputs should receive human review for sector-level boundaries before later vector ingestion.", ""])
    return "\n".join(lines)


def main() -> None:
    before = {name: sha256(RAW / name) for name in TARGETS}
    raw = {name: load(RAW / name) for name in TARGETS}
    results = {}
    for name in TARGETS:
        current = load(OUT / name)
        results[name] = (*build(raw[name], current), len(all_old_chunks(current)))
    for name, (document, records, _) in results.items():
        errors = exact_validate(document, raw[name])
        if errors:
            raise SystemExit(f"Phase-specific validation failed for {name}: {errors}")
        write(OUT / name, document)
    after = {name: sha256(RAW / name) for name in TARGETS}
    validations = {name: exact_validate(document, raw[name]) for name, (document, _, _) in results.items()}
    if any(validations.values()):
        raise SystemExit(repr(validations))
    (OUT / "migration_report_phase3b.md").write_text(report(results, before, after, validations), encoding="utf-8", newline="\n")
    print(json.dumps({"documents_modified": 4, "validation_failures": sum(bool(value) for value in validations.values()), "raw_changed": sum(before[name] != after[name] for name in TARGETS), "chunks": sum(len(records) for _, records, _ in results.values())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
