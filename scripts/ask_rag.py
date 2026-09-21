"""Ask the retrieval-gated RAG service."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.embeddings.factory import create_embedding_provider
from src.generation.answer_generator import AnswerGenerator
from src.generation.llm_client import LLMClient
from src.rag.rag_service import RAGService
from src.retrieval.retrieval_pipeline import RetrievalPipeline
from src.retrieval.semantic_retriever import SemanticRetriever
from src.utils.config import (E5_COLLECTION, E5_RELEVANCE_THRESHOLD,
                              EMBEDDING_BATCH_SIZE, QDRANT_API_KEY, QDRANT_URL)
from src.vectorstore.qdrant_store import QdrantStore


def main():
    # Keep multilingual JSON answers printable on Windows consoles using a
    # legacy code page (without changing the data passed to retrieval/LLM).
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--diagnostics", action="store_true")
    args = parser.parse_args()
    provider = create_embedding_provider("multilingual-e5-base", EMBEDDING_BATCH_SIZE)
    retriever = SemanticRetriever(provider, QdrantStore(QDRANT_URL, QDRANT_API_KEY), E5_COLLECTION)
    pipeline = RetrievalPipeline(retriever, E5_RELEVANCE_THRESHOLD, enable_reranker=False)
    service = RAGService(pipeline, AnswerGenerator(LLMClient()))
    response = service.answer(args.question)
    if args.as_json:
        print(json.dumps(response, ensure_ascii=False, indent=2)); return
    print(f"Status: {response['status']}\n\nAnswer:\n{response.get('answer', '')}")
    if response.get("citations"):
        print("\nSources:")
        for citation in response["citations"]:
            print(f"- {citation.get('filename')} — page {citation.get('page')}")
    if args.diagnostics:
        print("\nDiagnostics:")
        print(json.dumps({"retrieval": response.get("retrieval"), "llm": response.get("llm")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
