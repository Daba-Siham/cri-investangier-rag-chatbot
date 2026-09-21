"""Retrieval-gated RAG orchestration; no external knowledge or fallback answer."""
import logging
import re
from typing import Any

from src.generation.answer_generator import AnswerGenerator
from src.generation.llm_client import LLMGenerationError, LLMModelUnavailableError
from src.utils.language import is_tifinagh

LOGGER = logging.getLogger(__name__)

REFUSALS = {"fr": "Cette information n’est pas disponible dans les documents fournis.",
            "en": "This information is not available in the provided documents.",
            "es": "Esta información no está disponible en los documentos proporcionados.",
            "ar": "هذه المعلومة غير متوفرة في الوثائق المقدمة.",
            # TODO: Have a Tamazight linguist review this initial localization.
            "tzm": "ⵓⵔ ⵜⵍⵍⵉ ⵜⵎⵙⵙⵉⵔⵜ ⴳ ⵉⵙⵏⴰⴼⵏ."}


def _generation_error_type(exc: Exception) -> str:
    text = str(exc).lower()
    if "unknown citation" in text:
        return "invalid_citations"
    if "malformed" in text or "json" in text or "empty generation" in text:
        return "malformed_generations"
    return getattr(exc, "code", "other_generation_error")


def _safe_generation_error(exc: Exception) -> str:
    text = str(exc).replace("\n", " ")
    text = re.sub(r"(?i)(authorization\s*[:=]\s*bearer\s+)[^\s,}]+", r"\1<redacted>", text)
    text = re.sub(r"(?i)(api[_ -]?key|access[_ -]?token|secret)\s*[:=]\s*[^\s,}]+", r"\1=<redacted>", text)
    return text[:500]


def _log_generation_failure(model: object, exc: Exception, error_type: str) -> None:
    LOGGER.error("LLM generation failed model=%s status=%s error_type=%s error=%s",
                 model, "local", error_type, _safe_generation_error(exc))


def _chunk_key(item: dict[str, Any]) -> tuple:
    return (item.get("chunk_id"), item.get("document_id"), item.get("page"), item.get("text", ""))


def _top_chunks(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{key: item.get(key) for key in ("filename", "document_id", "page", "chunk_id")}
            for item in items[:5]]


def _annotate_amazigh_retrieval(retrieval: dict[str, Any], queries: list[str]) -> dict[str, Any]:
    items = retrieval.get("candidate_results") or retrieval.get("diagnostics") or []
    items = sorted(items, key=lambda item: item.get("retrieval_score", item.get("score", 0.0)) or 0.0,
                   reverse=True)
    retrieval["query_scores"] = [{"query": query, "top1_score": retrieval.get("top1_score"),
                                  "status": retrieval.get("status"),
                                  "selected_count": retrieval.get("selected_count", 0)}
                                 for query in queries]
    retrieval["top_scores"] = [item.get("retrieval_score", item.get("score")) for item in items[:5]]
    retrieval["top_chunks"] = _top_chunks(items)
    return retrieval


def _merge_amazigh_retrievals(runs: list[dict[str, Any]], queries: list[str]) -> dict[str, Any]:
    best_by_chunk: dict[tuple, dict[str, Any]] = {}
    query_scores = []
    threshold = None
    for query, run in zip(queries, runs):
        threshold = run.get("query_threshold", threshold)
        query_scores.append({"query": query, "top1_score": run.get("top1_score"),
                             "status": run.get("status"),
                             "selected_count": run.get("selected_count", 0)})
        for item in run.get("results") or []:
            key = _chunk_key(item)
            score = item.get("final_score", item.get("retrieval_score", item.get("score", 0.0))) or 0.0
            previous = best_by_chunk.get(key)
            if previous is None or score > (previous.get("final_score", previous.get("retrieval_score", 0.0)) or 0.0):
                best_by_chunk[key] = dict(item)
    merged = sorted(best_by_chunk.values(),
                    key=lambda item: item.get("final_score", item.get("retrieval_score", item.get("score", 0.0))) or 0.0,
                    reverse=True)[:5]
    status = "ok" if merged else "insufficient_evidence"
    result = {
        "query": queries[0] if queries else "",
        "status": status,
        "top1_score": max((run.get("top1_score") or 0.0 for run in runs), default=None),
        "query_threshold": threshold,
        "selected_count": len(merged),
        "results": merged,
        "candidate_results": merged,
        "query_scores": query_scores,
        "top_scores": [item.get("final_score", item.get("retrieval_score", item.get("score"))) for item in merged],
        "top_chunks": _top_chunks(merged),
    }
    return result


def detect_language(question: str) -> str:
    if is_tifinagh(question):
        return "tzm"
    if any("\u0600" <= char <= "\u06ff" for char in question):
        return "ar"
    if any(char in question for char in "¿¡"):
        return "es"
    lower = f" {question.casefold()} "
    if any(word in lower for word in (" combien ", " quelle ", " quel ", " projets ", " est-ce ")):
        return "fr"
    return "en"


class RAGService:
    def __init__(self, retrieval_pipeline, answer_generator: AnswerGenerator,
                 retrieval_translator=None):
        self.retrieval_pipeline = retrieval_pipeline
        self.answer_generator = answer_generator
        self.retrieval_translator = retrieval_translator

    def answer(self, question: str, retrieval_query: str | None = None) -> dict:
        """Answer ``question`` using evidence retrieved for ``retrieval_query``.

        The distinction keeps follow-up rewriting out of answer intent and
        language handling while preserving the retrieval-only role of history.
        """
        retrieval_query = retrieval_query if retrieval_query is not None else question
        language = detect_language(question)
        query_translation_used = False
        direct_translation = None
        retrieval_queries = [retrieval_query]
        if language == "tzm" and self.retrieval_translator is not None:
            try:
                reformulation = self.retrieval_translator.translate(retrieval_query)
                if isinstance(reformulation, str):
                    # Backward-compatible adapter for simple test/local translators.
                    direct_translation = reformulation.strip()
                    retrieval_queries = [direct_translation] if direct_translation else []
                else:
                    direct_translation = str(reformulation.get("translation", "")).strip()
                    retrieval_queries = [str(item).strip() for item in reformulation.get("retrieval_queries", []) if str(item).strip()][:3]
                if retrieval_queries:
                    retrieval_query = retrieval_queries[0]
                    query_translation_used = True
            except Exception as exc:
                LOGGER.warning("Amazigh retrieval translation failed; using original query: %s",
                               _safe_generation_error(exc))
                retrieval_queries = [question]
        if language == "tzm":
            LOGGER.info("Amazigh retrieval reformulation original=%s direct_translation=%s retrieval_queries=%s",
                        question, direct_translation, retrieval_queries)
        if language == "tzm" and query_translation_used and len(retrieval_queries) > 1:
            retrieval_runs = [self.retrieval_pipeline.retrieve(query, diagnostics=True)
                              for query in retrieval_queries[:3]]
            retrieval = _merge_amazigh_retrievals(retrieval_runs, retrieval_queries)
        elif language == "tzm":
            retrieval = self.retrieval_pipeline.retrieve(retrieval_query, diagnostics=True)
            retrieval = _annotate_amazigh_retrieval(retrieval, retrieval_queries)
        else:
            retrieval = self.retrieval_pipeline.retrieve(retrieval_query)
        if language == "tzm":
            LOGGER.info(
                "Amazigh retrieval scores per_query=%s final_top_scores=%s threshold=%s selected_count=%s top_documents=%s",
                retrieval.get("query_scores", []), retrieval.get("top_scores", []),
                retrieval.get("query_threshold"), retrieval.get("selected_count"),
                retrieval.get("top_chunks", []))
        retrieval_summary = {key: retrieval.get(key) for key in ("top1_score", "query_threshold", "selected_count")}
        retrieval_summary["status"] = retrieval.get("status")
        retrieval_summary["query_language"] = language
        retrieval_summary["query_translation_used"] = query_translation_used
        retrieval_summary["query"] = retrieval_query
        if language == "tzm":
            retrieval_summary["direct_translation"] = direct_translation
            retrieval_summary["retrieval_queries"] = retrieval_queries
            retrieval_summary["query_scores"] = retrieval.get("query_scores", [])
            retrieval_summary["top_scores"] = retrieval.get("top_scores", [])
            retrieval_summary["top_chunks"] = retrieval.get("top_chunks", [])
        if retrieval.get("status") != "ok" or not retrieval.get("results"):
            return {"status": "insufficient_evidence", "answer": REFUSALS[language], "citations": [],
                    "retrieval": retrieval_summary, "insufficient_evidence_reason": "retrieval_gate",
                    "llm": {"llm_called": False, "insufficient_evidence_reason": "retrieval_gate"}}
        generation_metadata = {
            "generation_attempts": 0,
            "structured_retry_used": False,
            "structured_retry_succeeded": False,
        }
        try:
            generated = self.answer_generator.generate(question, retrieval["results"])
            generation_metadata = getattr(self.answer_generator, "last_generation_metadata", generation_metadata)
        except LLMModelUnavailableError as exc:
            _log_generation_failure(getattr(self.answer_generator.provider, "model", None), exc,
                                    "model_unavailable")
            generation_metadata = getattr(self.answer_generator, "last_generation_metadata", generation_metadata)
            return {"status": "model_unavailable", "answer": "", "citations": [],
                    "retrieval": retrieval_summary, "llm": {"llm_called": True, **generation_metadata},
                    "error": str(exc), "error_type": "model_unavailable"}
        except LLMGenerationError as exc:
            _log_generation_failure(getattr(self.answer_generator.provider, "model", None), exc, exc.code)
            generation_metadata = getattr(self.answer_generator, "last_generation_metadata", generation_metadata)
            return {"status": "generation_error", "answer": "", "citations": [],
                    "retrieval": retrieval_summary, "llm": {"llm_called": True, **generation_metadata},
                    "error": str(exc), "error_type": exc.code}
        except Exception as exc:
            _log_generation_failure(getattr(self.answer_generator.provider, "model", None), exc,
                                    _generation_error_type(exc))
            generation_metadata = getattr(self.answer_generator, "last_generation_metadata", generation_metadata)
            return {"status": "generation_error", "answer": "", "citations": [],
                    "retrieval": retrieval_summary, "llm": {"llm_called": True, **generation_metadata},
                    "error": str(exc), "error_type": _generation_error_type(exc)}
        if generated.get("status") == "answered" and not str(generated.get("answer", "")).strip():
            return {"status": "generation_error", "answer": "", "citations": [],
                    "retrieval": retrieval_summary, "llm": {"llm_called": True, **generation_metadata},
                    "error": "Grounded answer was unexpectedly empty"}
        if generated["status"] == "insufficient_evidence":
            return {"status": "insufficient_evidence", "answer": REFUSALS[language], "citations": [],
                    "retrieval": retrieval_summary, "insufficient_evidence_reason": "model_context_rejection",
                    "llm": {"llm_called": True, **generation_metadata,
                            "insufficient_evidence_reason": "model_context_rejection"}}
        provider = self.answer_generator.provider
        return {"status": "answered", "answer": generated["answer"], "citations": generated["citations"],
                "retrieval": retrieval_summary,
                "llm": {"model": getattr(provider, "model", None),
                        "llm_called": True, **generation_metadata}}
