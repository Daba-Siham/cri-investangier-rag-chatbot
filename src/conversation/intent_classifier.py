"""Small provider-neutral intent classification for ambiguous chat turns."""

import json
from typing import Any

from src.generation.llm_client import LLMClient
INTENT_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "conversation_intent",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "intent": {"type": "string", "enum": ["social", "rag", "conversation_control"]},
                "language": {"type": "string", "enum": ["fr", "ar", "en", "es", "tzm"]},
            },
            "required": ["intent", "language"],
            "additionalProperties": False,
        },
    },
}

SYSTEM_PROMPT = """You classify messages sent to a CRI document chatbot.
Return only strict JSON with intent and language.
intent must be one of: social, rag, conversation_control.
social means greetings, thanks, goodbye, politeness, casual small talk, or addressing the assistant without asking for factual CRI information.
rag means any question or request requiring facts, explanations, numbers, procedures, investment information, CRI information, or document-based information.
conversation_control means controlling the conversation, such as asking to repeat the previous answer, clarify it, or asking where it came from.
A greeting combined with an actual question is rag.
Examples: "bonjour ghiitaa" is social; "bonjour AI" is social; "hiii madame" is social; "merci beaucoup" is social; "au revoir" is social.
"bonjour, combien de projets ont été approuvés en 2024 ?" is rag; "salut, comment créer une entreprise ?" is rag; "et en 2023 ?" is rag; "quelle est la source ?" is conversation_control.
language must be fr, ar, en, es, or tzm (Amazigh/Tifinagh)."""

_VALID_INTENTS = {"social", "rag", "conversation_control"}
_VALID_LANGUAGES = {"fr", "ar", "en", "es", "tzm"}


class IntentClassifier:
    """Classify only; this class never generates an answer."""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def classify(self, message: str) -> dict[str, str]:
        content = self.llm_client.generate(
            [{"role": "system", "content": SYSTEM_PROMPT},
             {"role": "user", "content": message}],
            _response_format=INTENT_SCHEMA,
            max_tokens=80,
            temperature=0,
            reasoning_effort=None,
            _max_attempts=1,
        )
        try:
            result: Any = json.loads(content)
        except (TypeError, json.JSONDecodeError) as exc:
            raise ValueError("intent classifier returned invalid JSON") from exc
        if not isinstance(result, dict):
            raise ValueError("intent classifier returned a non-object")
        intent = str(result.get("intent", "")).casefold()
        language = str(result.get("language", "")).casefold()
        if intent not in _VALID_INTENTS or language not in _VALID_LANGUAGES:
            raise ValueError("intent classifier returned an invalid classification")
        return {"intent": intent, "language": language}
