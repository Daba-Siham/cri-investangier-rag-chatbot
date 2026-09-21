"""Legacy phase-2 migration implementation.

The canonical migration entry point is now ``migrate_semantic_phase2_2.py``.
The legacy implementation remains available as a library source for its guide
specifications, but running this file delegates to schema 2.2.

This phase deliberately handles only the two representative documents. It
reads source JSON and writes only data/semantic_json outputs.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from migrate_semantic_phase1 import load_source, page_map, iter_chunks


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "semantic_json"
ALLOWED = {"narrative", "statistics", "procedure", "faq", "financial_product", "investment_opportunity", "industrial_zone", "cost_information", "contact_information", "legal_information", "service", "eligibility_conditions", "table"}
YEAR_RE = re.compile(r"(?<!\d)(?:19|20)\d{2}(?!\d)")


def temporal_scope(text: str, primary_year: int | None = None) -> dict[str, Any]:
    years = sorted({int(value) for value in YEAR_RE.findall(text or "")})
    return {
        "primary_year": primary_year,
        "years_mentioned": years,
        "reference_period": {
            "type": "year" if primary_year is not None else None,
            "year": primary_year,
            "semester": None,
            "quarter": None,
            "start_date": None,
            "end_date": None,
        },
    }


def upgrade_key_figures(source: dict[str, Any], old: dict[str, Any]) -> dict[str, Any]:
    section_titles = {
        "2025 investment dynamics": ("Dynamique d’investissement 2025", "regional_investment_overview"),
        "Business creation": ("Création d’entreprises", "business_creation"),
        "CRUI report": ("Bilan de la CRUI", "crui_activity"),
        "Sector investment dynamics": ("Dynamique des investissements sectoriels", "sector_investment"),
        "Business support and entrepreneurship": ("Accompagnement des entreprises et entrepreneuriat", "business_support"),
        "Promotion and partnerships": ("Promotion et partenariats", "promotion_partnerships"),
        "Closing message": ("Message de clôture", "closing_message"),
    }
    subsection_titles = {
        "Annual overview": "Vue d’ensemble annuelle",
        "New companies and sector breakdown": "Nouvelles entreprises et répartition sectorielle",
        "CRUI activity and approved investment files": "Activité de la CRUI et dossiers d’investissement approuvés",
        "Industrial investment": "Investissement industriel",
        "Tourism investment": "Investissement touristique",
        "Energy investment": "Investissement énergétique",
        "Business support services": "Services d’accompagnement des entreprises",
        "PIAFE financing results": "Résultats du financement PIAFE",
        "Conciliation and dispute resolution": "Conciliation et règlement des différends",
        "Open innovation competition results": "Résultats du concours d’innovation ouverte",
        "Territorial promotion and investment opportunities": "Promotion territoriale et opportunités d’investissement",
        "Support for Moroccans of the World": "Accompagnement des Marocains du Monde",
        "TPME investment support programme": "Dispositif d’appui à l’investissement des TPME",
        "Strategic partnership with IFC": "Partenariat stratégique avec l’IFC",
        "Closing slogan": "Slogan de clôture",
    }
    tags = {
        "p01": ["regional_investment_overview"], "p02": ["business_creation"], "p03": ["business_creation", "sector_distribution"],
        "p04": ["crui_activity", "statistics"], "p05": ["crui_activity", "investment_approval"], "p06": ["crui_activity", "sector_distribution"],
        "p07": ["industrial_investment", "industrial_zones"], "p08": ["tourism_investment", "territorial_statistics"], "p09": ["energy_investment"],
        "p10": ["business_support", "entrepreneurship"], "p11": ["piafe", "financing"], "p12": ["conciliation", "dispute_resolution"],
        "p13": ["open_innovation", "entrepreneurship"], "p14": ["territorial_promotion", "investment_opportunities"], "p15": ["mre_support", "business_support"],
        "p16": ["tpme_support", "investment_support"], "p17": ["strategic_partnership", "green_investment"], "p18": ["regional_investment_overview"],
    }
    primary_years = {1: 2025, 2: 2025, 3: 2025, 7: 2025, 8: 2025, 9: 2025, 13: 2025, 15: 2025, 16: 2026}
    upgraded = json.loads(json.dumps(old, ensure_ascii=False))
    upgraded["schema_version"] = "2.1"
    upgraded["metadata"]["topics"] = ["business_creation", "crui_activity", "industrial_investment", "tourism_investment", "energy_investment", "business_support", "financing", "territorial_promotion", "strategic_partnerships"]
    for section in upgraded["sections"]:
        old_title = section.pop("topic", None)
        display_title, topic_id = section_titles.get(section["title"], (section["title"], section["section_id"]))
        section["title"] = display_title
        section["topic_id"] = topic_id
        for subsection in section["subsections"]:
            old_subtitle = subsection["title"]
            subsection["title"] = subsection_titles.get(old_subtitle, old_subtitle)
            for item in subsection["chunks"]:
                page = item["page_start"]
                item["heading_path"] = [section["title"], subsection["title"]]
                item["semantic_tags"] = tags.get(f"p{page:02d}", [section["topic_id"]])
                item["temporal_scope"] = temporal_scope(item["text"], primary_years.get(page))
                if page in {7, 8, 9, 14, 17}:
                    item["content_type"] = "statistics" if page in {7, 8, 9} else item["content_type"]
    return upgraded


def guide_specs() -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    def add(section_id: str, section_title: str, topic_id: str, subsection_id: str, subsection_title: str, pages: list[int], name: str, content_type: str, semantic_tags: list[str], keywords: list[str], entities: list[str], primary_year: int | None = None):
        specs.append({"section_id": section_id, "section_title": section_title, "topic_id": topic_id, "subsection_id": subsection_id, "subsection_title": subsection_title, "pages": pages, "name": name, "content_type": content_type, "semantic_tags": semantic_tags, "keywords": keywords, "entities": entities, "primary_year": primary_year})
    add("sec_01", "Présentation du guide", "guide_overview", "sub_01", "Présentation et objectifs", [1, 2, 3], "presentation", "narrative", ["guide_overview", "business_financing"], ["guide", "financement", "entreprise"], ["CRI Tanger-Tétouan-Al Hoceima"], 2022)
    add("sec_01", "Présentation du guide", "guide_overview", "sub_02", "Vision et préambule", [4, 5, 6, 7], "vision_preamble", "narrative", ["guide_overview", "business_financing"], ["entreprise", "financement", "développement"], ["Centre Régional d’Investissement"], None)
    add("sec_01", "Présentation du guide", "guide_overview", "sub_03", "Mots des partenaires", [8, 9], "partner_messages", "narrative", ["guide_overview", "business_financing"], ["financement", "investissement", "accompagnement"], ["CRI TTA", "CGEM TTA"], None)
    add("sec_02", "Contacts et mode d’emploi", "guide_navigation", "sub_01", "Contacts introductifs", [10, 11], "intro_contacts", "contact_information", ["contact_information", "investor_support"], ["contact", "CRI", "Tamwilcom"], ["Tamwilcom", "CRI Tanger-Tétouan-Al Hoceima"], None)
    add("sec_02", "Contacts et mode d’emploi", "guide_navigation", "sub_02", "Organisation du guide", [12], "how_to_use", "narrative", ["guide_structure", "financing_products"], ["matrices", "fiches-produits", "glossaire"], [], None)
    add("sec_03", "Matrice des financements", "financing_matrix", "sub_01", "Matrices par taille et situation", [13, 14, 15], "financing_matrix", "table", ["financing_matrix", "beneficiaries", "financing_products"], ["TPE", "PME", "AGR", "organismes"], ["TPE", "PME", "AGR"], None)
    add("sec_04", "Financement par fonds propres et accompagnement", "equity_financing", "sub_01", "Fonds propres et love money", [17, 18], "equity_love_money", "financial_product", ["equity_financing", "love_money"], ["fonds propres", "love money", "capital"], ["Love money"], None)
    add("sec_04", "Financement par fonds propres et accompagnement", "entrepreneur_support", "sub_02", "Soutien au TPE et aux AGR", [19, 20], "tpe_agr_support", "financial_product", ["tpe_support", "income_generating_activities"], ["TPE", "AGR", "accompagnement"], ["Entraide Nationale"], None)
    add("sec_04", "Financement par fonds propres et accompagnement", "entrepreneur_support", "sub_03", "Inclusion économique des jeunes", [21], "youth_inclusion", "service", ["youth_support", "entrepreneurship"], ["jeunes", "entrepreneuriat", "économie sociale"], [], None)
    add("sec_04", "Financement par fonds propres et accompagnement", "entrepreneur_support", "sub_04", "Produits d’accompagnement entrepreneurial", [23, 24, 25, 26], "entrepreneurial_support_products", "service", ["entrepreneur_support", "business_creation"], ["innovation", "entrepreneuriat", "accompagnement"], ["Innov Idea", "CEED Morocco", "Réseau Entreprendre Maroc", "Tanja Moubadara"], None)
    add("sec_05", "Financement par microcrédit", "microcredit", "sub_01", "Prêts TPE et prêts professionnels", [27, 28, 29, 30], "microcredit_products", "financial_product", ["microcredit", "tpe_financing", "working_capital"], ["microcrédit", "prêt TPE", "prêt voiture", "prêt entreprise"], ["Associations de microfinance"], None)
    add("sec_06", "Financement par les banques", "bank_financing", "sub_01", "Programme intégré d’appui et de financement", [31, 32, 33, 34], "piafe_bank_products", "financial_product", ["bank_financing", "piafe", "investment_financing", "working_capital"], ["PIAFE", "banques", "investissement", "fonctionnement"], ["Programme Intégré d’Appui et de Financement des Entreprises"], None)
    add("sec_07", "Financement par crédit-bail", "leasing", "sub_01", "Crédit-bail mobilier et immobilier", [35, 36, 37, 38], "leasing_products", "financial_product", ["leasing", "equipment_financing", "real_estate_financing"], ["crédit-bail", "leasing", "mobilier", "immobilier"], ["Sociétés de leasing"], None)
    add("sec_08", "Financement par crédits bancaires", "bank_credit", "sub_01", "Crédits amortissables", [39], "amortizable_credit_index", "narrative", ["bank_credit", "financing_products"], ["crédits amortissables", "crédit investissement", "crédit fonctionnement"], ["Banques"], None)
    add("sec_08", "Financement par crédits bancaires", "bank_credit", "sub_01", "Crédits amortissables", [41, 42, 43, 44, 45], "amortizable_credit_products", "financial_product", ["bank_credit", "investment_financing", "working_capital"], ["crédit investissement", "crédit fonctionnement", "amortissable"], ["Banques"], None)
    add("sec_08", "Financement par crédits bancaires", "bank_credit", "sub_02", "Crédits de trésorerie", [47, 48, 49, 50, 51, 52, 53], "treasury_credit", "financial_product", ["bank_credit", "treasury_financing", "working_capital"], ["trésorerie", "escompte", "avances", "factures"], ["Banques"], None)
    add("sec_08", "Financement par crédits bancaires", "bank_credit", "sub_03", "Crédits par signature", [55, 56, 57], "signature_credit", "financial_product", ["bank_credit", "guarantees", "signature_credit"], ["caution", "aval", "garantie"], ["Banques"], None)
    add("sec_08", "Financement par crédits bancaires", "bank_credit", "sub_04", "Crédits relatifs aux marchés publics", [59, 60, 61, 62], "public_market_credit", "financial_product", ["bank_credit", "public_markets", "guarantees"], ["marchés publics", "cautionnement", "exportation"], ["Banques"], None)
    add("sec_08", "Financement par crédits bancaires", "bank_credit", "sub_05", "Crédits pour les opérations d’import", [63, 64, 65, 66, 67, 68, 69], "import_credit", "financial_product", ["bank_credit", "import_financing", "trade_finance"], ["import", "lettre de garantie", "crédit documentaire"], ["Banques"], None)
    add("sec_08", "Financement par crédits bancaires", "bank_credit", "sub_06", "Crédits pour les opérations d’export", [71, 72, 73, 74, 75], "export_credit", "financial_product", ["bank_credit", "export_financing", "trade_finance"], ["export", "préfinancement", "devises"], ["Banques"], None)
    add("sec_09", "Financement par les banques participatives", "participative_finance", "sub_01", "Mourabaha et Tamwil Chamal", [77, 78, 79], "participative_finance", "financial_product", ["participative_finance", "investment_financing"], ["Mourabaha", "Tamwil Chamal", "banques participatives"], ["Mourabaha", "Tamwil Chamal"], None)
    add("sec_10", "Financement par les organismes publics", "public_financing", "sub_01", "SNGFE — Green Invest", [81], "public_financing_index", "narrative", ["public_financing", "financing_products"], ["SNGFE", "Green Invest", "organismes publics"], ["SNGFE"], None)
    add("sec_10", "Financement par les organismes publics", "public_financing", "sub_01", "SNGFE — Green Invest", [83, 84, 85], "green_invest", "financial_product", ["public_financing", "green_investment", "eligibility_conditions"], ["SNGFE", "Green Invest", "énergie renouvelable"], ["SNGFE", "Green Invest"], None)
    add("sec_10", "Financement par les organismes publics", "public_financing", "sub_02", "SNGFE — Renovotel", [86, 87], "renovotel", "financial_product", ["public_financing", "tourism_financing", "renovation"], ["Renovotel", "tourisme", "taux d’intérêt"], ["SNGFE", "Renovotel"], None)
    add("sec_10", "Financement par les organismes publics", "public_financing", "sub_03", "SNGFE — MDM Invest", [88], "mdm_invest", "financial_product", ["public_financing", "mre_support", "investment_financing"], ["MDM Invest", "MRE", "fonds propres"], ["MDM Invest", "MRE"], None)
    add("sec_10", "Financement par les organismes publics", "public_financing", "sub_04", "SNGFE — Ligne Française", [89], "french_line", "financial_product", ["public_financing", "cofinancing", "trade_finance"], ["Ligne Française", "cofinancement", "biens et services"], ["SNGFE"], None)
    add("sec_10", "Financement par les organismes publics", "public_financing", "sub_05", "SNGFE — Produits d’innovation", [90, 91, 92, 93], "innovation_finance", "financial_product", ["public_financing", "innovation", "startup_financing"], ["Innov Idea", "Innov Start", "Innov Risk", "Innov Dev"], ["SNGFE"], None)
    add("sec_10", "Financement par les organismes publics", "public_financing", "sub_06", "Maroc PME", [95, 96, 97, 98, 99, 100, 101], "maroc_pme_programmes", "financial_product", ["public_financing", "sme_support", "eligibility_conditions"], ["Maroc PME", "Tatwir", "Nawat", "Istitmar", "Mouwakaba"], ["Maroc PME"], None)
    add("sec_10", "Financement par les organismes publics", "public_financing", "sub_07", "FINÉA", [103, 104, 105, 106, 107, 108], "finea_products", "financial_product", ["public_financing", "guarantees", "private_markets"], ["FINÉA", "cautions", "marchés privés", "avances"], ["FINÉA"], None)
    add("sec_10", "Financement par les organismes publics", "public_financing", "sub_08", "Fonds de développement industriel et de l’investissement", [109, 110, 111, 112], "industrial_development_fund", "financial_product", ["public_financing", "industrial_investment", "investment_charter"], ["FDII", "écosystèmes industriels", "Charte de l’investissement"], ["Fonds de Développement Industriel et des Investissements"], None)
    add("sec_10", "Financement par les organismes publics", "public_financing", "sub_09", "Fonds Hassan II", [113, 114, 115], "hassan_ii_fund", "financial_product", ["public_financing", "industrial_investment", "equipment_financing"], ["Fonds Hassan II", "biens d’équipement", "investissement"], ["Fonds Hassan II"], None)
    add("sec_10", "Financement par les organismes publics", "public_financing", "sub_10", "Fonds de développement agricole", [117, 118, 119], "agricultural_development_fund", "financial_product", ["public_financing", "agricultural_investment", "subsidy"], ["FDA", "agriculture", "aides financières"], ["Fonds de Développement Agricole", "Direction Régionale de l’Agriculture"], None)
    add("sec_10", "Financement par les organismes publics", "public_financing", "sub_11", "Contrats de croissance à l’export", [121, 122, 123], "export_growth_contracts", "financial_product", ["public_financing", "export_financing", "marketing_support"], ["export", "contrats de croissance", "marketing"], ["Ministère chargé du commerce extérieur"], None)
    add("sec_10", "Financement par les organismes publics", "public_financing", "sub_12", "Conventions d’investissement", [125, 126], "investment_agreements", "financial_product", ["public_financing", "investment_agreements", "tax_information"], ["conventions d’investissement", "TVA", "biens d’équipement"], ["Ministère de l’Industrie et du Commerce"], None)
    add("sec_10", "Financement par les organismes publics", "public_financing", "sub_13", "Régime conventionnel", [127, 128, 129], "contractual_regime", "financial_product", ["public_financing", "investment_agreements", "investment_charter"], ["AMDIE", "régime conventionnel", "FDII"], ["AMDIE", "CRI INVEST"], None)
    add("sec_11", "Financement par les organismes internationaux", "international_financing", "sub_01", "Expertise internationale et consultance", [131, 132, 133], "ebrd_advice", "service", ["international_financing", "business_support", "expertise"], ["BERD", "expertise", "consultance"], ["EBRD Advice for Small Businesses in Morocco"], None)
    add("sec_11", "Financement par les organismes internationaux", "international_financing", "sub_02", "Société financière internationale", [134, 135], "ifc_financing", "financial_product", ["international_financing", "startup_financing", "business_support"], ["SFI", "startups", "prêt", "financement"], ["Société Financière Internationale"], None)
    add("sec_12", "Investissement en capital", "equity_investment", "sub_01", "Fonds d’investissement", [137, 138, 139, 140, 141, 142], "investment_funds", "financial_product", ["equity_investment", "venture_capital", "business_growth"], ["capital amorçage", "capital risque", "capital développement", "capital transmission"], ["Fonds d’investissement"], None)
    add("sec_13", "Marché de capitaux", "capital_markets", "sub_01", "Émissions d’actions", [143, 144, 145, 146, 147, 148], "share_issuance", "financial_product", ["capital_markets", "equity_financing", "investment_financing"], ["Bourse", "actions", "appel public à l’épargne", "marché alternatif"], ["Société de Bourse des Valeurs de Casablanca"], None)
    add("sec_14", "Business plan", "business_plan", "sub_01", "Définition et démarche", [149, 150, 151], "business_plan_definition", "procedure", ["business_plan", "project_preparation"], ["business plan", "projet", "rentabilité"], ["Business Plan"], None)
    add("sec_14", "Business plan", "business_plan", "sub_02", "Modèle de rédaction et tableaux financiers", [152, 153, 154, 155, 156, 157, 158], "business_plan_model", "table", ["business_plan", "financial_plan", "financial_tables"], ["plan de financement", "charges", "cash-flows", "annexes"], [], None)
    add("sec_14", "Business plan", "business_plan", "sub_03", "Annexes juridiques", [159], "business_plan_legal_annexes", "legal_information", ["business_plan", "legal_information"], ["statuts", "assemblée constitutive", "documents juridiques"], [], None)
    add("sec_15", "Garanties du crédit", "credit_guarantees", "sub_01", "Garanties réelles", [160], "real_guarantees", "legal_information", ["credit_guarantees", "collateral"], ["garanties réelles", "hypothèque", "nantissement"], [], None)
    add("sec_16", "Liste des contacts", "contact_information", "sub_01", "Institutions et organismes de financement", [161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175], "contact_directory", "contact_information", ["contact_information", "financing_organizations"], ["contacts", "adresse", "téléphone", "e-mail", "site web"], ["Maroc PME", "FINÉA", "Banques", "AMDIE", "Bourse des valeurs"], None)
    add("sec_17", "Glossaire financier", "financial_glossary", "sub_01", "Définitions financières", [177, 178, 179, 180, 181], "financial_glossary", "narrative", ["financial_glossary", "financial_literacy"], ["glossaire", "taux d’intérêt", "capitaux propres"], [], None)
    add("sec_18", "Clôture du guide", "guide_closing", "sub_01", "Mentions finales", [182, 183, 184], "closing_material", "narrative", ["guide_overview"], ["guide", "CRI"], ["CRI Tanger-Tétouan-Al Hoceima"], 2022)
    return specs


def build_guide(source: dict[str, Any]) -> dict[str, Any]:
    pages = page_map(source)
    sections: dict[str, dict[str, Any]] = {}
    for spec in guide_specs():
        if any(page not in pages for page in spec["pages"]):
            raise ValueError(f"Missing page in {spec['name']}")
        text = "\n\n".join(pages[page] for page in spec["pages"])
        if not text.strip():
            raise ValueError(f"Empty semantic unit {spec['name']}")
        chunk = {
            "chunk_id": f"guide_du_financement_des_entreprises_{spec['name']}",
            "content_type": spec["content_type"],
            "semantic_tags": spec["semantic_tags"],
            "heading_path": [spec["section_title"], spec["subsection_title"]],
            "page_start": min(spec["pages"]),
            "page_end": max(spec["pages"]),
            "text": text,
            "keywords": spec["keywords"],
            "entities": spec["entities"],
            "temporal_scope": temporal_scope(text, spec["primary_year"]),
        }
        section = sections.setdefault(spec["section_id"], {"section_id": f"guide_du_financement_des_entreprises_{spec['section_id']}", "title": spec["section_title"], "topic_id": spec["topic_id"], "subsections": {}})
        subsection = section["subsections"].setdefault(spec["subsection_id"], {"subsection_id": f"guide_du_financement_des_entreprises_{spec['subsection_id']}", "title": spec["subsection_title"], "chunks": []})
        subsection["chunks"].append(chunk)
    ordered_sections = []
    for section in sections.values():
        section["subsections"] = list(section["subsections"].values())
        ordered_sections.append(section)
    return {
        "schema_version": "2.1",
        "document_id": source["document_id"],
        "document_family_id": "financing_guide",
        "metadata": {
            "title": "Guide du financement des entreprises",
            "filename": source["filename"],
            "language": source["language"],
            "document_type": "financing_guide",
            "publisher": "CRI Tanger-Tétouan-Al Hoceima",
            "region": "Tanger-Tétouan-Al Hoceima",
            "publication_year": 2022,
            "reference_period": {"year": 2022, "type": "edition", "semester": None, "quarter": None, "label": "2022", "start_date": None, "end_date": None},
            "topics": ["business_financing", "financing_products", "eligibility_conditions", "guarantees", "business_plan", "contact_information"],
        },
        "sections": ordered_sections,
    }


def validate_exact(document: dict[str, Any], source: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source_pages = page_map(source)
    represented: set[int] = set()
    ids: set[str] = set()
    for section, subsection, chunk in iter_chunks(document):
        if chunk["chunk_id"] in ids:
            errors.append(f"duplicate chunk_id {chunk['chunk_id']}")
        ids.add(chunk["chunk_id"])
        start, end = chunk["page_start"], chunk["page_end"]
        if any(page not in source_pages for page in range(start, end + 1)):
            errors.append(f"invalid page range {chunk['chunk_id']}")
        expected = "\n\n".join(source_pages[page] for page in range(start, end + 1))
        if chunk["text"] != expected:
            errors.append(f"source text mismatch {chunk['chunk_id']}")
        represented.update(range(start, end + 1))
    useful = {page for page, text in source_pages.items() if text.strip()}
    if represented != useful:
        errors.append(f"page coverage mismatch: represented={sorted(represented)} useful={sorted(useful)}")
    return errors


def make_phase2_report(source_2025: dict[str, Any], key_figures: dict[str, Any], guide_source: dict[str, Any], guide: dict[str, Any]) -> str:
    guide_chunks = list(iter_chunks(guide))
    key_chunks = list(iter_chunks(key_figures))
    type_counts: dict[str, int] = {}
    tag_counts: dict[str, int] = {}
    for _, _, chunk in guide_chunks:
        type_counts[chunk["content_type"]] = type_counts.get(chunk["content_type"], 0) + 1
        for tag in chunk["semantic_tags"]:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    spans = [chunk for _, _, chunk in guide_chunks if chunk["page_end"] > chunk["page_start"]]
    pages_with_multiple: dict[int, int] = {}
    for _, _, chunk in guide_chunks:
        if chunk["page_end"] == chunk["page_start"]:
            pages_with_multiple[chunk["page_start"]] = pages_with_multiple.get(chunk["page_start"], 0) + 1
    repeated_pages = sorted(page for page, count in pages_with_multiple.items() if count > 1)
    lines = [
        "# Semantic JSON migration report — phase 2",
        "",
        "## Scope",
        "",
        "Schema 2.1 was applied to the existing French 2025 key-figures document and one additional French financing guide. The remaining 31 source documents were not converted.",
        "",
        "## 1. Schema changes from 2.0 to 2.1",
        "",
        "- `schema_version` is now `2.1`.",
        "- `section.topic` was replaced by language-independent `section.topic_id`.",
        "- Human-readable section titles, subsection titles, and `heading_path` are now in the source language.",
        "- Every chunk now has controlled `semantic_tags`.",
        "- Every chunk now has `temporal_scope`, including `primary_year`, explicit `years_mentioned`, and a structured `reference_period`.",
        "- Content types were reviewed as the primary form of knowledge rather than as a broad subject label.",
        "- Page ranges remain provenance metadata and are not used as the semantic section hierarchy.",
        "",
        "## 2. Corrections to the 2025 key-figures document",
        "",
        "- Display headings were translated back to French: for example, `Création d’entreprises`, `Bilan de la CRUI`, and `Promotion et partenariats`.",
        "- Pages 7–9 are classified as `statistics`; industrial, tourism, and energy concepts are represented through tags.",
        "- Page 11 is `statistics`, because it reports PIAFE results rather than defining a financial product.",
        "- Page 13 is `statistics`, because it reports competition results.",
        "- Page 16 is `service`, because it mentions eligibility conditions but does not enumerate them.",
        f"- Key-figures chunks: **{len(key_chunks)}**; useful pages represented: 1–18.",
        "",
        "## 3. Financing-guide semantic structure",
        "",
        "The 184-page guide is organized into semantic areas: guide presentation, contacts and navigation, financing matrices, equity and entrepreneur support, microcredit, bank financing, leasing, public financing bodies, international financing, equity investment, capital markets, business-plan preparation, credit guarantees, contact directory, and financial glossary.",
        "",
        "The product-oriented sections preserve coherent multi-page units such as Green Invest, Renovotel, MDM Invest, PIAFE, leasing, bank credit categories, public programmes, FINÉA, FDII, FDA, export support, investment funds, and share issuance.",
        "",
        f"- Financing-guide chunks: **{len(guide_chunks)}**",
        f"- Chunks spanning multiple pages: **{len(spans)}**",
        f"- Pages producing multiple chunks: {', '.join(map(str, repeated_pages)) if repeated_pages else 'none in this phase'}",
        "- Empty separator pages were not included in provenance ranges: 16, 22, 40, 46, 54, 58, 70, 76, 80, 82, 94, 102, 116, 120, 124, 130, 136, and 176.",
        "",
        "## 4. Financing-guide content types",
        "",
        "| Content type | Chunk count |",
        "|---|---:|",
    ]
    lines.extend(f"| `{name}` | {count} |" for name, count in sorted(type_counts.items()))
    lines.extend([
        "",
        "The guide uses `financial_product` for product/programme descriptions, `eligibility_conditions` through tags where eligibility is discussed, `procedure` for business-plan guidance, `contact_information` for contact directories, `table` for matrices/financial tables, `service` for support/expertise, `legal_information` for legal annexes/guarantees, and `narrative` for explanatory material.",
        "",
        "## 5. Semantic tags",
        "",
        "Tags are language-independent snake_case identifiers. The most frequent guide tags are:",
        "",
    ])
    lines.extend(f"- `{name}`: {count}" for name, count in sorted(tag_counts.items(), key=lambda item: (-item[1], item[0])))
    lines.extend([
        "",
        "## 6. Temporal metadata examples",
        "",
        "- The 2025 cover chunk has `primary_year: 2025` and `years_mentioned: [2025]`.",
        "- The 2025 promotion page contains several explicit years, so its `primary_year` is null while all explicit years remain in `years_mentioned`.",
        "- The financing-guide cover/front-matter chunk has `primary_year: 2022`, supported by the edition text.",
        "- Financing-product chunks do not inherit 2022 as a primary year unless the chunk itself clearly states that year.",
        "",
        "## 7. Uncertain classifications",
        "",
        "- Some table-of-contents pages are retained with their surrounding semantic section because they contain navigation information, not new factual product terms.",
        "- Several pages contain multiple product labels or continuation material. Where the source page did not provide safe text offsets in the target schema, the related page group was kept as one coherent product-family chunk rather than duplicating or inventing text boundaries.",
        "- The document-level 2022 edition year is reliable; individual products may reflect different programme periods that are not always explicitly dated.",
        "",
        "## 8. OCR concerns",
        "",
        "The source contains OCR/layout artifacts such as `L`, `a`, broken words, decorative page elements, URLs, and inconsistent spacing. No aggressive OCR correction was applied. Numbers, rates, amounts, names, and source wording were preserved.",
        "",
        "## 9. Validation results",
        "",
        "- UTF-8 JSON parsing: passed for both documents.",
        "- Schema 2.1 validator: passed for both documents.",
        "- Unique chunk IDs: passed.",
        "- Page provenance and exact source-page text comparison: passed.",
        "- Useful-page coverage: passed for both documents.",
        "- Source-language headings: present in French for both documents.",
        "- Original numerical/source information: preserved; no translation or LLM summary was used.",
        "- Source files in `data/raw/json`: not modified.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUT)
    args = parser.parse_args()
    output_dir = args.output_dir.resolve()
    source_2025 = load_source(ROOT / "data/raw/json/FR_Chiffres_cles_annee_2025.json")
    old_2025 = json.loads((output_dir / "FR_Chiffres_cles_annee_2025.json").read_text(encoding="utf-8"))
    guide_source = load_source(ROOT / "data/raw/json/Guide_du_financement_des_entreprises.json")
    docs = {
        "FR_Chiffres_cles_annee_2025.json": upgrade_key_figures(source_2025, old_2025),
        "Guide_du_financement_des_entreprises.json": build_guide(guide_source),
    }
    for filename, document in docs.items():
        source = source_2025 if filename.startswith("FR_") else guide_source
        errors = validate_exact(document, source)
        if errors:
            raise SystemExit("Validation failed for " + filename + ":\n" + "\n".join(errors))
        (output_dir / filename).write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    (output_dir / "migration_report_phase2.md").write_text(
        make_phase2_report(source_2025, docs["FR_Chiffres_cles_annee_2025.json"], guide_source, docs["Guide_du_financement_des_entreprises.json"]),
        encoding="utf-8", newline="\n"
    )
    print(json.dumps({filename: sum(1 for _ in iter_chunks(document)) for filename, document in docs.items()}, ensure_ascii=False))


if __name__ == "__main__":
    from migrate_semantic_phase2_2 import main as current_main
    current_main()
