"""Phase 4D context, provenance, citation, and regression evaluation."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.retrieval.context_builder_v2 import ContextBuilderV2, ProvenanceStore, render_citation
from src.retrieval.retriever_v2 import V2Retriever

OUT = ROOT / "data" / "retrieval_v2"
REPORT = OUT / "context_v2_report.md"
RESULTS = OUT / "context_v2_results.json"

QUERIES = [
    ("fr", "Quels sont les coûts ou les démarches pour le branchement électrique ?"),
    ("fr", "Quels projets ont été approuvés par la CRUI en 2024 ?"),
    ("en", "What investment opportunities exist in the automotive sector?"),
    ("ar", "ما هي شروط الاستفادة من برامج التمويل؟"),
    ("es", "¿Qué servicios ofrece el CRI a los inversores?"),
    ("es", "¿Cuáles son las condiciones para beneficiarse de los programas de financiación?"),
    ("es", "¿Cuáles son las condiciones para beneficiarse de los programas de financiación؟"),
]


def _compact_evidence(item):
    return {key: item[key] for key in (
        "evidence_id", "retrieval_chunk_id", "parent_semantic_chunk_id", "document_id",
        "document_family_id", "filename", "document_title", "language", "topic_id",
        "content_type", "page_start", "page_end", "source_pages", "text", "source_spans",
        "dense_score", "ranking_score", "expanded_from_sibling")}


def _query_row(language, question, retrieval, context):
    debug = retrieval["debug"]
    return {
        "language_expected": language,
        "question": question,
        "detected_language": debug.get("query_language"),
        "concepts": debug.get("concepts", []),
        "retrieval_results_received": len(retrieval["results"]),
        "raw_dense_top10": retrieval["raw_dense_top10"],
        "final_retrieval": retrieval["results"],
        "context": {
            "context_text": context["context_text"],
            "evidence": [_compact_evidence(item) for item in context["evidence"]],
            "citations": context["citations"],
            "diagnostics": context["diagnostics"],
            "rendered_citations": [render_citation(item) for item in context["citations"]],
        },
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    report = ["# Phase 4D — v2 context and citation evaluation", "", f"- Timestamp UTC: `{datetime.now(timezone.utc).isoformat()}`", "- Production retriever, Qdrant collections, and generation path: unchanged", ""]
    result = {"status": "FAIL", "queries": [], "configuration": {"max_evidence_units": 6, "max_context_characters": 12000, "sibling_expansion": "at most one adjacent child, same parent, content-aware", "provenance_source": "data/retrieval_v2/retrieval_chunks.jsonl"}}
    try:
        store = ProvenanceStore()
        builder = ContextBuilderV2(store=store, max_evidence_units=6, max_context_characters=12000, expand_siblings=True)
        retriever = V2Retriever(candidate_k=30, final_k=5, max_per_parent=1, max_per_family=None, family_repeat_penalty=0.002, language_bonus=0.005, semantic_bonus=0.004, temporal_bonus=0.012)
        if not retriever.collection_exists():
            raise RuntimeError("v2 Qdrant collection is unavailable")
        rows = []
        aggregate = {"primary_results_received": 0, "primary_results_kept": 0, "primary_results_dropped_budget": 0, "siblings_considered": 0, "siblings_added": 0, "siblings_skipped_capacity": 0, "siblings_skipped_budget": 0, "siblings_skipped_nonindexable": 0, "duplicates_removed": 0, "context_build_failures": 0, "cross_language_cases": 0, "citation_count": 0}
        for expected_language, question in QUERIES:
            retrieval = retriever.retrieve(question, debug=True)
            context = builder.build(retrieval, query=question, query_language=retrieval["debug"].get("query_language"))
            row = _query_row(expected_language, question, retrieval, context)
            rows.append(row)
            for key in ("primary_results_received", "primary_results_kept", "primary_results_dropped_budget", "siblings_considered", "siblings_added", "siblings_skipped_capacity", "siblings_skipped_budget", "siblings_skipped_nonindexable", "duplicates_removed"):
                aggregate[key] += context["diagnostics"][key]
            report += [f"- Primary IDs: {', '.join(context['diagnostics']['primary_retrieval_chunk_ids'])}", f"- Primary IDs preserved: {', '.join(context['diagnostics']['primary_ids_preserved'])}", f"- Optional sibling IDs added: {', '.join(context['diagnostics']['optional_sibling_ids_added']) or 'none'}", f"- Siblings considered/skipped capacity/skipped budget/skipped non-indexable: {context['diagnostics']['siblings_considered']}/{context['diagnostics']['siblings_skipped_capacity']}/{context['diagnostics']['siblings_skipped_budget']}/{context['diagnostics']['siblings_skipped_nonindexable']}", ""]
            aggregate["citation_count"] += len(context["citations"])
            if any(item["language"] != retrieval["debug"].get("query_language") for item in context["evidence"]):
                aggregate["cross_language_cases"] += 1
            report += [f"## {expected_language.upper()} — {question}", "", f"- Detected query language: `{row['detected_language']}`", f"- Concepts: `{', '.join(row['concepts']) or 'none'}`", f"- Retrieval results received: {row['retrieval_results_received']}", f"- Evidence units: {context['diagnostics']['final_evidence_units']}", f"- Siblings added: {context['diagnostics']['siblings_added']}", f"- Duplicates removed: {context['diagnostics']['duplicates_removed']}", f"- Context characters: {context['diagnostics']['context_characters']} / 12000", f"- Citations: {len(context['citations'])}", f"- Languages cited: {', '.join(sorted({item['language'] for item in context['evidence']}))}", f"- Pages: {', '.join(render_citation(item) for item in context['citations']) or 'none'}", "", "### Citations", "", *[f"- {render_citation(item)}" for item in context["citations"]], ""]
        result["queries"] = rows
        result["aggregate"] = aggregate

        normal = rows[5]
        stray = rows[6]
        spanish_pass = all(row["detected_language"] == "es" and {"eligibility_conditions", "financial_product"}.issubset(row["concepts"]) for row in (normal, stray))
        temporal = rows[1]["final_retrieval"]
        supported = [item["ranking_score"] for item in temporal if item.get("temporal_bonus", 0) > 0]
        conflicts = [item["ranking_score"] for item in temporal if item.get("temporal_conflict_type") in {"strong", "weak"}]
        temporal_pass = bool(supported) and (not conflicts or max(supported) >= max(conflicts))
        cross_language_pass = aggregate["cross_language_cases"] > 0
        primary_priority_pass = all(item["context"]["diagnostics"]["primary_results_dropped_budget"] == 0 and item["context"]["diagnostics"]["primary_results_dropped_capacity"] == 0 and item["context"]["diagnostics"]["primary_results_received"] == item["context"]["diagnostics"]["primary_results_kept"] for item in rows)
        no_nonindexable_sibling = all(all(not evidence["expanded_from_sibling"] or store.get(evidence["retrieval_chunk_id"]).get("indexable", False) for evidence in item["context"]["evidence"]) for item in rows)
        sibling_metrics_consistent = all(item["context"]["diagnostics"]["siblings_added"] == len(item["context"]["diagnostics"]["optional_sibling_ids_added"]) and item["context"]["diagnostics"]["final_evidence_units"] == len(item["context"]["evidence"]) for item in rows)
        result["assertions"] = {"spanish_regressions": spanish_pass, "spanish_normal_language": normal["detected_language"] == "es", "spanish_stray_language": stray["detected_language"] == "es", "spanish_concepts": {"eligibility_conditions", "financial_product"}.issubset(normal["concepts"]) and {"eligibility_conditions", "financial_product"}.issubset(stray["concepts"]), "temporal_crui_2024": temporal_pass, "cross_language_citation_case": cross_language_pass, "primary_evidence_priority": primary_priority_pass, "no_nonindexable_sibling": no_nonindexable_sibling, "sibling_metrics_consistent": sibling_metrics_consistent, "all_contexts_within_budget": all(item["context"]["diagnostics"]["context_characters"] <= 12000 for item in rows), "citation_validation": all(item["context"]["diagnostics"]["provenance_validation"] == "PASS" for item in rows)}
        result["status"] = "PASS" if all(result["assertions"].values()) else "FAIL"
        report += ["## Aggregate priority diagnostics", "", f"- Primary results received: {aggregate['primary_results_received']}", f"- Primary results retained: {aggregate['primary_results_kept']}", f"- Primary results dropped because of budget: {aggregate['primary_results_dropped_budget']}", f"- Siblings considered: {aggregate['siblings_considered']}", f"- Siblings actually added: {aggregate['siblings_added']}", f"- Siblings skipped for capacity: {aggregate['siblings_skipped_capacity']}", f"- Siblings skipped for budget: {aggregate['siblings_skipped_budget']}", f"- Non-indexable siblings skipped: {aggregate['siblings_skipped_nonindexable']}", ""]
        report += ["## Aggregate validation", "", f"- Provenance artifact SHA-256: `{store.jsonl_sha256}`", f"- Retrieval records loaded: {len(store.records)}", f"- Sibling expansions: {aggregate['siblings_added']}", f"- Duplicate evidence units removed: {aggregate['duplicates_removed']}", f"- Cross-language citation cases: {aggregate['cross_language_cases']}", f"- Citation validation pass rate: {sum(row['context']['diagnostics']['provenance_validation'] == 'PASS' for row in rows)}/{len(rows)}", "", "## Regression assertions", "", *[f"- {name}: {'PASS' if value else 'FAIL'}" for name, value in result["assertions"].items()], "", "## Provenance policy", "", "Qdrant results are resolved only through the SHA-verified retrieval JSONL. Source spans are clipped using stored parent offsets and are never inferred from fuzzy text matching. Evidence preserves the original source language; no translation or LLM call is performed."]
    except Exception as exc:
        result["error"] = str(exc)
        report += ["## Status", "", f"- **FAIL**: {exc}"]
    RESULTS.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "report": str(REPORT), "results": str(RESULTS), "error": result.get("error")}))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
