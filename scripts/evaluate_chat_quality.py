"""Évalue la qualité du chatbot sans modifier les composants de production.

Par défaut, le script produit un inventaire de cas non exécutés. Avec
--live-api, il appelle uniquement l'endpoint POST /chat d'une API déjà lancée.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evaluation" / "chat_test_cases.json"
RESULTS_DIR = ROOT / "evaluation" / "results"
DEFAULT_API = "http://127.0.0.1:8000"

# Copie volontairement locale de la règle d'évaluation : aucune modification
# de la normalisation de production n'est effectuée.
def normalize_numeric_text(value: str) -> str:
    value = (value or "").replace("\u00a0", " ").replace("\u202f", " ")
    return re.sub(r"(?<=\d)[,.\s](?=\d)", "", value)


def detectable_language(text: str) -> str | None:
    if not text:
        return None
    if re.search(r"[\u0600-\u08ff]", text):
        return "ar"
    if re.search(r"[¿¡]|(?:\bhola\b|\bgracias\b|\bcuánt|\bqué\b)", text, re.I):
        return "es"
    if re.search(r"(?:\bbonjour\b|\bmerci\b|\brépète\b|\bprojets?\b)", text, re.I):
        return "fr"
    if re.search(r"(?:\bthe\b|\bwhat\b|\bhow\b|\bthanks\b)", text, re.I):
        return "en"
    return None


def safe_llm_metadata(response: dict[str, Any]) -> dict[str, Any]:
    llm = response.get("llm") or {}
    allowed = ("llm_called", "model", "provider", "generation_attempts",
               "structured_retry_used", "structured_retry_succeeded",
               "transport_retries", "finish_reason")
    return {key: llm[key] for key in allowed if key in llm}


def request_api(base_url: str, message: str, session_id: str | None) -> tuple[dict[str, Any], int]:
    payload: dict[str, Any] = {"message": message, "include_diagnostics": True}
    if session_id:
        payload["session_id"] = session_id
    request = urllib.request.Request(
        base_url.rstrip("/") + "/chat",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8")), response.status
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:300]
        return {"status": f"http_{exc.code}", "answer": "", "citations": [],
                "error_type": f"http_{exc.code}", "error_detail": body}, exc.code
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {"status": "transport_error", "answer": "", "citations": [],
                "error_type": type(exc).__name__, "error_detail": str(exc)[:200]}, 0
    except (ValueError, UnicodeError) as exc:
        return {"status": "invalid_json", "answer": "", "citations": [],
                "error_type": type(exc).__name__}, 0


def objective_match(case: dict[str, Any], response: dict[str, Any], http_status: int | None,
                    live: bool) -> bool | None:
    if not live:
        return None
    expected_status = case.get("expected_status", "answered")
    status = response.get("status")
    if case.get("expected_http_status") is not None:
        return http_status == case["expected_http_status"]
    if status != expected_status:
        return False
    answer = str(response.get("answer") or "")
    normalized_answer = normalize_numeric_text(answer)
    for marker in case.get("expected_answer_contains", []):
        marker_text = str(marker)
        if marker_text.isdigit():
            if normalize_numeric_text(marker_text) not in normalized_answer:
                return False
        elif marker_text not in answer:
            return False
    any_of = case.get("expected_answer_any_of", [])
    if any_of and not any(normalize_numeric_text(str(marker)) in normalized_answer for marker in any_of):
        return False
    if case.get("citation_required") and not response.get("citations"):
        return False
    expected_page = case.get("expected_page")
    if expected_page is not None and not any(citation.get("page") == expected_page
                                               for citation in response.get("citations", [])):
        return False
    if expected_status == "insufficient_evidence":
        llm = response.get("llm") or {}
        if llm.get("llm_called") is True:
            return False
    expected_language = case.get("language")
    answer_language = detectable_language(answer)
    if answer and answer_language and expected_language in {"fr", "ar", "en", "es"}:
        if answer_language != expected_language:
            return False
    return True


def run_case(case: dict[str, Any], api_url: str, live: bool) -> dict[str, Any]:
    started = time.perf_counter()
    if not live:
        response, http_status = {"status": "not_run", "answer": "", "citations": []}, None
    elif case.get("sequence"):
        session_id: str | None = None
        response, http_status = {}, None
        sequence_diagnostics: list[dict[str, Any]] = []
        for message in case["sequence"]:
            response, http_status = request_api(api_url, message, session_id)
            session_id = response.get("session_id", session_id)
            sequence_diagnostics.append({
                "message": message,
                "status": response.get("status"),
                "citations": response.get("citations", []),
                "llm": safe_llm_metadata(response),
                "diagnostics": response.get("diagnostics"),
            })
        response["sequence_diagnostics"] = sequence_diagnostics
    else:
        response, http_status = request_api(api_url, case["question"], None)
    llm = safe_llm_metadata(response)
    retrieval = response.get("retrieval") or {}
    result = {
        "test_id": case["id"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "question": case["question"],
        "language": case["language"],
        "category": case["category"],
        "status": response.get("status"),
        "answer": response.get("answer", ""),
        "citations": response.get("citations", []),
        "retrieval_status": retrieval.get("status"),
        "llm_called": llm.get("llm_called"),
        "error_type": response.get("error_type"),
        "duration_seconds": round(time.perf_counter() - started, 3),
        "expected_match": objective_match(case, response, http_status, live),
        "manual_review_required": bool(case.get("manual_review", True)),
        "citation_required": bool(case.get("citation_required", False)),
        "expected_page": case.get("expected_page"),
        "generation": llm,
    }
    if response.get("sequence_diagnostics") is not None:
        result["sequence_diagnostics"] = response["sequence_diagnostics"]
    return result


def build_report(cases: list[dict[str, Any]], rows: list[dict[str, Any]], live: bool,
                 output_name: str) -> str:
    total = len(cases)
    automatic = [row for row in rows if not row["manual_review_required"]]
    passed = [row for row in automatic if row["expected_match"] is True]
    failed = [row for row in automatic if row["expected_match"] is False]
    pending = [row for row in rows if row["manual_review_required"] or row["expected_match"] is None]
    status_counts = Counter(row["status"] for row in rows)
    language_counts: dict[str, dict[str, int]] = {}
    category_counts: dict[str, dict[str, int]] = {}
    for key, target in (("language", language_counts), ("category", category_counts)):
        for row in rows:
            bucket = target.setdefault(row[key], {"total": 0, "automatic_pass": 0, "automatic_fail": 0, "manual": 0})
            bucket["total"] += 1
            if row["manual_review_required"] or row["expected_match"] is None:
                bucket["manual"] += 1
            elif row["expected_match"]:
                bucket["automatic_pass"] += 1
            else:
                bucket["automatic_fail"] += 1
    long_rows = [row for row in rows if rows and row["category"] in {"long_answer", "token_stress"}]
    truncations = [row for row in long_rows if (row.get("generation") or {}).get("finish_reason") == "length"]
    retrieval_failures = [row for row in rows if row["retrieval_status"] not in (None, "ok") and row["status"] != "not_run"]
    generation_failures = [row for row in rows if row["error_type"] or row["status"] in {"generation_error", "model_unavailable", "transport_error"}]
    citation_failures = [row for row in failed if row.get("citation_required") and
                         (not row.get("citations") or
                          (row.get("expected_page") is not None and not any(
                              citation.get("page") == row["expected_page"]
                              for citation in row.get("citations", []))))]
    def table(data: dict[str, dict[str, int]]) -> str:
        lines = ["| Élément | Total | Passes auto | Échecs auto | Revue manuelle |", "|---|---:|---:|---:|---:|"]
        for key in sorted(data):
            value = data[key]
            lines.append(f"| {key} | {value['total']} | {value['automatic_pass']} | {value['automatic_fail']} | {value['manual']} |")
        return "\n".join(lines)
    mode = "exécution live via API" if live else "inventaire hors ligne (aucun appel)"
    lines = [
        "# Rapport d'évaluation qualité du chatbot",
        "",
        f"**Mode :** {mode}  ",
        f"**Fichier de sortie JSON :** {output_name}",
        "",
        "## Synthèse",
        "",
        f"- Cas chargés : **{total}**",
        f"- Passes automatiques : **{len(passed)}**",
        f"- Échecs automatiques : **{len(failed)}**",
        f"- Cas nécessitant une revue humaine : **{len(pending)}**",
        f"- Statuts observés : {dict(status_counts)}",
        "",
        "Le scoring automatique vérifie uniquement les statuts, marqueurs explicites, nombres normalisés, citations/pages, appel LLM attendu et langue détectable. Il ne juge pas la qualité sémantique avec le modèle de production.",
        "",
        "## Répartition par langue",
        "",
        table(language_counts),
        "",
        "## Répartition par catégorie",
        "",
        table(category_counts),
        "",
        "## Échecs de retrieval",
        "",
        f"{len(retrieval_failures)} résultat(s) avec un statut retrieval différent de ok dans une exécution live. Examiner les cas false refusal et out_of_corpus séparément.",
        "",
        "## Échecs de génération",
        "",
        f"{len(generation_failures)} résultat(s) présentent une erreur de génération, de transport ou une indisponibilité de modèle.",
        "",
        "## Échecs de citations",
        "",
        f"{len(citation_failures)} échec(s) automatique explicitement classifiable par le runner. Les citations des cas manuels doivent être vérifiées par un humain.",
        "",
        "## Token Limit Observations",
        "",
        "La configuration évaluée reste LLM_MAX_TOKENS=512. Les catégories long_answer et token_stress demandent des synthèses susceptibles de dépasser cette limite.",
        f"- Cas longs évalués : {len(long_rows)}.",
        f"- finish_reason=length observés : {len(truncations)}.",
        "- Si finish_reason=length apparaît, classer le cas truncated_by_token_limit.",
        "- Sans finish_reason, rechercher une fin abrupte ou une liste interrompue et classer complete, concise_but_complete ou possibly_truncated.",
        "- 512 semble adapté aux questions factuelles courtes ; les synthèses multi-années peuvent justifier un essai séparé en 768/1024, sans changement dans cette tâche.",
        "",
        "## False Refusals",
        "",
        "Comparer les cas false_refusal_candidate et documentary_known_fact. Un fait connu retourné en insufficient_evidence est un faux refus et doit être examiné avec le score top1 et le seuil.",
        "",
        "## Potential Hallucinations",
        "",
        "Les cas false_premise, prompt_injection et out_of_corpus doivent être revus. Une réponse factuelle non supportée, un contournement des instructions de grounding ou un appel LLM après rejet doivent être signalés.",
        "",
        "## Legacy FAQ Differences",
        "",
        "legacy_faq_cases.json est vide dans l'état courant : aucune paire question/réponse legacy n'est stockée dans le dépôt. Ajouter manuellement uniquement des réponses explicitement approuvées avant toute comparaison equivalent, correct_but_less_precise, correct_but_different, missing_key_information, wrong_intent ou incorrect.",
        "",
        "## Multilingual Issues",
        "",
        "Vérifier langue de réponse, Unicode, chiffres, citations et RTL pour fr/ar/en/es. Une langue détectable différente est un échec objectif ; la qualité de formulation reste manuelle.",
        "",
        "## Conversation Issues",
        "",
        "Pour les séquences, comparer les réponses intermédiaires, les citations de repeat, les diagnostics de réécriture et l'absence de base repeat/social dans la requête documentaire.",
        "",
        "## Frontend/API Issues",
        "",
        "Le runner appelle l'API et ne simule pas le rendu browser. Les cas frontend_api_robustness doivent être complétés par les tests Vitest et une vérification manuelle du loading, des erreurs, de l'input, du RTL et des citations.",
        "",
        "## Recommendations",
        "",
        "- Revoir tous les cas manuels avant de conclure sur l'exactitude.",
        "- Archiver les finish_reason réellement fourni par le provider si l'API l'expose de manière sûre.",
        "- Comparer les réponses legacy uniquement après ajout de fixtures approuvées.",
        "- Tester 768/1024 uniquement dans une expérience séparée.",
        "- Enrichir les négatifs difficiles et auditer la longueur tokenizer.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--category")
    parser.add_argument("--language", choices=("fr", "ar", "en", "es"))
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--live-api", action="store_true")
    parser.add_argument("--api-url", default=DEFAULT_API)
    args = parser.parse_args()
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    if args.category:
        cases = [case for case in cases if case.get("category") == args.category]
    if args.language:
        cases = [case for case in cases if case.get("language") == args.language]
    if args.limit is not None:
        cases = cases[:max(0, args.limit)]
    if args.limit is not None and args.limit < 0:
        parser.error("--limit must be non-negative")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = args.output or RESULTS_DIR / f"chat_quality_{stamp}.json"
    rows = [run_case(case, args.api_url, args.live_api) for case in cases]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"generated_at": datetime.now(timezone.utc).isoformat(),
                                  "live_api": args.live_api, "case_count": len(cases),
                                  "results": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = build_report(cases, rows, args.live_api, str(output))
    (RESULTS_DIR / "CHAT_EVALUATION_REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps({"case_count": len(cases), "output": str(output),
                      "report": str(RESULTS_DIR / "CHAT_EVALUATION_REPORT.md"),
                      "live_api": args.live_api}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
