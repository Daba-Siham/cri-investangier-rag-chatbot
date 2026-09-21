"""Retrieval-only Amazigh reformulation for the initial integration."""

import json
import re
from typing import Any
from src.generation.llm_client import LLMClient


TRANSLATION_SYSTEM_PROMPT = """You translate Amazigh/Tamazight questions written in Tifinagh for semantic retrieval
in documents from the Centre Régional d'Investissement (CRI).

First determine the actual meaning of the Tifinagh question. Then return JSON with:
1. translation: the direct French meaning;
2. retrieval_queries: up to three short French semantic retrieval formulations using
   terminology likely to appear in CRI documents.

The question may concern investment projects, CRI services, CRUI, business creation,
financing, land/foncier, industrial land, administrative procedures, permits, incentives,
investor support, territorial opportunities, or company support.
Preserve names, numbers, years, place names, organizations, investment terminology, and
administrative terminology. When wording is ambiguous, prefer CRI-appropriate terminology
without inventing concepts absent from the question. Do not answer the question or explain.
Return only valid JSON."""

# Small, maintainable guidance for common CRI concepts; this is intentionally not a
# complete Amazigh dictionary and should be reviewed by the company later.
CRI_GLOSSARY_GUIDANCE = """Useful French retrieval terminology when supported by the question:
- land access / foncier / terrain industriel
- accompagnement de l'investisseur / services du CRI
- projet d'investissement / financement
- création d'entreprise / procédures administratives / autorisations

Example intent guidance:
If the question asks how the CRI helps with finding land, retrieval formulations should
mention accompagnement du CRI and recherche de foncier, not only company-creation steps."""

REFORMULATION_SCHEMA = {
    "type": "object",
    "properties": {
        "translation": {"type": "string"},
        "retrieval_queries": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["translation", "retrieval_queries"],
    "additionalProperties": False,
}

_STOPWORDS = {"avec", "dans", "des", "du", "les", "pour", "que", "qui", "sur", "une", "est", "le", "la"}


def _valid_text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _sanity_check(translation: str, queries: list[str]) -> None:
    direct_tokens = {token for token in re.findall(r"[\wÀ-ÿ-]+", translation.casefold()) if token not in _STOPWORDS}
    query_tokens = set().union(*(set(re.findall(r"[\wÀ-ÿ-]+", query.casefold())) for query in queries))
    if not direct_tokens or not queries or not (direct_tokens & query_tokens):
        raise ValueError("Amazigh reformulation failed semantic sanity check")


class AmazighRetrievalTranslator:
    """Use the shared generic LLM client for deterministic retrieval translation."""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def translate(self, question: str) -> dict[str, Any]:
        content = self.llm_client.generate(
            [{"role": "system", "content": TRANSLATION_SYSTEM_PROMPT + "\n\n" + CRI_GLOSSARY_GUIDANCE},
             {"role": "user", "content": question}],
            temperature=0.0,
            _response_format={"type": "json_schema", "json_schema": {
                "name": "amazigh_retrieval_reformulation",
                "strict": True,
                "schema": REFORMULATION_SCHEMA,
            }},
        )
        try:
            value = json.loads(content)
        except (TypeError, json.JSONDecodeError) as exc:
            raise ValueError("Amazigh retrieval reformulation was not valid JSON") from exc
        translation = _valid_text(value.get("translation")) if isinstance(value, dict) else ""
        raw_queries = value.get("retrieval_queries") if isinstance(value, dict) else None
        queries = [_valid_text(item) for item in raw_queries] if isinstance(raw_queries, list) else []
        queries = [query for query in queries if query][:3]
        if not translation or not queries:
            raise ValueError("Amazigh retrieval reformulation was incomplete")
        _sanity_check(translation, queries)
        return {"translation": translation, "retrieval_queries": queries}
