"""Development-only staged diagnostic for the configured OpenAI-compatible LLM."""

import json
import sys
import urllib.error
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.generation.llm_client import LLMClient, _error_text, structured_response_format
from src.generation.prompts import SYSTEM_PROMPT
from src.utils.config import API_HOST, API_PORT, LLM_MODEL


def run_stage(name: str, client: LLMClient, messages: list[dict[str, str]], response_format):
    try:
        content = client.generate(messages, _response_format=response_format)
        print(f"{name}: success status={client.last_status_code or 'unknown'}")
        print(f"{name}: content={content[:2000]}")
    except Exception as exc:
        print(f"{name}: failure status={client.last_status_code or 'unknown'} "
              f"error_type={getattr(exc, 'code', type(exc).__name__)} "
              f"error={str(exc)[:1000].replace(chr(10), ' ')}")


def main() -> int:
    client = LLMClient()
    plain = [{"role": "user", "content": "أجب بكلمة مرحبا"}]
    run_stage("A plain", client, plain, None)

    json_messages = [{"role": "system", "content": "Return only valid JSON with answer, source_ids, and sufficient_context."},
                     {"role": "user", "content": "أجب بكلمة مرحبا"}]
    run_stage("B json_object", client, json_messages, {"type": "json_object"})

    schema = structured_response_format(LLM_MODEL)
    print("C json_schema: response_format=" + json.dumps(schema, ensure_ascii=False, separators=(",", ":")))
    schema_messages = [{"role": "system", "content": SYSTEM_PROMPT},
                       {"role": "user", "content": "Question:\nأجب بكلمة مرحبا"}]
    run_stage("C json_schema", client, schema_messages, schema)

    request = urllib.request.Request(
        f"http://{API_HOST}:{API_PORT}/chat",
        data=json.dumps({"message": "ما هو عدد الملفات التي صادقت عليها اللجنة خلال 2023",
                         "include_diagnostics": True}, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            print(f"D full_rag: http_status={response.status} status={result.get('status')} "
                  f"answer={str(result.get('answer', ''))[:500]}")
            if result.get("status") != "answered":
                retrieval = result.get("retrieval", {})
                llm = result.get("llm", {})
                print(f"D full_rag: retrieval_status={retrieval.get('status', 'unknown')} "
                      f"llm_called={llm.get('llm_called', 'unknown')} "
                      f"llm_attempts={llm.get('generation_attempts', 'unknown')}")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(f"D full_rag: failure http_status={exc.code} error={detail[:1000]}")
    except Exception as exc:
        print(f"D full_rag: failure http_status=unknown error_type={type(exc).__name__} "
              f"error={_error_text(exc)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
