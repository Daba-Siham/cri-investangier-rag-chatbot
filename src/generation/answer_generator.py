from src.generation.citation_validator import validate_and_map
from src.generation.prompts import SYSTEM_PROMPT, build_source_context
from src.generation.llm_client import LLMGenerationError
from src.generation.schemas import parse_generation


class AnswerGenerator:
    def __init__(self, provider):
        self.provider = provider
        self.last_generation_metadata = {
            "generation_attempts": 0,
            "structured_retry_used": False,
            "structured_retry_succeeded": False,
            "transport_retries": 0,
        }

    def generate(self, question: str, results: list[dict]) -> dict:
        if not results:
            raise ValueError("Generation requires non-empty documentary evidence")
        context, source_map = build_source_context(results)
        messages = [{"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Question:\n{question}\n\n{context}"}]
        self.last_generation_metadata = {
            "generation_attempts": 1,
            "structured_retry_used": False,
            "structured_retry_succeeded": False,
            "transport_retries": 0,
        }
        try:
            content = self.provider.generate(messages)
            first_attempts = getattr(self.provider, "last_attempt_count", 1)
            self.last_generation_metadata["generation_attempts"] = first_attempts
            self.last_generation_metadata["transport_retries"] = getattr(self.provider, "last_transport_retry_count", 0)
        except LLMGenerationError as exc:
            first_attempts = getattr(self.provider, "last_attempt_count", 1)
            self.last_generation_metadata["generation_attempts"] = first_attempts
            self.last_generation_metadata["transport_retries"] = getattr(self.provider, "last_transport_retry_count", 0)
            if (exc.code != "structured_output_error" or
                    exc.provider_code != "json_validate_failed"):
                raise
            self.last_generation_metadata.update({
                "generation_attempts": 2,
                "structured_retry_used": True,
            })
            first_transport_retries = getattr(self.provider, "last_transport_retry_count", 0)
            retry_messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": (
                    f"Question:\n{question}\n\n"
                    "Answer from the supplied evidence only. Use the same language as the user, including Amazigh/Tamazight in Tifinagh when the question is written in Tifinagh. "
                    "Use only allowed SOURCE_X IDs. Set sufficient_context to false if the evidence "
                    "is insufficient.\n\n" + context
                )},
            ]
            remaining_attempts = max(1, 3 - first_attempts)
            try:
                content = self.provider.generate(retry_messages, _max_attempts=remaining_attempts)
            except LLMGenerationError:
                self.last_generation_metadata["generation_attempts"] = first_attempts + getattr(self.provider, "last_attempt_count", 1)
                self.last_generation_metadata["transport_retries"] = first_transport_retries + getattr(self.provider, "last_transport_retry_count", 0)
                raise
            self.last_generation_metadata["generation_attempts"] = first_attempts + getattr(self.provider, "last_attempt_count", 1)
            self.last_generation_metadata["transport_retries"] = first_transport_retries + getattr(self.provider, "last_transport_retry_count", 0)
            self.last_generation_metadata["structured_retry_succeeded"] = True
        parsed = parse_generation(content)
        citations = validate_and_map(parsed["source_ids"], source_map)
        if not parsed["sufficient_context"]:
            return {"status": "insufficient_evidence", "answer": "", "citations": [], "sufficient_context": False}
        if not parsed["answer"].strip() or not citations:
            raise ValueError("Grounded answer must contain text and at least one valid source")
        return {"status": "answered", "answer": parsed["answer"], "citations": citations, "sufficient_context": True}
