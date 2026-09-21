"""Phase 4E.1 evaluation-only abstention and temporal experiments."""
from __future__ import annotations

import json
import re
import statistics
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BASELINE_DATASET = ROOT / "data" / "retrieval_v2" / "eval_queries_v1_v2.json"
BASELINE_RESULTS = ROOT / "data" / "retrieval_v2" / "eval_v1_v2_results.json"

NEW_NEGATIVES = [
    {"query_id":"N006","language":"fr","question":"Quel est le cours actuel de l'action Apple ?","category":"no_answer","explicit_year":None},
    {"query_id":"N007","language":"fr","question":"Quelle est la mÃ©tÃ©o aujourd'hui Ã  Paris ?","category":"no_answer","explicit_year":None},
    {"query_id":"N008","language":"fr","question":"Comment demander un visa de travail pour le Canada ?","category":"no_answer","explicit_year":None},
    {"query_id":"N009","language":"fr","question":"Quel est le salaire moyen des infirmiers en Allemagne ?","category":"no_answer","explicit_year":None},
    {"query_id":"N010","language":"fr","question":"Quels sont les symptÃ´mes et le traitement du diabÃ¨te ?","category":"no_answer","explicit_year":None},
    {"query_id":"N011","language":"en","question":"What is the current price of Brent crude oil?","category":"no_answer","explicit_year":None},
    {"query_id":"N012","language":"en","question":"How can I obtain a work visa for Australia?","category":"no_answer","explicit_year":None},
    {"query_id":"N013","language":"en","question":"What is the weather forecast in London today?","category":"no_answer","explicit_year":None},
    {"query_id":"N014","language":"en","question":"What is the average salary of teachers in Canada?","category":"no_answer","explicit_year":None},
    {"query_id":"N015","language":"en","question":"What medication should I take for a migraine?","category":"no_answer","explicit_year":None},
    {"query_id":"N016","language":"ar","question":"Ù…Ø§ Ù‡Ùˆ Ø³Ø¹Ø± Ø§Ù„Ø°Ù‡Ø¨ Ø§Ù„ÙŠÙˆÙ… ÙÙŠ Ø¯Ø¨ÙŠØŸ","category":"no_answer","explicit_year":None},
    {"query_id":"N017","language":"ar","question":"ÙƒÙŠÙ ÙŠÙ…ÙƒÙ† Ø§Ù„Ø­ØµÙˆÙ„ Ø¹Ù„Ù‰ ØªØ£Ø´ÙŠØ±Ø© Ø¹Ù…Ù„ Ø¥Ù„Ù‰ ÙØ±Ù†Ø³Ø§ØŸ","category":"no_answer","explicit_year":None},
    {"query_id":"N018","language":"ar","question":"Ù…Ø§ Ù‡ÙŠ ØªÙˆÙ‚Ø¹Ø§Øª Ø§Ù„Ø·Ù‚Ø³ Ø§Ù„ÙŠÙˆÙ… ÙÙŠ Ø§Ù„Ù‚Ø§Ù‡Ø±Ø©ØŸ","category":"no_answer","explicit_year":None},
    {"query_id":"N019","language":"ar","question":"Ù…Ø§ Ù‡Ùˆ Ù…ØªÙˆØ³Ø· Ø±Ø§ØªØ¨ Ø§Ù„Ø£Ø·Ø¨Ø§Ø¡ ÙÙŠ Ø£Ù„Ù…Ø§Ù†ÙŠØ§ØŸ","category":"no_answer","explicit_year":None},
    {"query_id":"N020","language":"ar","question":"Ù…Ø§ Ù‡Ùˆ Ø¹Ù„Ø§Ø¬ Ø§Ù„ØªÙ‡Ø§Ø¨ Ø§Ù„Ù…ÙØ§ØµÙ„ØŸ","category":"no_answer","explicit_year":None},
]


def expanded_queries() -> list[dict[str, Any]]:
    base = json.loads(BASELINE_DATASET.read_text(encoding="utf-8"))["queries"]
    existing = {item["query_id"] for item in base}
    additions = []
    for item in NEW_NEGATIVES:
        if item["query_id"] in existing:
            continue
        additions.append({**item, "expected_topics": [], "expected_document_families": [], "acceptable_languages": [item["language"]]})
    return base + additions


def is_strict_year_query(query: dict[str, Any]) -> bool:
    if not query.get("explicit_year"):
        return False
    lowered = query["question"].casefold()
    comparative = ("between", "from ", " to ", "evolution", "growth", "trend", "historical", "entre ", " et ", "Ã©volution", "croissance", "historique", "Ø¨ÙŠÙ† ", "Ù…Ù† ", "Ø¥Ù„Ù‰ ")
    return not any(token in lowered for token in comparative)


def temporal_status(item: dict[str, Any], year: int) -> str:
    scope = item.get("temporal_scope") or {}
    ref = scope.get("reference_period") or {}
    primary = scope.get("primary_year")
    ref_year = ref.get("year") or item.get("reference_period_year")
    years = scope.get("years_mentioned") or item.get("years_mentioned") or []
    if year == primary or year == ref_year or year in years:
        return "requested"
    if primary or ref_year or years:
        return "conflicting"
    return "undated"


def experimental_temporal_context(context: dict[str, Any], query: dict[str, Any]) -> dict[str, Any]:
    """Evaluation-only strict-year context policy; retrieval is untouched."""
    year = query.get("explicit_year")
    if not year or not is_strict_year_query(query):
        return {**context, "experimental_temporal_policy": "not_applicable"}
    evidence = context.get("evidence", [])
    statuses = [temporal_status(item, year) for item in evidence]
    requested_exists = "requested" in statuses
    if not requested_exists:
        return {**context, "experimental_temporal_policy": "no_requested_year_evidence", "temporal_statuses": statuses}
    kept = [item for item, status in zip(evidence, statuses) if status != "conflicting"]
    citations = []
    for index, item in enumerate(kept, 1):
        clone = dict(item)
        clone["evidence_id"] = f"E{index}"
        kept[index - 1] = clone
        citations.append({"citation_id": f"C{index}", "evidence_id": f"E{index}", "retrieval_chunk_id": item["retrieval_chunk_id"], "document_id": item["document_id"], "document_family_id": item["document_family_id"], "filename": item["filename"], "document_title": item["document_title"], "language": item["language"], "page_start": item["page_start"], "page_end": item["page_end"], "source_pages": item["source_pages"], "source_spans": item["source_spans"]})
    context_text = "\n\n".join(context["context_text"].split("\n\n")[:0]) if False else "\n\n".join(
        f"[{item['evidence_id']}]\nDocument: {item['document_title']}\nLanguage: {item['language']}\nPages: {item['page_start']}â€“{item['page_end']}\nTopic: {item.get('topic_id') or ''}\nContent:\n{item['text']}" for item in kept)
    diagnostics = dict(context.get("diagnostics", {}))
    diagnostics.update({"final_evidence_units": len(kept), "context_characters": len(context_text), "experimental_conflicting_removed": statuses.count("conflicting")})
    return {**context, "context_text": context_text, "evidence": kept, "citations": citations, "diagnostics": diagnostics, "experimental_temporal_policy": "requested_year_first_conflicts_removed", "temporal_statuses": statuses}


def margin(scores: list[float]) -> float | None:
    return scores[0] - scores[1] if len(scores) >= 2 else None


def threshold_analysis(rows: list[dict[str, Any]], system: str, score_key: str, thresholds: list[float]) -> list[dict[str, Any]]:
    output = []
    for threshold in thresholds:
        positives = [row for row in rows if row["query"]["category"] != "no_answer"]
        negatives = [row for row in rows if row["query"]["category"] == "no_answer"]
        def accept(row):
            return bool(row[system][score_key] and row[system][score_key][0] >= threshold)
        tp, fp = sum(accept(row) for row in positives), sum(accept(row) for row in negatives)
        recall = tp / len(positives) if positives else 0.0
        rejection = 1 - fp / len(negatives) if negatives else 0.0
        precision = tp / (tp + fp) if tp + fp else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        output.append({"threshold": threshold, "answerable_acceptance_recall": recall, "no_answer_rejection": rejection, "false_acceptance_rate": fp / len(negatives) if negatives else None, "false_rejection_rate": 1 - recall, "balanced_accuracy": (recall + rejection) / 2, "precision_answerable": precision, "f1": f1})
    return output


def margin_analysis(rows: list[dict[str, Any]], system: str, score_key: str, thresholds: list[float], margins: list[float]) -> list[dict[str, Any]]:
    output = []
    for threshold in thresholds:
        for min_margin in margins:
            positives = [row for row in rows if row["query"]["category"] != "no_answer"]
            negatives = [row for row in rows if row["query"]["category"] == "no_answer"]
            def accept(row):
                scores = row[system][score_key]
                return bool(scores and scores[0] >= threshold and margin(scores) is not None and margin(scores) >= min_margin)
            tp, fp = sum(accept(row) for row in positives), sum(accept(row) for row in negatives)
            recall = tp / len(positives) if positives else 0.0
            rejection = 1 - fp / len(negatives) if negatives else 0.0
            output.append({"threshold": threshold, "minimum_margin": min_margin, "answerable_recall": recall, "no_answer_rejection": rejection, "balanced_accuracy": (recall + rejection) / 2})
    return output

