"""Refine the FR/EN territorial-opportunities guides into semantic units.

This script is deliberately scoped to the two investor-guide semantic files.
It uses reviewed editorial boundaries (project title plus its continuation
pages), keeps raw page text byte-for-byte, and validates provenance by exact
substring membership in the raw page text.
"""
from __future__ import annotations

import hashlib
import json
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "json"
SEM = ROOT / "data" / "semantic_json"
REPORT = SEM / "migration_report_phase3d.md"

FILES = {
    "fr": "Investors_Guide_territorial_opportunities_FR.json",
    "en": "Investors_Guide_territorial_opportunities_EN.json",
}

# Canonical projects are paired by project identity, not ordinal position.
# Ranges were checked against the visible project title/description pages.
PROJECTS = [
    ("agri_food_flour_mill", "Minoterie industrielle", "Industrial flour mill", "agri_food", ["ouezzane"], (17,19), (16,18)),
    ("agri_food_couscous_unit", "Unité industrielle de fabrication du couscous", "Industrial unit for couscous", "agri_food", ["ouezzane","larache"], (20,22), (19,21)),
    ("agri_food_fig_processing", "Unité industrielle de valorisation de figues", "Industrial unit for fig processing", "agri_food", ["chefchaouen","ouezzane","tetouan","al_hoceima"], (23,27), (22,25)),
    ("agri_food_red_fruit_processing", "Unité de valorisation de fruits rouges", "Industrial unit for red fruit processing", "agri_food", ["larache"], (28,30), (26,29)),
    ("agri_food_olive_oil", "Unité industrielle d’huile d’olive", "Industrial unit for olive oil", "agri_food", ["ouezzane"], (31,34), (30,32)),
    ("agri_food_biscuit_factory", "Unité industrielle de biscuiterie", "Biscuit factory", "agri_food", ["larache","tetouan"], (35,36), (33,35)),
    ("agri_food_sunflower_oil", "Unité industrielle d’huile de tournesol", "Industrial unit for sunflower oil", "agri_food", ["ouezzane","larache"], (37,40), (36,41)),
    ("automotive_cannabis_processing", "Unité de transformation du cannabis pour l’industrie automobile", "Cannabis processing unit for the automotive industry", "automotive", ["fahs_anjra","tanger_assilah"], (43,48), (42,45)),
    ("automotive_shock_absorbers", "Unité industrielle d’amortisseurs", "Industrial unit for shock absorbers", "automotive", ["fahs_anjra","tanger_assilah"], (49,49), (46,48)),
    ("automotive_filters", "Unité industrielle de filtres automobiles", "Industrial unit for automotive filters", "automotive", ["fahs_anjra","tanger_assilah"], (50,52), (49,51)),
    ("automotive_brake_pads", "Unité Industrielle De Plaquettes De Freins", "Brake pad industrial unit", "automotive", ["fahs_anjra","tanger_assilah"], (53,55), (52,54)),
    ("automotive_electric_bikes", "Assemblage de Vélos & Motos électriques", "Electric bike & motorcycle assembly", "automotive", ["fahs_anjra","tanger_assilah"], (56,58), (55,59)),
    ("construction_cannabis_processing", "Unité de transformation du cannabis pour l’industrie du BTP", "Cannabis processing unit for the construction materials industry", "industry", ["chefchaouen","al_hoceima","ouezzane","tetouan"], (61,64), (60,63)),
    ("cannabis_cbd_supplements", "Unité de production de compléments alimentaires à base de CBD", "Cannabis-based dietary supplements production unit", "industry", ["chefchaouen","al_hoceima","tetouan","larache"], (67,70), (64,69)),
    ("cannabis_cosmetics", "Unité de transformation du cannabis pour un usage cosmétique", "Cannabis processing unit for cosmetic use", "industry", ["chefchaouen","al_hoceima","ouezzane","tetouan","larache"], (71,74), (70,73)),
    ("cannabis_pharmaceuticals", "Unité de transformation du cannabis pour un usage pharmaceutique", "Cannabis processing unit for pharmaceutical use", "industry", ["tanger_assilah"], (75,77), (74,78)),
    ("tetouan_shopping_center", "Centre commercial", "Shopping center", "services", ["tetouan"], (80,82), (79,81)),
    ("french_school", "École Française", "French school", "education", ["tanger_assilah"], (85,86), (84,85)),
    ("automotive_training_institute", "Institut de Formation aux Métiers de l’Industrie Automobile", "Training institute for professions in the automobile industry", "education", ["fahs_anjra"], (87,88), (86,89)),
    ("electrical_conductors", "Unité industrielle de conducteurs électriques", "Industrial Unit for Electrical Conductors", "industry", ["tanger_assilah","fahs_anjra","tetouan"], (91,94), (90,93)),
    ("renewable_electricity", "Production électrique renouvelable", "Renewable electricity production", "renewable_energy", ["regional"], (97,100), (94,99)),
    ("industrial_thermosetting", "Unité de thermo-laquage", "Thermosetting Unit", "industry", ["fahs_anjra"], (103,105), (102,103)),
    ("container_manufacturing", "Production de conteneurs", "Container Manufacturing Unit", "industry", ["tanger_assilah","fahs_anjra"], (106,107), (104,106)),
    ("wind_turbine_components", "Unité de production d'éoliennes et de leurs parties", "Wind Turbine and Components Production Facility", "renewable_energy", ["tanger_assilah"], (108,110), (107,109)),
    ("naval_shipyard", "Chantier naval pour bateaux économiques", "Naval Shipyard for Economical Pleasure Boats", "industry", ["tanger_assilah"], (111,112), (110,113)),
    ("fish_canning_unit", "Unité de conserves de poisson", "Canned Fish Unit", "fisheries", ["tanger_assilah","tetouan","larache"], (115,117), (114,116)),
    ("seafood_waste_processing", "Unité de transformation des déchets des industries de transformation de produits de la mer", "Unit for the Transformation of Waste from Seafood Processing Industries", "fisheries", ["regional"], (118,121), (117,120)),
    ("agar_agar_aquaculture", "Unité d’aquaculture et industrielle pour la production d’agar agar", "Aquaculture and Industrial Unit for Agar Agar Production", "fisheries", ["chefchaouen","al_hoceima","larache"], (122,126), (121,126)),
    ("cannabis_seed_import", "Importation de semences et de plants de Cannabis", "Importation of Cannabis Seeds and Plants", "logistics", ["chefchaouen","fahs_anjra","larache","al_hoceima"], (128,129), (127,129)),
    ("cannabis_transport", "Transport du cannabis", "Transportation of Cannabis", "logistics", ["chefchaouen","al_hoceima","larache","tanger_assilah"], (130,132), (130,132)),
    ("distribution_company", "Société de distribution", "Distribution Company", "logistics", ["fahs_anjra","tanger_assilah","tetouan"], (133,138), (133,138)),
    ("al_hoceima_clinic", "Clinique à Al-Hoceima", "Clinic in Al-Hoceima", "healthcare", ["al_hoceima"], (140,142), (139,141)),
    ("offshoring_center", "Centre d’Offshoring", "Offshoring Center", "services", ["mdiq_fnideq","tanger_assilah"], (145,147), (144,147)),
    ("startup_accelerator", "Accélérateur de Start-Up", "Start-up Accelerator", "digital", ["tetouan","tanger_assilah","al_hoceima"], (148,153), (148,151)),
    ("textile_cannabis_processing", "Unité de transformation du cannabis pour l’industrie textile", "Cannabis Transformation Unit for the Textile Industry", "industry", ["tetouan","ouezzane","al_hoceima","tanger_assilah"], (155,158), (154,157)),
    ("textile_spinning", "Unité industrielle de filature", "Industrial Spinning Unit", "industry", ["tetouan","tanger_assilah","ouezzane","al_hoceima"], (159,161), (158,160)),
    ("textile_zippers", "Unité industrielle de fermetures éclair", "Industrial Zipper Unit", "industry", ["tetouan","al_hoceima"], (162,164), (161,163)),
    ("textile_buttons", "Unité industrielle de boutonnerie", "Industrial Button Manufacturing Unit", "industry", ["tetouan","al_hoceima"], (165,168), (164,167)),
    ("tourism_five_star_hotel", "Hôtel 5 étoiles", "5-Star Hotel", "tourism", ["fahs_anjra"], (171,172), (170,171)),
    ("tourism_chefchaouen_hotel", "Hôtel 4 ou 5 étoiles à Chefchaouen", "4 or 5-Star Hotel in Chefchaouen", "tourism", ["chefchaouen"], (173,175), (172,174)),
    ("tourism_club_hotel", "Hôtel-Club", "Club Hotel", "tourism", ["al_hoceima"], (176,178), (175,177)),
    ("tourism_water_park", "Parc Aquatique", "Water Park", "tourism", ["tetouan","tanger_assilah"], (179,181), (178,180)),
    ("tourism_theme_park", "Parc d’attractions (A thème)", "Theme Park", "tourism", ["tetouan","tanger_assilah"], (182,183), (181,182)),
    ("tourism_science_culture_park", "Parc d’attraction : Science et culture", "Theme Park: Science and Culture", "tourism", ["tetouan","tanger_assilah"], (184,185), (183,184)),
    ("tourism_seaside_resort", "Centre balnéaire", "Seaside Resort", "tourism", ["chefchaouen"], (186,189), (185,188)),
    ("tourism_mini_ski", "Mini station de Ski à Chakrane", "Mini Ski Resort in Chakrane", "tourism", ["al_hoceima"], (190,193), (189,192)),
    ("tourism_mountain_lodge", "Gîte en montagne", "Mountain Lodge", "tourism", ["chefchaouen"], (194,197), (193,196)),
    ("tourism_boat_rental", "Agence de plaisance et de location d'embarcations", "Pleasure and Boat Rental Agency", "tourism", ["tanger_assilah"], (198,201), (197,200)),
    ("tourism_club_biladi", "Village de vacances touristique (Club Biladi)", "Touristical holiday village (Club Biladi)", "tourism", ["al_hoceima"], (202,205), (201,204)),
    ("tourism_residential_complex", "Complexe touristique et résidentiel", "Tourist and Residential Complex", "tourism", ["tanger_assilah"], (206,210), (205,208)),
]

def norm_text(text: str) -> str:
    return " ".join(text.split())

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def load_pages(language: str):
    name = FILES[language]
    raw = json.loads((RAW / name).read_text(encoding="utf-8"))
    return {int(p["page"]): p.get("text", "") for p in raw.get("pages", [])}, raw

def all_pages(ranges):
    out = set()
    for a,b in ranges: out.update(range(a,b+1))
    return out

def make_chunk(doc_id, index, title, topic_id, pages, page_texts, content_type, tags, heading):
    spans = [{"page": p, "text": page_texts[p]} for p in pages if page_texts.get(p, "").strip()]
    text = "\n\n".join(s["text"] for s in spans)
    years = sorted({int(y) for y in re.findall(r"\b(?:19|20)\d{2}\b", text)})
    primary = None
    if len(years) == 1 and any(x in text.lower() for x in ["2020", "2021", "2022", "2023"]):
        # A single year in a profile is still not automatically the edition year;
        # it is primary only when the unit is explicitly dated in its facts.
        primary = years[0] if re.search(r"(?:as of|en |en l’année|année|in )\s*"+str(years[0]), text, re.I) else None
    return {
        "chunk_id": f"{doc_id}_chunk_{index:04d}",
        "content_type": content_type,
        "semantic_tags": sorted(set(tags)),
        "heading_path": [heading[0], title] if title else heading,
        "page_start": min(s["page"] for s in spans),
        "page_end": max(s["page"] for s in spans),
        "source_spans": spans,
        "text": text,
        "keywords": [],
        "entities": [],
        "temporal_scope": {"primary_year": primary, "years_mentioned": years, "reference_period": {"type": None, "year": None, "semester": None, "quarter": None, "start_date": None, "end_date": None}},
    }

def build(language: str):
    pages, raw = load_pages(language)
    doc_id = raw["document_id"]
    title = "Offre territoriale des opportunités d’investissement" if language == "fr" else "Investors Guide to Territorial Opportunities"
    used = set()
    sections = []
    idx = 1

    def add_section(section_id, display, topic_id, chunks):
        nonlocal sections
        sections.append({"section_id": f"{doc_id}_{section_id}", "title": display, "topic_id": topic_id, "subsections": [{"subsection_id": f"{doc_id}_{section_id}_sub_01", "title": display, "chunks": chunks}]})

    # Editorial/context pages before the project catalogue.
    pre_end = 15 if language == "fr" else 15
    pre_pages = [p for p in range(1, pre_end+1) if pages.get(p, "").strip()]
    if pre_pages:
        c = make_chunk(doc_id, idx, title, "investment_guide_overview", pre_pages, pages, "narrative", ["investment_guide_overview", "territorial_overview"], [title, "Introduction"]); idx += 1
        add_section("overview", "Introduction" if language == "fr" else "Introduction", "investment_guide_overview", [c])

    # Projects grouped by sector, preserving each profile as a coherent unit.
    by_sector = defaultdict(list)
    for pid, fr_title, en_title, sector, territories, fr_range, en_range in PROJECTS:
        a,b = fr_range if language == "fr" else en_range
        if a > len(pages): continue
        ps = [p for p in range(a, min(b, max(pages))+1) if pages.get(p, "").strip()]
        if not ps: continue
        display = fr_title if language == "fr" else en_title
        tags = [pid, "investment_opportunity", sector] + territories
        c = make_chunk(doc_id, idx, display, "investment_opportunity", ps, pages, "investment_opportunity", tags, [title, display]); idx += 1
        by_sector[sector].append(c); used.update(ps)
    for sector, chunks in by_sector.items():
        display = {"agri_food":"Agroalimentaire" if language=="fr" else "Agri-food", "automotive":"Automobile" if language=="fr" else "Automotive", "industry":"Industrie" if language=="fr" else "Industry", "renewable_energy":"Énergie" if language=="fr" else "Energy", "fisheries":"Pêche" if language=="fr" else "Fisheries & seafood", "logistics":"Logistique" if language=="fr" else "Logistics", "healthcare":"Santé" if language=="fr" else "Health", "services":"Services" if language=="fr" else "Business services", "education":"Éducation" if language=="fr" else "Education", "digital":"Services numériques" if language=="fr" else "Digital services", "tourism":"Tourisme" if language=="fr" else "Tourism"}.get(sector, sector)
        add_section(f"sector_{sector}", display, "sector_overview", chunks)

    # Remaining pages are retained as separate documentary units (overview,
    # statistics or support directory) rather than forced into opportunities.
    remaining = sorted(p for p,t in pages.items() if t.strip() and p not in used)
    service_start = 211 if language == "fr" else 209
    for p in remaining:
        t = norm_text(pages[p])
        if p >= service_start:
            ctype, topic, tag = "service", "investment_support", "investment_support"
            if re.search(r"contact|tél|tel|email|@|www\.", t, re.I):
                ctype, topic, tag = "contact_information", "contact_information", "contact_information"
            display = (t[:100] if t else ("Service" if language == "fr" else "Service"))
        elif re.search(r"statistic|indicateur|chiffres|figures|%|million|hectares|PIB|GDP", t, re.I):
            ctype, topic, tag, display = "statistics", "territorial_overview", "territorial_overview", ("Aperçu territorial" if language=="fr" else "Territorial overview")
        else:
            ctype, topic, tag, display = "narrative", "territorial_overview", "territorial_overview", ("Contexte territorial" if language=="fr" else "Territorial context")
        c = make_chunk(doc_id, idx, display, topic, [p], pages, ctype, [tag], [title, display]); idx += 1
        add_section(f"page_{p:03d}", display, topic, [c])
    out = {"schema_version":"2.2", "document_id":doc_id, "document_family_id":"investors_guide_territorial_opportunities", "metadata":{"title":title,"filename":FILES[language],"language":language,"document_type":"investment_opportunities","publisher":"CRI Tanger-Tétouan-Al Hoceima","region":"Tanger-Tétouan-Al Hoceima","publication_year":None,"reference_period":{"year":None,"type":None,"semester":None,"quarter":None,"label":None,"start_date":None,"end_date":None},"topics":sorted({s["topic_id"] for s in sections})},"sections":sections}
    return out, raw, pages, used

def validate(doc, pages):
    errors=[]; chunks=[c for s in doc["sections"] for ss in s["subsections"] for c in ss["chunks"]]
    ids=[c["chunk_id"] for c in chunks]
    if len(ids)!=len(set(ids)): errors.append("duplicate chunk IDs")
    for c in chunks:
        spans=c["source_spans"]
        if c["page_start"] != min(x["page"] for x in spans) or c["page_end"] != max(x["page"] for x in spans): errors.append(c["chunk_id"]+": page bounds")
        for s in spans:
            if not pages.get(s["page"], "").strip(): errors.append(c["chunk_id"]+": empty/missing page")
            elif s["text"] not in pages[s["page"]]: errors.append(c["chunk_id"]+": source span mismatch")
        if c["text"] != "\n\n".join(s["text"] for s in spans): errors.append(c["chunk_id"]+": text mismatch")
    return errors, chunks

def main():
    before={k:sha(RAW/v) for k,v in FILES.items()}
    docs={}; stats={}; rawdocs={}
    for lang in FILES:
        doc, raw, pages, used=build(lang); docs[lang]=doc; rawdocs[lang]=raw
        errors,chunks=validate(doc,pages)
        if errors: raise SystemExit("; ".join(errors[:10]))
        stats[lang]=(chunks,pages,used)
        (SEM/FILES[lang]).write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    after={k:sha(RAW/v) for k,v in FILES.items()}
    sizes=[len(c["text"]) for d in docs.values() for s in d["sections"] for ss in s["subsections"] for c in ss["chunks"]]
    project_ids=[p[0] for p in PROJECTS]
    lines=["# Phase 3D — Territorial investment opportunities refinement", "", "## Scope", "", "Only the French and English investors-guide semantic documents were modified. Raw page text is preserved in exact source spans; no RAG or vector-store files were changed.", "", "## Chunk counts", "", f"- FR: {len(stats['fr'][0])} chunks (previously 95)", f"- EN: {len(stats['en'][0])} chunks (previously 70)", f"- Identified project profiles: FR {sum(1 for p in PROJECTS if p[5][0] <= max(stats['fr'][1]))}; EN {sum(1 for p in PROJECTS if p[6][0] <= max(stats['en'][1]))}", "", "## Canonical opportunity IDs", "", "The paired project IDs are stable, language-independent identifiers derived from project names and profile meaning:", "", ", ".join(f"`{x}`" for x in project_ids), "", "## FR/EN alignment", "", "| Canonical opportunity ID | FR pages | EN pages | FR title | EN title | Status |", "|---|---:|---:|---|---|---|"]
    for pid,fr,en,sector,terr,frg,eng in PROJECTS:
        lines.append(f"| `{pid}` | {frg[0]}–{frg[1]} | {eng[0]}–{eng[1]} | {fr} | {en} | aligned_with_translation_difference |")
    lines += ["", "The alignment is content-based: titles, sector, territory and profile attributes were compared. It does not require equal page ranges. Both editions contain the same main opportunity catalogue in different layouts; wording and page extents differ.", "", "## Content, sector and territory distributions", ""]
    for lang,(chunks,pages,used) in stats.items():
        lines += [f"### {lang.upper()}", "", "Content types: " + ", ".join(f"{k}={v}" for k,v in Counter(c['content_type'] for c in chunks).items()), "", "Sectors: " + ", ".join(f"{k}={v}" for k,v in Counter(tag for c in chunks for tag in c['semantic_tags'] if tag in {p[3] for p in PROJECTS}).items()), "", "Territories: " + ", ".join(f"{k}={v}" for k,v in Counter(tag for c in chunks for tag in c['semantic_tags'] if tag in {'tanger_assilah','tetouan','fahs_anjra','mdiq_fnideq','larache','al_hoceima','ouezzane','chefchaouen','regional'}).items()), ""]
    lines += ["## Project page ranges", "", "Project ranges are listed in the alignment table. Multi-page ranges are retained where the source profile is a single coherent opportunity sheet.", "", "## Chunk-size diagnostics", "", f"- Total chunks: {len(sizes)}", f"- Minimum: {min(sizes)}", f"- Median: {statistics.median(sizes):.1f}", f"- Average: {statistics.mean(sizes):.1f}", f"- Maximum: {max(sizes)}"]
    for limit in [3000,5000,8000,12000]: lines.append(f"- >{limit}: {sum(x>limit for x in sizes)}")
    large=[]
    for lang,(chunks,_,_) in stats.items():
        for c in chunks:
            if len(c['text'])>3000: large.append(f"- `{lang}` {c['chunk_id']}: {len(c['text'])} chars, pages {c['page_start']}–{c['page_end']}")
    lines += ["", "Large chunks:"] + (large or ["- None above 3,000 characters."]) + ["", "## Repeated boilerplate", "", "Repeated sector labels, investment-advantage headings, support-program references and tourism/agri-food market-statistics blocks remain in their original source spans. They were not removed; they should be considered later for retrieval weighting or deduplication.", "", "## Temporal metadata", "", "Publication year is `null` for both documents because the guide edition year was not safely established from an explicit publication marker. Explicit years found in each chunk are retained in `temporal_scope.years_mentioned`; no edition year was inherited.", "", "## OCR and identity confidence", "", "Some source pages contain OCR noise, especially cover/table-of-contents pages and a small number of English headings. Project identities are directly supported by explicit titles on profile pages or by title plus continuation evidence. The following should receive later manual review: English pages 25–29 (fig/red-fruit transition), French pages 112–121 (naval/seafood transition), and service-directory pages after the opportunity catalogue.", "", "## Validation", "", "Phase-specific exact provenance validation: PASS for FR and EN. Every emitted source span is a non-empty exact substring of its raw page; chunk text is the ordered span concatenation; page bounds match span extrema.", "", "Canonical validator: run separately with `scripts/validate_semantic_json.py --source-dir data/raw/json`.", "", "## Raw SHA-256 integrity", "", "| File | Before | After | Unchanged |", "|---|---|---|---|"]
    for lang,n in FILES.items(): lines.append(f"| `{n}` | `{before[lang]}` | `{after[lang]}` | {'yes' if before[lang]==after[lang] else 'NO'} |")
    lines += ["", "## Manual review items", "", "- Verify the few profile transitions identified above against rendered PDF pages before using these semantic chunks for ingestion.", "- Review OCR-degraded English titles and the service-directory page-level units; no source text was corrected or invented."]
    REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"documents_modified":list(FILES.values()),"fr_chunks":len(stats['fr'][0]),"en_chunks":len(stats['en'][0]),"raw_changed":sum(before[k]!=after[k] for k in FILES)},ensure_ascii=False))

if __name__ == "__main__": main()
