"""Small local A/B audit for GPT-OSS reasoning parameters on the Arabic RAG case."""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("HF_HUB_OFFLINE", "1")

from src.embeddings.factory import create_embedding_provider
from src.generation.llm_client import LLMClient, LLMGenerationError
from src.generation.prompts import SYSTEM_PROMPT, build_source_context
from src.retrieval.retrieval_pipeline import RetrievalPipeline
from src.retrieval.semantic_retriever import SemanticRetriever
from src.utils.config import E5_COLLECTION, E5_RELEVANCE_THRESHOLD, EMBEDDING_BATCH_SIZE, QDRANT_API_KEY, QDRANT_URL
from src.vectorstore.qdrant_store import QdrantStore

QUESTION = "كم عدد الطلبات التي وافقت عليها اللجنة الجهوية الموحدة للاستثمار خلال سنة 2023"


def run(label, provider, messages, **kwargs):
    try:
        content = provider.generate(messages, **kwargs)
        return {"case": label, "status": "success", "content": content}
    except LLMGenerationError as exc:
        return {"case": label, "status": exc.code, "provider_code": exc.provider_code}


def main():
    embedding = create_embedding_provider("multilingual-e5-base", EMBEDDING_BATCH_SIZE)
    retrieval = RetrievalPipeline(
        SemanticRetriever(embedding, QdrantStore(QDRANT_URL, QDRANT_API_KEY), E5_COLLECTION),
        E5_RELEVANCE_THRESHOLD, enable_reranker=False,
    ).retrieve(QUESTION)
    context, _ = build_source_context(retrieval["results"])
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Question:\n{QUESTION}\n\n{context}"}]
    provider = LLMClient()
    results = [run("current", provider, messages),
               run("hidden_low", provider, messages, reasoning_format="hidden", reasoning_effort="low")]
    print(json.dumps({"retrieval": {"status": retrieval.get("status"), "top1_score": retrieval.get("top1_score")}, "results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
