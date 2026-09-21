"""Task 6 chat API; documentary answers always go through RAGService."""

import logging
import time
import uuid
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from src.api.dependencies import (build_conversation_store, build_query_rewriter,
                                  build_intent_classifier, build_rag_service)
from src.api.schemas import ChatRequest, ChatResponse
from src.conversation.query_rewriter import needs_rewrite
from src.generation.llm_client import LLMClient
from src.conversation.router import response_for_control, response_for_social, route_message
from src.utils.config import (CORS_ORIGINS, E5_COLLECTION, ENABLE_SESSION_INSPECTION,
                              LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, MAX_USER_MESSAGE_CHARACTERS, QDRANT_API_KEY,
                              QDRANT_URL)
from src.utils.logger import configure_logging
from src.vectorstore.qdrant_store import QdrantStore

LOGGER = logging.getLogger(__name__)
configure_logging()


def create_app(rag_service: Any | None = None, conversation_store: Any | None = None,
               query_rewriter: Any | None = None,
               enable_session_inspection: bool = ENABLE_SESSION_INSPECTION,
               intent_classifier: Any | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if app.state.rag_service is None:
            app.state.rag_service = build_rag_service(app.state.llm_client)
        yield

    app = FastAPI(title="CRI RAG Chat API", lifespan=lifespan)
    app.state.rag_service = rag_service
    app.state.llm_client = LLMClient()
    # Tests and embedded callers that supply a RAG service can opt out of the
    # network classifier; the production app builds both dependencies below.
    app.state.intent_classifier = intent_classifier
    if app.state.intent_classifier is None and rag_service is None:
        app.state.intent_classifier = build_intent_classifier(app.state.llm_client)
    app.state.conversation_store = conversation_store or build_conversation_store()
    app.state.query_rewriter = query_rewriter or build_query_rewriter()
    app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS,
                       allow_credentials=False, allow_methods=["GET", "POST", "DELETE"],
                       allow_headers=["Content-Type"])

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/ready")
    def ready():
        collection = False
        qdrant = False
        try:
            store = QdrantStore(QDRANT_URL, QDRANT_API_KEY)
            qdrant = store.collection_exists(E5_COLLECTION)
            collection = qdrant
        except Exception as exc:
            LOGGER.warning("Readiness Qdrant check failed: %s", str(exc)[:200])
        configured = bool(LLM_API_KEY and LLM_BASE_URL and LLM_MODEL)
        return {"status": "ready" if qdrant and collection and configured else "not_ready",
                "qdrant": qdrant, "collection": collection,
                "llm_configured": configured, "llm_model": LLM_MODEL}

    @app.post("/chat", response_model=ChatResponse, response_model_exclude_none=True)
    def chat(payload: ChatRequest, request: Request):
        message = payload.message.strip()
        if not message:
            raise HTTPException(status_code=422, detail="message must not be empty")
        if len(message) > MAX_USER_MESSAGE_CHARACTERS:
            raise HTTPException(status_code=422, detail="message exceeds the maximum length")
        session_id = payload.session_id or str(uuid.uuid4())
        store = request.app.state.conversation_store
        history = store.get(session_id)
        routed = route_message(message, request.app.state.intent_classifier)
        if routed["intent"] == "SOCIAL":
            answer = response_for_social(message, routed["action"], routed["language"])
            store.append(session_id, "user", message, kind="social")
            store.append(session_id, "assistant", answer, status="answered", citations=[], kind="social")
            return {"session_id": session_id, "status": "answered", "answer": answer,
                    "citations": [], "kind": "social"}
        if routed["intent"] == "CONVERSATION_CONTROL":
            control = response_for_control(history, routed["language"])
            answer, status = control["answer"], control["status"]
            store.append(session_id, "user", message, kind="control")
            store.append(session_id, "assistant", answer, status=status,
                         citations=control["citations"], kind="control")
            return {"session_id": session_id, "status": status, "answer": answer,
                    "citations": control["citations"], "kind": "control"}
        rewrite_used = needs_rewrite(message, history)
        retrieval_query = message
        rewrite_error = None
        if rewrite_used:
            try:
                retrieval_query = request.app.state.query_rewriter.rewrite(message, history)
            except Exception as exc:
                retrieval_query = message
                rewrite_error = "query rewrite failed"
                LOGGER.warning("Query rewrite failed for session %s: %s", session_id, str(exc)[:200])
        started = time.perf_counter()
        try:
            result = request.app.state.rag_service.answer(
                question=message, retrieval_query=retrieval_query)
        except Exception as exc:
            LOGGER.exception("RAG request failed for session %s", session_id)
            result = {"status": "generation_error", "answer": "", "citations": [],
                      "error": "RAG service unavailable"}
        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        store.append(session_id, "user", message, kind="document")
        result_kind = "document" if result.get("status") in {"answered", "insufficient_evidence"} else "error"
        store.append(session_id, "assistant", result.get("answer", ""),
                     status=result.get("status"), citations=result.get("citations", []), kind=result_kind)
        response = {"session_id": session_id, "status": result.get("status", "generation_error"),
                    "answer": result.get("answer", ""), "citations": result.get("citations", []),
                    "kind": "document" if result.get("status") == "answered" else "error"}
        if payload.include_diagnostics:
            response["retrieval"] = result.get("retrieval")
            response["llm"] = result.get("llm")
            response["diagnostics"] = {"original_query": message, "retrieval_query": retrieval_query,
                                        "query_rewrite_used": rewrite_used,
                                        "query_rewrite_error": rewrite_error,
                                        "duration_ms": duration_ms}
        LOGGER.info("chat session=%s status=%s retrieval=%s llm_called=%s model=%s duration_ms=%s",
                    session_id, response["status"], (result.get("retrieval") or {}).get("status"),
                    (result.get("llm") or {}).get("llm_called"), LLM_MODEL, duration_ms)
        if response["status"] in {"generation_error", "model_unavailable"}:
            response.pop("error", None)
        return response

    @app.delete("/sessions/{session_id}")
    def delete_session(session_id: str, request: Request):
        if not request.app.state.conversation_store.delete(session_id):
            raise HTTPException(status_code=404, detail="session not found")
        return {"status": "deleted", "session_id": session_id}

    if enable_session_inspection:
        @app.get("/sessions/{session_id}")
        def inspect_session(session_id: str, request: Request):
            history = request.app.state.conversation_store.get(session_id)
            if not history:
                raise HTTPException(status_code=404, detail="session not found")
            return {"session_id": session_id, "messages": history}

    return app


app = create_app()
