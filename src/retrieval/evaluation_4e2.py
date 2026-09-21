"""Phase 4E.2 corrected-encoding evaluation inputs and integrity checks."""
from __future__ import annotations

import re
from typing import Any

from src.retrieval.evaluation_4e1 import BASELINE_DATASET

SUSPICIOUS_MOJIBAKE = ("Ã", "Ø", "Ù", "Â")

CORRECTED_NEGATIVES = [
    {"query_id":"Q051","language":"fr","question":"Quel est le montant du salaire minimum au Japon en 2026 ?"},
    {"query_id":"Q052","language":"en","question":"What is the stock price of Tesla today?"},
    {"query_id":"Q053","language":"ar","question":"\u0645\u0627 \u0647\u0648 \u0633\u0639\u0631 \u0627\u0644\u0646\u0641\u0637 \u0627\u0644\u0639\u0627\u0644\u0645\u064a \u0627\u0644\u064a\u0648\u0645\u061f"},
    {"query_id":"Q054","language":"es","question":"\u00bfCu\u00e1l es el PIB de Espa\u00f1a en 2026?"},
    {"query_id":"Q055","language":"fr","question":"Quelle est la proc\u00e9dure pour obtenir un visa de travail au Canada ?"},
    {"query_id":"N006","language":"fr","question":"Quel est le cours actuel de l'action Apple ?"},
    {"query_id":"N007","language":"fr","question":"Quelle est la m\u00e9t\u00e9o aujourd'hui \u00e0 Paris ?"},
    {"query_id":"N008","language":"fr","question":"Comment demander un visa de travail pour le Canada ?"},
    {"query_id":"N009","language":"fr","question":"Quel est le salaire moyen des infirmiers en Allemagne ?"},
    {"query_id":"N010","language":"fr","question":"Quels sont les sympt\u00f4mes et le traitement du diab\u00e8te ?"},
    {"query_id":"N011","language":"en","question":"What is the current price of Brent crude oil?"},
    {"query_id":"N012","language":"en","question":"How can I obtain a work visa for Australia?"},
    {"query_id":"N013","language":"en","question":"What is the weather forecast in London today?"},
    {"query_id":"N014","language":"en","question":"What is the average salary of teachers in Canada?"},
    {"query_id":"N015","language":"en","question":"What medication should I take for a migraine?"},
    {"query_id":"N016","language":"ar","question":"\u0645\u0627 \u0647\u0648 \u0633\u0639\u0631 \u0627\u0644\u0630\u0647\u0628 \u0627\u0644\u064a\u0648\u0645 \u0641\u064a \u062f\u0628\u064a\u061f"},
    {"query_id":"N017","language":"ar","question":"\u0643\u064a\u0641 \u064a\u0645\u0643\u0646 \u0627\u0644\u062d\u0635\u0648\u0644 \u0639\u0644\u0649 \u062a\u0623\u0634\u064a\u0631\u0629 \u0639\u0645\u0644 \u0625\u0644\u0649 \u0641\u0631\u0646\u0633\u0627\u061f"},
    {"query_id":"N018","language":"ar","question":"\u0645\u0627 \u0647\u064a \u062a\u0648\u0642\u0639\u0627\u062a \u0627\u0644\u0637\u0642\u0633 \u0627\u0644\u064a\u0648\u0645 \u0641\u064a \u0627\u0644\u0642\u0627\u0647\u0631\u0629\u061f"},
    {"query_id":"N019","language":"ar","question":"\u0645\u0627 \u0647\u0648 \u0645\u062a\u0648\u0633\u0637 \u0631\u0627\u062a\u0628 \u0627\u0644\u0623\u0637\u0628\u0627\u0621 \u0641\u064a \u0623\u0644\u0645\u0627\u0646\u064a\u0627\u061f"},
    {"query_id":"N020","language":"ar","question":"\u0645\u0627 \u0647\u0648 \u0639\u0644\u0627\u062c \u0627\u0644\u062a\u0647\u0627\u0628 \u0627\u0644\u0645\u0641\u0627\u0635\u0644\u061f"}
]


def corrected_queries() -> list[dict[str, Any]]:
    import json
    baseline = json.loads(BASELINE_DATASET.read_text(encoding="utf-8"))["queries"]
    answerable = [item for item in baseline if item.get("category") != "no_answer"]
    output = []
    for item in answerable:
        output.append(item)
    for item in CORRECTED_NEGATIVES:
        output.append({**item, "category":"no_answer", "explicit_year":None, "expected_topics":[], "expected_document_families":[], "acceptable_languages":[item["language"]]})
    return output


def validate_unicode_dataset(queries: list[dict[str, Any]]) -> dict[str, Any]:
    failures = []
    arabic_letters = re.compile(r"[\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff]")
    for query in queries:
        text = query["question"]
        markers = [marker for marker in SUSPICIOUS_MOJIBAKE if marker in text]
        if markers:
            failures.append({"query_id":query["query_id"],"reason":"mojibake_marker","markers":markers})
        if query["language"] == "ar" and not arabic_letters.search(text):
            failures.append({"query_id":query["query_id"],"reason":"missing_arabic_letters"})
        if query["language"] in {"fr","es"} and any(marker in text for marker in ("Ã", "Â", "Ø", "Ù")):
            failures.append({"query_id":query["query_id"],"reason":"latin_query_contains_mojibake"})
    return {"status":"PASS" if not failures else "FAIL", "query_count":len(queries), "failures":failures}

