"""Generic client for an OpenAI-compatible chat-completions endpoint."""

import json
import logging
import re
import time
from typing import Any

import httpx
from openai import OpenAI
from src.generation.base import LLMProvider
from src.utils.config import (LLM_API_KEY, LLM_BASE_URL, LLM_MAX_RETRIES,
                              LLM_MAX_TOKENS, LLM_MODEL, LLM_TEMPERATURE,
                              LLM_TIMEOUT_SECONDS, LLM_REASONING_EFFORT)

LOGGER = logging.getLogger(__name__)

GROUNDING_SCHEMA = {
    "type": "object",
    "properties": {
        "answer": {"type": "string"},
        "source_ids": {"type": "array", "items": {"type": "string"}},
        "sufficient_context": {"type": "boolean"},
    },
    "required": ["answer", "source_ids", "sufficient_context"],
    "additionalProperties": False,
}


class LLMGenerationError(RuntimeError):
    def __init__(self, message: str, code: str = "other_generation_error",
                 provider_code: str | None = None):
        super().__init__(message)
        self.code = code
        self.provider_code = provider_code


class LLMModelUnavailableError(LLMGenerationError):
    pass


class LLMAuthenticationError(LLMGenerationError):
    def __init__(self, message: str, provider_code: str | None = None):
        super().__init__(message, "authentication_error", provider_code)


class LLMTimeoutError(LLMGenerationError):
    def __init__(self, message: str, provider_code: str | None = None):
        super().__init__(message, "timeout", provider_code)


class LLMStructuredOutputError(LLMGenerationError):
    def __init__(self, message: str, provider_code: str | None = None):
        super().__init__(message, "structured_output_error", provider_code)


def structured_response_format(_model: str) -> dict[str, Any]:
    """Prefer standard JSON Schema; callers fall back to JSON mode if rejected."""
    return {"type": "json_schema", "json_schema": {
        "name": "grounded_rag_answer", "strict": True, "schema": GROUNDING_SCHEMA}}


def _error_text(exc: Exception) -> str:
    text = str(exc).replace("\n", " ")
    text = re.sub(r"(?i)(authorization\s*[:=]\s*bearer\s+)[^\s,}]+", r"\1<redacted>", text)
    text = re.sub(r"(?i)(api[_ -]?key|access[_ -]?token|secret)\s*[:=]\s*[^\s,}]+", r"\1=<redacted>", text)
    return text[:500]


def _status_code(exc: Exception | str) -> str:
    status = getattr(exc, "status_code", None)
    if status is not None:
        return str(status)
    text = exc if isinstance(exc, str) else _error_text(exc)
    match = re.search(
        r"\bHTTP\s+(\d{3})\b|\bstatus(?:_code)?\s*[=:]\s*(\d{3})\b|\bcode\s*[:=]\s*(\d{3})\b",
        text, re.I)
    return next((group for group in match.groups() if group), "unknown") if match else "unknown"


def _log_generation_failure(model: str, exc: Exception, error_type: str | None = None) -> None:
    safe_text = _error_text(exc)
    LOGGER.error("LLM generation failed model=%s status=%s error_type=%s error=%s",
                 model, _status_code(exc), error_type or _error_code(safe_text), safe_text)


def _error_code(text: str) -> str:
    lowered = text.lower()
    if "json_validate_failed" in lowered or "structured" in lowered or "response_format" in lowered:
        return "structured_output_error"
    if "rate limit" in lowered or "429" in lowered:
        return "rate_limit"
    if "timeout" in lowered or "timed out" in lowered:
        return "timeout"
    if "connection" in lowered or "network" in lowered:
        return "connection_error"
    if re.search(r"\b5\d\d\b", lowered):
        return "server_error"
    if any(value in lowered for value in ("authentication", "unauthorized", "invalid api key", "401")):
        return "authentication_error"
    return "other_generation_error"


def _is_retryable(text: str) -> bool:
    lowered = text.lower()
    return ("connection" in lowered or "network" in lowered or "timeout" in lowered or
            "timed out" in lowered or bool(re.search(r"\b5\d\d\b", lowered)))


def _is_format_unsupported(text: str) -> bool:
    lowered = text.lower()
    return ("response_format" in lowered or "json_schema" in lowered or
            "json_object" in lowered or "structured output" in lowered) and any(
                value in lowered for value in ("400", "bad request", "unsupported"))


def _is_reasoning_unsupported(text: str) -> bool:
    lowered = text.lower()
    mentions_parameter = "reasoning_effort" in lowered or "reasoning effort" in lowered
    return mentions_parameter and any(value in lowered for value in (
        "unsupported", "unknown parameter", "unrecognized", "invalid parameter", "not allowed"))


def _is_token_exhaustion(text: str) -> bool:
    lowered = text.lower()
    return any(value in lowered for value in (
        "max completion tokens reached", "maximum completion tokens", "max tokens reached",
        "completion token limit", "token limit"))


class LLMClient(LLMProvider):
    def __init__(self, api_key: str | None = LLM_API_KEY, base_url: str = LLM_BASE_URL,
                 model: str = LLM_MODEL, temperature: float = LLM_TEMPERATURE,
                 max_tokens: int = LLM_MAX_TOKENS, timeout: float = LLM_TIMEOUT_SECONDS,
                 client: Any | None = None, max_retries: int = LLM_MAX_RETRIES,
                 reasoning_effort: str | None = LLM_REASONING_EFFORT):
        self.api_key = api_key
        self.base_url = base_url
        self.model, self.temperature, self.max_tokens = model, temperature, max_tokens
        self.timeout = timeout
        self.reasoning_effort = reasoning_effort
        self.max_retries = max(0, max_retries)
        self._client = client
        self.last_attempt_count = 0
        self.last_transport_retry_count = 0
        self.last_status_code = None

    @property
    def client(self):
        if self._client is None:
            if not self.api_key:
                raise LLMAuthenticationError("LLM_API_KEY is not configured; set it before generation.")
            if not self.base_url:
                raise LLMGenerationError("LLM_BASE_URL is not configured; set it before generation.", "configuration_error")
            if not self.model:
                raise LLMGenerationError("LLM_MODEL is not configured; set it before generation.", "configuration_error")
            self._client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout,
                # The managed environment exposes a dead localhost proxy
                # (127.0.0.1:9).  Groq is directly reachable, so do not let
                # unrelated proxy variables break the configured API client.
                http_client=httpx.Client(trust_env=False, timeout=self.timeout),
            )
        return self._client

    def generate(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        max_attempts = max(1, min(2, int(kwargs.pop("_max_attempts", 2))))
        response_format = kwargs.pop("_response_format", structured_response_format(self.model))
        request = {"model": self.model, "messages": messages,
                   "temperature": kwargs.pop("temperature", self.temperature),
                   "max_tokens": kwargs.pop("max_tokens", self.max_tokens), **kwargs}
        reasoning_effort = request.pop("reasoning_effort", self.reasoning_effort)
        if reasoning_effort:
            request["reasoning_effort"] = reasoning_effort
        if response_format is not None:
            request["response_format"] = response_format
            LOGGER.debug("LLM response_format=%s", response_format)
        last_error = None
        format_fallback_used = False
        reasoning_fallback_used = False
        self.last_attempt_count = self.last_transport_retry_count = 0
        for attempt in range(max_attempts):
            self.last_attempt_count = attempt + 1
            try:
                response = self.client.chat.completions.create(**request)
                self.last_status_code = getattr(response, "status_code", 200)
                content = response.choices[0].message.content or ""
                if not content:
                    error = LLMGenerationError("LLM returned an empty generation", "empty_generation")
                    raise error
                return content
            except LLMGenerationError as exc:
                # Covers configuration/initialization errors raised before an
                # HTTP request exists; request failures are logged below with
                # their sanitized provider payload.
                _log_generation_failure(self.model, exc, getattr(exc, "code", None))
                raise
            except Exception as exc:
                last_error = exc
                self.last_status_code = getattr(exc, "status_code", None)
                text = _error_text(exc)
                lowered = text.lower()
                if "model_not_found" in lowered or "model not found" in lowered or "does not exist" in lowered:
                    error = LLMModelUnavailableError(
                        f"Configured LLM_MODEL {self.model!r} is unavailable; set it to an active model.",
                        "model_unavailable")
                    _log_generation_failure(self.model, exc, error.code)
                    raise error from exc
                if "json_validate_failed" in lowered:
                    if (_is_token_exhaustion(text) and not format_fallback_used and
                            request.get("response_format", {}).get("type") == "json_schema"):
                        # Schema-constrained output can exhaust the budget before
                        # producing a document. JSON mode is a bounded generic fallback.
                        request["response_format"] = {"type": "json_object"}
                        format_fallback_used = True
                        continue
                    error = LLMStructuredOutputError(
                        f"LLM generation failed: {text}", "json_validate_failed")
                    _log_generation_failure(self.model, exc, error.code)
                    raise error from exc
                if reasoning_effort and not reasoning_fallback_used and _is_reasoning_unsupported(text):
                    request.pop("reasoning_effort", None)
                    reasoning_fallback_used = True
                    continue
                if not format_fallback_used and _is_format_unsupported(text):
                    request["response_format"] = {"type": "json_object"}
                    format_fallback_used = True
                    continue
                if attempt + 1 < max_attempts and _is_retryable(text):
                    self.last_transport_retry_count += 1
                    time.sleep(0.25 * (attempt + 1))
                    continue
                code = _error_code(text)
                if code == "authentication_error":
                    error = LLMAuthenticationError(f"LLM generation failed: {text}")
                    _log_generation_failure(self.model, exc, error.code)
                    raise error from exc
                if code == "timeout":
                    error = LLMTimeoutError(f"LLM generation failed: {text}")
                    _log_generation_failure(self.model, exc, error.code)
                    raise error from exc
        final_text = _error_text(last_error)
        final_code = _error_code(final_text)
        error = LLMGenerationError(f"LLM generation failed: {final_text}", final_code)
        _log_generation_failure(self.model, last_error, error.code)
        raise error from last_error
