"""UTF-8 API conversation smoke test using one explicit session."""
import argparse, json, sys, urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://127.0.0.1:8000"

def chat(message, session_id=None, diagnostics=False):
    payload = {"message": message, "include_diagnostics": diagnostics}
    if session_id: payload["session_id"] = session_id
    request = urllib.request.Request(BASE_URL + "/chat", data=json.dumps(payload, ensure_ascii=False).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request) as response: return json.loads(response.read().decode("utf-8"))

def check(condition, message):
    if not condition: raise AssertionError(message)

def main(strict=False):
    first = chat("hi my name is siham")
    check(first["status"] == "answered" and first.get("kind") == "social", "step 1 is not social")
    session_id = first["session_id"]
    documentary = chat("Combien de projets ont été approuvés par la CRUI au premier semestre 2024 ?", session_id, True)
    check("379" in documentary.get("answer", ""), "French answer does not contain 379")
    repeated = chat("repeat", session_id)
    check("379" in repeated.get("answer", "") and repeated["citations"] == documentary["citations"], "repeat changed answer/citations")
    followup = chat("Et en 2025 ?", session_id, True)
    follow_diag = followup.get("diagnostics") or {}
    check(followup["session_id"] == session_id and follow_diag.get("query_rewrite_used") is True, "follow-up was not rewritten")
    check(follow_diag.get("retrieval_query") != "Et en 2025 ?", "follow-up used raw retrieval query")
    if strict:
        query = follow_diag.get("retrieval_query", "")
        check("repeat" not in query.casefold() and "2025" in query and "crui" in query.casefold(), "follow-up context is invalid")
    arabic = chat("\u0643\u0645 \u0639\u062f\u062f \u0627\u0644\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u062a\u064a \u0648\u0627\u0641\u0642\u062a \u0639\u0644\u064a\u0647\u0627 \u0627\u0644\u0644\u062c\u0646\u0629 \u0627\u0644\u062c\u0647\u0648\u064a\u0629 \u0627\u0644\u0645\u0648\u062d\u062f\u0629 \u0644\u0644\u0627\u0633\u062a\u062b\u0645\u0627\u0631 \u062e\u0644\u0627\u0644 \u0633\u0646\u0629 2023", session_id, True)
    if strict:
        check(arabic["status"] == "answered" and "709" in arabic.get("answer", ""), "Arabic strict check failed")
        check(any(c.get("page") == 25 for c in arabic.get("citations", [])), "Arabic citation page is not 25")
    weather = chat("What is the weather today?", session_id, True)
    check(weather["status"] == "insufficient_evidence" and (weather.get("llm") or {}).get("llm_called") is False, "weather check failed")
    print(json.dumps({"session_id": session_id, "social": first["status"], "french_answer": documentary.get("answer"), "repeat_citations_preserved": repeated["citations"] == documentary["citations"], "followup_retrieval_query": follow_diag.get("retrieval_query"), "followup_query_rewrite_used": follow_diag.get("query_rewrite_used"), "arabic": {"status": arabic.get("status"), "answer": arabic.get("answer"), "llm": arabic.get("llm")}, "out_of_corpus": {"status": weather["status"], "llm_called": (weather.get("llm") or {}).get("llm_called")}}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    args = argparse.ArgumentParser(); args.add_argument("--strict", action="store_true"); parsed = args.parse_args()
    try: main(parsed.strict)
    except Exception as exc:
        print(f"API sequence failed: {type(exc).__name__}: {exc}", file=sys.stderr); raise
