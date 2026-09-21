"""Sanitized staged preflight for the configured OpenAI-compatible LLM endpoint."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.generation.llm_client import LLMClient
from src.utils.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, LLM_TIMEOUT_SECONDS


def host(value: str) -> str:
    parsed = urlparse(value or "")
    return parsed.hostname or "<missing>"


def category(exc: Exception) -> str:
    text = str(exc).casefold()
    if any(value in text for value in ("auth", "api key", "401", "unauthorized")):
        return "authentication"
    if "timeout" in text or "timed out" in text:
        return "timeout"
    if "ssl" in text or "certificate" in text:
        return "SSL"
    if "model" in text and ("not" in text or "unavailable" in text):
        return "model unavailable"
    if any(value in text for value in ("connection", "connect", "network", "dns")):
        return "connection"
    if "response_format" in text or "json_schema" in text or "400" in text:
        return "malformed request"
    return "other"


def sanitized_chain(exc: Exception) -> str:
    parts = []
    current: BaseException | None = exc
    while current is not None and len(parts) < 3:
        text = re.sub(r"(?i)(authorization\s*[:=]\s*bearer\s+)[^\s,}]+", r"\1<redacted>", str(current).replace("\n", " "))
        text = re.sub(r"(?i)(api[_ -]?key|access[_ -]?token|secret)\s*[:=]\s*[^\s,}]+", r"\1=<redacted>", text)
        parts.append(f"{type(current).__name__}: {text[:240]}")
        current = current.__cause__ or current.__context__
    return " <- ".join(parts)


def main() -> int:
    print(f"Endpoint host: {host(LLM_BASE_URL)}")
    print(f"Model: {LLM_MODEL or '<missing>'}")
    print(f"API key configured: {'PASS' if bool(LLM_API_KEY) else 'FAIL'}")
    print(f"Base URL: {'PASS' if LLM_BASE_URL.endswith('/v1') else 'FAIL'}")
    if not LLM_API_KEY or not LLM_BASE_URL or not LLM_MODEL:
        print("Configuration: FAIL (missing required setting)")
        return 1
    print("Configuration: PASS")
    try:
        client = LLMClient(temperature=0.0, max_tokens=64, timeout=LLM_TIMEOUT_SECONDS, max_retries=0)
        print("Client: PASS")
    except Exception as exc:
        print(f"Client: FAIL [{category(exc)}] {sanitized_chain(exc)}")
        return 1
    try:
        client.generate(
            [{"role": "system", "content": "Return JSON with keys ok and kind."},
             {"role": "user", "content": 'Return {"ok":true,"kind":"trivial"}.'}],
            _max_attempts=1,
        )
        print("Trivial request: PASS")
    except Exception as exc:
        print(f"Trivial request: FAIL [{category(exc)}] {sanitized_chain(exc)}")
        return 1
    try:
        client.generate(
            [{"role": "system", "content": "Answer only from supplied evidence and return JSON."},
             {"role": "user", "content": "Question: What color is the sky? Evidence: The supplied evidence says the sky is blue. Return a JSON answer."}],
            _max_attempts=1,
        )
        print("RAG request: PASS")
    except Exception as exc:
        print(f"RAG request: FAIL [{category(exc)}] {sanitized_chain(exc)}")
        return 1
    print("Connection: PASS")
    print("Authentication: PASS")
    print("Model: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
