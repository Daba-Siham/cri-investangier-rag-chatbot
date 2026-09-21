"""Construction and dependency access for the FastAPI application."""

from src.conversation.memory import ConversationStore
from src.conversation.intent_classifier import IntentClassifier
from src.conversation.query_rewriter import QueryRewriter
from src.generation.answer_generator import AnswerGenerator
from src.generation.llm_client import LLMClient
from src.rag.query_translation import AmazighRetrievalTranslator
from src.retrieval.retrieval_pipeline import RetrievalPipeline
from src.retrieval.semantic_retriever import SemanticRetriever
from src.embeddings.factory import create_embedding_provider
from src.utils.config import (E5_COLLECTION, E5_RELEVANCE_THRESHOLD, EMBEDDING_BATCH_SIZE,
                              MAX_HISTORY_MESSAGES, QDRANT_API_KEY, QDRANT_URL)
from src.vectorstore.qdrant_store import QdrantStore
from src.rag.rag_service import RAGService


def build_rag_service(llm_client: LLMClient | None = None) -> RAGService:
    llm_client = llm_client or LLMClient()
    provider = create_embedding_provider("multilingual-e5-base", EMBEDDING_BATCH_SIZE)
    store = QdrantStore(QDRANT_URL, QDRANT_API_KEY)
    retriever = SemanticRetriever(provider, store, E5_COLLECTION)
    pipeline = RetrievalPipeline(retriever, E5_RELEVANCE_THRESHOLD, enable_reranker=False)
    return RAGService(
        pipeline,
        AnswerGenerator(llm_client),
        retrieval_translator=AmazighRetrievalTranslator(llm_client),
    )


def build_intent_classifier(llm_client: LLMClient) -> IntentClassifier:
    return IntentClassifier(llm_client)


def build_conversation_store() -> ConversationStore:
    return ConversationStore(MAX_HISTORY_MESSAGES)


def build_query_rewriter() -> QueryRewriter:
    return QueryRewriter()
