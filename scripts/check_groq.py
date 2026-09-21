"""Validate the configured Groq model and its structured-output support."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.generation.llm_client import structured_response_format
from src.utils.config import LLM_API_KEY, LLM_MODEL


def _client():
    if not LLM_API_KEY:
        return None
    from groq import Groq
    return Groq(api_key=LLM_API_KEY)


def _model_ids(client):
    return {item.id for item in client.models.list().data}


def _sanitized(exc):
    return str(exc).replace("\n", " ")[:300]


def main() -> int:
    print(f"Configured model: {LLM_MODEL}")
    if not LLM_API_KEY:
        print("Model available: UNKNOWN (LLM_API_KEY is not configured)")
        return 1
    try:
        client = _client()
        available = LLM_MODEL in _model_ids(client)
        print(f"Model available: {'YES' if available else 'NO'}")
        if not available:
            return 1
        try:
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": "user", "content": "Respond only with OK"}],
                temperature=0,
                max_tokens=64,
            )
            print("Basic completion: OK" if response.choices[0].message.content else "Basic completion: ERROR (empty response)")
        except Exception as exc:
            print(f"Basic completion: ERROR ({_sanitized(exc)})")
            return 1
        request = {
            "model": LLM_MODEL,
            "messages": [
                {"role": "system", "content": "Return ONLY a JSON object, with no markdown or extra text. It must have exactly these keys: answer (string), source_ids (array of strings), sufficient_context (boolean)."},
                {"role": "user", "content": "Answer 2+2 using this exact shape: {\"answer\":\"4\",\"source_ids\":[],\"sufficient_context\":true}"},
            ],
            "temperature": 0,
            "max_tokens": 256,
            "response_format": structured_response_format(LLM_MODEL),
        }
        try:
            response = client.chat.completions.create(**request)
            json.loads(response.choices[0].message.content or "")
            print("Structured JSON schema: OK")
        except Exception as exc:
            if not ("response_format" in _sanitized(exc).lower() or "json_schema" in _sanitized(exc).lower()):
                print(f"Structured JSON schema: ERROR ({_sanitized(exc)})")
                return 1
            request.pop("response_format")
            try:
                response = client.chat.completions.create(**request)
                json.loads(response.choices[0].message.content or "")
                print("Structured JSON schema: fallback OK")
            except Exception as fallback_exc:
                print(f"Structured JSON schema: fallback ERROR ({_sanitized(fallback_exc)})")
                return 1
        return 0
    except Exception as exc:
        print(f"Groq check: ERROR ({_sanitized(exc)})")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
