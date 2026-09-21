import json

import pytest

from src.generation.answer_generator import AnswerGenerator
from src.generation.citation_validator import validate_and_map
from src.generation.llm_client import (GROUNDING_SCHEMA, LLMAuthenticationError,
                                       LLMClient, LLMGenerationError,
                                       LLMModelUnavailableError,
                                       structured_response_format)
from src.utils.config import LLM_TEMPERATURE
from src.generation.prompts import build_source_context


SOURCE = {"chunk_id": "c1", "text": "379 projets approuvés", "document_id": "doc",
          "filename": "source.pdf", "page": 2, "language": "fr"}


class FakeProvider:
    model = "fake-llm-model"

    def __init__(self, response):
        self.response, self.calls = response, []

    def generate(self, messages, **kwargs):
        self.calls.append(messages)
        return self.response


class RetryProvider:
    model = "fake-llm-model"

    def __init__(self, responses):
        self.responses, self.calls = list(responses), []

    def generate(self, messages, **kwargs):
        self.calls.append(messages)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def test_source_context_assigns_ids_and_preserves_unicode():
    context, mapping = build_source_context([{**SOURCE, "text": "العربية Réponse ¿Qué?"}])
    assert "SOURCE_1" in context and "العربية Réponse ¿Qué?" in context
    assert mapping["SOURCE_1"]["page"] == 2


def test_answer_maps_only_retrieval_metadata_and_deduplicates_sources():
    provider = FakeProvider(json.dumps({"answer": "379 projets ont été approuvés.",
                                        "source_ids": ["SOURCE_1", "SOURCE_1"], "sufficient_context": True}, ensure_ascii=False))
    result = AnswerGenerator(provider).generate("Combien de projets ?", [SOURCE])
    assert result["status"] == "answered" and len(result["citations"]) == 1
    assert result["citations"][0]["filename"] == "source.pdf"
    assert "page" in result["citations"][0]
    assert provider.calls[0][0]["role"] == "system"


def test_invalid_source_and_malformed_json_are_rejected():
    with pytest.raises(ValueError, match="Unknown citation"):
        AnswerGenerator(FakeProvider('{"answer":"x","source_ids":["SOURCE_99"],"sufficient_context":true}')).generate("q", [SOURCE])
    with pytest.raises(ValueError, match="malformed"):
        AnswerGenerator(FakeProvider("not-json")).generate("q", [SOURCE])


def test_insufficient_context_is_supported():
    provider = FakeProvider('{"answer":"","source_ids":[],"sufficient_context":false}')
    result = AnswerGenerator(provider).generate("q", [SOURCE])
    assert result["status"] == "insufficient_evidence" and result["citations"] == []


def test_missing_key_is_clear_and_no_secret_is_logged():
    provider = LLMClient(api_key=None, client=None)
    with pytest.raises(LLMAuthenticationError, match="LLM_API_KEY"):
        provider.generate([])


def test_validate_citations_deduplicates_by_document_page():
    second = {**SOURCE, "chunk_id": "c2", "language": "ar"}
    result = validate_and_map(["SOURCE_1", "SOURCE_2"], {"SOURCE_1": SOURCE, "SOURCE_2": second})
    assert len(result) == 1 and result[0]["chunk_id"] == "c1"


class FakeCompletion:
    def __init__(self, content):
        self.choices = [type("Choice", (), {"message": type("Message", (), {"content": content})()})()]


class FakeCompletions:
    def __init__(self, errors=None, content='{"answer":"4","source_ids":[],"sufficient_context":true}'):
        self.errors, self.content, self.requests = list(errors or []), content, []

    def create(self, **request):
        self.requests.append(request)
        if self.errors:
            error = self.errors.pop(0)
            raise error
        return FakeCompletion(self.content)


def test_json_schema_success_and_controlled_json_object_fallback():
    completions = FakeCompletions(content='{"answer":"4","source_ids":[],"sufficient_context":true}')
    client = type("Client", (), {"chat": type("Chat", (), {"completions": completions})()})()
    strict_provider = LLMClient(api_key="secret", model="test-model",
                                client=client, max_retries=0)
    assert strict_provider.generate([]).startswith("{")
    response_format = completions.requests[0]["response_format"]
    assert response_format["type"] == "json_schema"
    assert response_format["json_schema"]["schema"] == GROUNDING_SCHEMA

    unsupported = RuntimeError("400 response_format json_schema unsupported")
    completions = FakeCompletions(errors=[unsupported], content='{"answer":"4","source_ids":[],"sufficient_context":true}')
    client = type("Client", (), {"chat": type("Chat", (), {"completions": completions})()})()
    result = LLMClient(api_key="secret", model="future/model", client=client, max_retries=0).generate([])
    assert result.startswith("{") and len(completions.requests) == 2
    assert completions.requests[1]["response_format"] == {"type": "json_object"}


def test_token_exhaustion_uses_bounded_json_object_fallback():
    completions = FakeCompletions(
        errors=[RuntimeError("400 json_validate_failed max completion tokens reached before generating a valid document")],
        content='{"answer":"4","source_ids":[],"sufficient_context":true}',
    )
    client = type("Client", (), {"chat": type("Chat", (), {"completions": completions})()})()
    result = LLMClient(api_key="secret", model="test-model", client=client,
                       max_tokens=1024, max_retries=0).generate([])
    assert result.startswith("{")
    assert len(completions.requests) == 2
    assert completions.requests[0]["max_tokens"] == 1024
    assert completions.requests[1]["response_format"] == {"type": "json_object"}


def test_reasoning_effort_is_sent_and_removed_if_endpoint_rejects_it():
    completions = FakeCompletions(
        errors=[RuntimeError("400 invalid parameter reasoning_effort")],
        content='{"answer":"4","source_ids":[],"sufficient_context":true}',
    )
    client = type("Client", (), {"chat": type("Chat", (), {"completions": completions})()})()
    result = LLMClient(api_key="secret", model="test-model", client=client,
                       max_tokens=1024, reasoning_effort="none", max_retries=0).generate([])
    assert result.startswith("{")
    assert completions.requests[0]["reasoning_effort"] == "none"
    assert "reasoning_effort" not in completions.requests[1]


def test_plain_generation_can_omit_response_format():
    completions = FakeCompletions(content="مرحبا")
    client = type("Client", (), {"chat": type("Chat", (), {"completions": completions})()})()
    result = LLMClient(api_key="secret", model="test-model", client=client).generate(
        [{"role": "user", "content": "أجب بكلمة مرحبا"}], _response_format=None)
    assert result == "مرحبا"
    assert "response_format" not in completions.requests[0]


def test_grounding_schema_is_exact_and_arabic_json_parses():
    fmt = structured_response_format("test-model")
    assert fmt["type"] == "json_schema"
    assert fmt["json_schema"]["schema"] == GROUNDING_SCHEMA
    assert set(GROUNDING_SCHEMA["required"]) == set(GROUNDING_SCHEMA["properties"])
    assert GROUNDING_SCHEMA["additionalProperties"] is False
    arabic = json.dumps({"answer": "709", "source_ids": ["SOURCE_1"], "sufficient_context": True}, ensure_ascii=False)
    assert AnswerGenerator(FakeProvider(arabic)).generate("سؤال", [SOURCE])["answer"] == "709"


def test_json_validate_failure_is_classified_as_structured_output_error():
    completions = FakeCompletions(errors=[RuntimeError("400 json_validate_failed")])
    client = type("Client", (), {"chat": type("Chat", (), {"completions": completions})()})()
    with pytest.raises(LLMGenerationError) as error:
        LLMClient(api_key="secret", model="future/model", client=client, max_retries=0).generate([])
    assert error.value.code == "structured_output_error"


def test_json_validate_failed_uses_one_simplified_retry_and_validates_second_success():
    provider = RetryProvider([
        LLMGenerationError("bad", "structured_output_error", "json_validate_failed"),
        '{"answer":"709","source_ids":["SOURCE_1"],"sufficient_context":true}',
    ])
    generator = AnswerGenerator(provider)
    result = generator.generate("سؤال عربي", [SOURCE])
    assert result["status"] == "answered" and result["answer"] == "709"
    assert len(provider.calls) == 2
    assert "Question:" in provider.calls[0][1]["content"]
    assert "Answer from the supplied evidence only" in provider.calls[1][1]["content"]
    assert "Question:\nسؤال عربي" in provider.calls[1][1]["content"]
    assert generator.last_generation_metadata["generation_attempts"] == 2
    assert generator.last_generation_metadata["structured_retry_used"] is True
    assert generator.last_generation_metadata["structured_retry_succeeded"] is True


def test_malformed_llm_json_is_rejected_after_transport_response():
    completions = FakeCompletions(content="not-json")
    client = type("Client", (), {"chat": type("Chat", (), {"completions": completions})()})()
    with pytest.raises(ValueError, match="malformed"):
        AnswerGenerator(LLMClient(api_key="secret", model="test-model", client=client)).generate(
            "سؤال عربي", [SOURCE])


def test_generation_diagnostics_redact_credentials(caplog):
    completions = FakeCompletions(errors=[RuntimeError("401 unauthorized api_key=supersecret")])
    client = type("Client", (), {"chat": type("Chat", (), {"completions": completions})()})()
    with caplog.at_level("ERROR"):
        with pytest.raises(LLMAuthenticationError):
            LLMClient(api_key="supersecret", model="test-model", client=client, max_retries=0).generate([])
    assert "LLM generation failed" in caplog.text
    assert "model=test-model" in caplog.text
    assert "401" in caplog.text
    assert "supersecret" not in caplog.text


def test_structured_retry_is_at_most_once_and_second_failure_stays_structured_error():
    provider = RetryProvider([
        LLMGenerationError("bad", "structured_output_error", "json_validate_failed"),
        LLMGenerationError("bad again", "structured_output_error", "json_validate_failed"),
    ])
    with pytest.raises(LLMGenerationError) as error:
        AnswerGenerator(provider).generate("q", [SOURCE])
    assert error.value.code == "structured_output_error" and len(provider.calls) == 2


def test_invalid_citation_and_other_failures_do_not_retry():
    invalid = RetryProvider(['{"answer":"x","source_ids":["SOURCE_99"],"sufficient_context":true}'])
    with pytest.raises(ValueError, match="Unknown citation"):
        AnswerGenerator(invalid).generate("q", [SOURCE])
    assert len(invalid.calls) == 1
    provider = RetryProvider([LLMGenerationError("other", "other_generation_error")])
    with pytest.raises(LLMGenerationError):
        AnswerGenerator(provider).generate("q", [SOURCE])
    assert len(provider.calls) == 1


def test_model_not_found_is_classified():
    completions = FakeCompletions(errors=[RuntimeError("404 model_not_found")])
    client = type("Client", (), {"chat": type("Chat", (), {"completions": completions})()})()
    with pytest.raises(LLMModelUnavailableError, match="LLM_MODEL"):
        LLMClient(api_key="secret", client=client, max_retries=0).generate([])


def test_documentary_provider_uses_rag_temperature_not_chat_temperature():
    provider = LLMClient(api_key="secret", client=object(), max_retries=0)
    assert provider.temperature == LLM_TEMPERATURE == 0.0


def test_transport_error_retries_once_and_authentication_does_not_retry():
    transient = FakeCompletions(errors=[RuntimeError("503 service unavailable")], content='{"answer":"4","source_ids":[],"sufficient_context":true}')
    client = type("Client", (), {"chat": type("Chat", (), {"completions": transient})()})()
    assert LLMClient(api_key="secret", client=client, max_retries=0).generate([]).startswith("{")
    assert len(transient.requests) == 2
    auth = FakeCompletions(errors=[RuntimeError("401 unauthorized")])
    client = type("Client", (), {"chat": type("Chat", (), {"completions": auth})()})()
    with pytest.raises(LLMGenerationError) as error:
        LLMClient(api_key="secret", client=client).generate([])
    assert error.value.code == "authentication_error" and len(auth.requests) == 1


def test_structured_plus_transport_paths_have_three_attempt_hard_cap():
    completions = FakeCompletions(errors=[RuntimeError("400 json_validate_failed"), RuntimeError("503 unavailable"), RuntimeError("503 unavailable")])
    client = type("Client", (), {"chat": type("Chat", (), {"completions": completions})()})()
    provider = LLMClient(api_key="secret", client=client)
    with pytest.raises(LLMGenerationError):
        AnswerGenerator(provider).generate("q", [SOURCE])
    assert len(completions.requests) == 3
