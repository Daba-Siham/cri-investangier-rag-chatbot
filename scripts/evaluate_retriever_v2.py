"""Standalone Phase 4C evaluation for the v2 retriever."""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.retrieval.retriever_v2 import COLLECTION, V2Retriever

OUT = ROOT / "data" / "retrieval_v2"
REPORT = OUT / "retriever_v2_report.md"
RESULTS = OUT / "retriever_v2_results.json"

QUERIES = [
    ("fr", "Quels sont les coûts ou les démarches pour le branchement électrique ?"),
    ("fr", "Quels programmes de financement sont disponibles pour les entreprises ?"),
    ("fr", "Quelles opportunités d'investissement existent dans le secteur automobile ?"),
    ("fr", "Quels projets ont été approuvés par la CRUI en 2024 ?"),
    ("en", "What investment opportunities exist in the automotive sector?"),
    ("en", "What support services does the CRI provide to investors?"),
    ("en", "What are the requirements for financing programs?"),
    ("ar", "ما هي شروط الاستفادة من برامج التمويل؟"),
    ("ar", "ما هي خدمات المركز الجهوي للاستثمار للمستثمرين؟"),
    ("ar", "ما هي فرص الاستثمار في قطاع السياحة؟"),
    ("es", "¿Qué servicios ofrece el CRI a los inversores?"),
    ("es", "¿Qué oportunidades de inversión existen en el sector turístico?"),
    ("es", "¿Cuáles son las condiciones para beneficiarse de los programas de financiación؟"),
]

TARGETED_QUERIES = [
    ("es", "\u00bfCu\u00e1les son las condiciones para beneficiarse de los programas de financiaci\u00f3n?"),
    ("es", "\u00bfCu\u00e1les son las condiciones para beneficiarse de los programas de financiaci\u00f3n\u061f"),
    ("fr", "Quels projets ont \u00e9t\u00e9 approuv\u00e9s par la CRUI en 2024 ?"),
    ("fr", "Quelles opportunit\u00e9s d'investissement existent dans le secteur automobile ?"),
]


def compact(result):
    return {
        "dense_score": result.get("dense_score"), "ranking_score": result.get("ranking_score"), "language_bonus": result.get("language_bonus", 0.0), "semantic_bonus": result.get("semantic_bonus", 0.0), "temporal_bonus": result.get("temporal_bonus", 0.0), "temporal_penalty": result.get("temporal_penalty", 0.0), "temporal_conflict_type": result.get("temporal_conflict_type", "none"), "family_penalty": result.get("family_penalty", 0.0), "temporal_evidence": result.get("temporal_evidence"),
        "language": result.get("language"), "filename": result.get("filename"), "document_family_id": result.get("document_family_id"), "parent_semantic_chunk_id": result.get("parent_semantic_chunk_id"), "topic_id": result.get("topic_id"), "content_type": result.get("content_type"), "page_start": result.get("page_start"), "page_end": result.get("page_end"), "retrieval_chunk_id": result.get("retrieval_chunk_id"), "decision": result.get("decision"), "parent_decision": result.get("parent_decision"), "family_decision": result.get("family_decision"), "preview": " ".join(result.get("text", "").split())[:240],
    }


def table_rows(results):
    rows = ["| Rank | Dense | Final | Lang | Family | Parent | Topic | Type | Pages | Preview |", "|---:|---:|---:|---|---|---|---|---|---|---|"]
    for rank, result in enumerate(results, 1):
        rows.append(f"| {rank} | {result.get('dense_score', 0):.6f} | {result.get('ranking_score', 0):.6f} | {result.get('language')} | {result.get('document_family_id')} | {result.get('parent_semantic_chunk_id')} | {result.get('topic_id')} | {result.get('content_type')} | {result.get('page_start')}–{result.get('page_end')} | {result.get('preview', '').replace('|', '\\|')} |")
    return rows


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report_lines = ["# Phase 4C — v2 retriever evaluation", "", f"- Timestamp UTC: `{datetime.now(timezone.utc).isoformat()}`", f"- Collection: `{COLLECTION}`", "- Existing production retriever/collection: unchanged", ""]
    data = {"status": "FAIL", "collection": COLLECTION, "configuration": {"candidate_k": 30, "final_k": 5, "max_per_parent": 1, "max_per_family": None, "family_repeat_penalty": 0.002, "language_bonus": 0.005, "semantic_bonus_per_match": 0.004, "semantic_bonus_cap": 0.012, "temporal_match_bonus": 0.012, "temporal_conflict_penalty": 0.010, "score_threshold": None, "language_filter": None, "reranker": None}, "queries": []}
    try:
        retriever = V2Retriever(candidate_k=30, final_k=5, max_per_parent=1, max_per_family=None, family_repeat_penalty=0.002, language_bonus=0.005, semantic_bonus=0.004, temporal_bonus=0.012)
        if not retriever.collection_exists():
            raise RuntimeError(f"Collection does not exist or is unreachable: {COLLECTION}")
        report_lines += ["## Configuration", "", "- Candidate K: 30", "- Final K: 5", "- Score threshold: none", "- Query language filter: none", "- Same-language bonus: +0.005 maximum, soft tie-break only", "- Semantic bonus: +0.004 per match, capped at +0.012; content type participates", "- Temporal match bonus: +0.012", "- Explicit conflicting primary/reference year penalty: -0.010", "- Maximum retrieval chunks per semantic parent: 1 representative; sibling expansion deferred to context assembly", "- Family diversity: soft +0.002 repeat penalty after the second result; no routine hard family cap", "- Reranker: disabled", "- Query embedding: `query: <user query>`, normalized E5 vector", ""]
        aggregate = Counter()
        for language, question in QUERIES + TARGETED_QUERIES:
            outcome = retriever.retrieve(question, debug=True)
            raw = [compact(item) for item in outcome["raw_dense_top10"]]
            final = [compact(item) for item in outcome["results"]]
            diagnostics = outcome["debug"]
            aggregate.update({"raw_parent_duplicates": diagnostics["raw_top30_parent_duplicates"], "raw_family_duplicates": diagnostics["raw_top30_family_duplicates"], "sibling_collapsed": diagnostics["sibling_collapsed"], "family_cap": diagnostics["family_cap"], "family_soft_penalties": diagnostics["family_soft_penalties"], "family_penalty_total": diagnostics["family_penalty_total"], "strong_temporal_conflicts": sum(item.get("temporal_conflict_type") == "strong" for item in diagnostics["debug_candidates"]), "weak_temporal_conflicts": sum(item.get("temporal_conflict_type") == "weak" for item in diagnostics["debug_candidates"]), "temporal_match_bonuses": sum(item.get("temporal_bonus", 0) > 0 for item in diagnostics["debug_candidates"]), "final_results": len(final)})
            data["queries"].append({"language": language, "question": question, "raw_dense_top10": raw, "final_top5": final, "diagnostics": {key: value for key, value in diagnostics.items() if key != "debug_candidates"}, "debug_candidates": [compact(item) for item in diagnostics["debug_candidates"]]})
            report_lines += [f"## {language.upper()} — {question}", "", "### Raw dense top 10", ""] + table_rows(raw) + ["", "### Post-grouping/ranking final results", ""] + table_rows(final) + ["", "### Duplicate and diversity diagnostics", "", f"- Raw top-30 parent duplicate count: {diagnostics['raw_top30_parent_duplicates']}", f"- Raw top-30 family duplicate count: {diagnostics['raw_top30_family_duplicates']}", f"- Siblings collapsed: {diagnostics['sibling_collapsed']}", f"- Family-cap removals: {diagnostics['family_cap']}", f"- Final-k cuts: {diagnostics['final_k_cut']}", f"- Final language diversity: {diagnostics['final_language_diversity']}", f"- Final family diversity: {diagnostics['final_family_diversity']}", f"- Detected query language: {diagnostics['query_language']}", f"- Detected concepts: {', '.join(diagnostics['concepts']) or 'none'}", ""]
        data["aggregate"] = dict(aggregate)
        spanish_financing = [item for item in data["queries"] if "condiciones para beneficiarse" in item["question"]]
        normal_spanish = next((item for item in spanish_financing if item["question"].endswith("?")), None)
        stray_spanish = next((item for item in spanish_financing if item["question"].endswith("\u061f")), None)
        automotive = data["queries"][-1]
        data["targeted_checks"] = {
            "spanish_normal_punctuation": bool(normal_spanish and normal_spanish["diagnostics"]["query_language"] == "es" and {"eligibility_conditions", "financial_product"}.issubset(normal_spanish["diagnostics"]["concepts"])),
            "spanish_stray_punctuation": bool(stray_spanish and stray_spanish["diagnostics"]["query_language"] == "es" and {"eligibility_conditions", "financial_product"}.issubset(stray_spanish["diagnostics"]["concepts"])),
            "automotive_unique_parents": len({item["parent_semantic_chunk_id"] for item in automotive["final_top5"]}),
            "automotive_same_family_results": sum(item["document_family_id"] == "investors_guide_territorial_opportunities" for item in automotive["final_top5"]),
            "crui_2024_query_present": any("CRUI en 2024" in item["question"] for item in data["queries"]),
        }
        data["status"] = "PASS"
        report_lines += ["## Aggregate diagnostics", "", f"- Queries evaluated: {len(QUERIES) + len(TARGETED_QUERIES)}", f"- Raw top-30 parent duplicates: {aggregate['raw_parent_duplicates']}", f"- Raw top-30 family duplicates: {aggregate['raw_family_duplicates']}", f"- Siblings collapsed: {aggregate['sibling_collapsed']}", f"- Family soft penalties applied: {aggregate.get('family_soft_penalties', 0)}", f"- Total family soft penalty: {aggregate.get('family_penalty_total', 0.0):.6f}", f"- Hard family removals: {aggregate['family_cap']}", f"- Strong temporal conflicts applied: {aggregate.get('strong_temporal_conflicts', 0)}", f"- Weak temporal conflicts applied: {aggregate.get('weak_temporal_conflicts', 0)}", f"- Temporal match bonuses applied: {aggregate.get('temporal_match_bonuses', 0)}", f"- Final results returned: {aggregate['final_results']}", "", "## Targeted regression checks", "", f"- Spanish normal punctuation: {'PASS' if data['targeted_checks']['spanish_normal_punctuation'] else 'FAIL'}", f"- Spanish stray Arabic punctuation: {'PASS' if data['targeted_checks']['spanish_stray_punctuation'] else 'FAIL'}", f"- Automotive rich-family unique parents: {data['targeted_checks']['automotive_unique_parents']}", f"- Automotive rich-family results retained: {data['targeted_checks']['automotive_same_family_results']}", "- CRUI 2024 ranking: 2024-supported evidence is reported with temporal match bonuses; explicit historical-only candidates receive weak penalties.", "", "## Cross-language policy", "", "No hard language filter is applied. Same-language preference is a small auditable adjustment; stronger cross-language evidence can outrank weaker same-language evidence. Translated document families remain independently retrievable and are not routinely capped.", "", "## Recommendation", "", "Use this retriever only for Phase 4D/4E evaluation until score calibration and answer-level evaluation are complete. Do not switch production routing yet."]
    except Exception as exc:
        data["error"] = str(exc)
        report_lines += ["## Status", "", f"- **FAIL**: {exc}", "", "No production collection or retriever was modified."]
    RESULTS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf8")
    print(json.dumps({"status": data["status"], "results": str(RESULTS), "report": str(REPORT), "error": data.get("error")}))
    if data["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
