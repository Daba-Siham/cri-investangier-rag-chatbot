"""Unicode-safe command-line semantic search."""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.embeddings.factory import create_embedding_provider
from src.retrieval.semantic_retriever import SemanticRetriever
from src.utils.config import (BGE_M3_COLLECTION, DEFAULT_TOP_K, E5_COLLECTION,
                               EMBEDDING_BATCH_SIZE, QDRANT_API_KEY, QDRANT_URL)
from src.vectorstore.qdrant_store import QdrantStore


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=("bge-m3", "multilingual-e5-base"))
    parser.add_argument("--query", required=True)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--score-threshold", type=float, default=None)
    args = parser.parse_args()
    provider = create_embedding_provider(args.model, EMBEDDING_BATCH_SIZE)
    collection = BGE_M3_COLLECTION if args.model == "bge-m3" else E5_COLLECTION
    retriever = SemanticRetriever(provider, QdrantStore(QDRANT_URL, QDRANT_API_KEY), collection)
    for result in retriever.search(args.query, args.top_k, args.score_threshold):
        preview = " ".join(result["text"].split())[:300]
        print(f"rank={result['rank']} score={result['score']:.4f} filename={result['filename']} "
              f"page={result['page']} language={result['language']} chunk_id={result['chunk_id']}\n  {preview}\n")


if __name__ == "__main__":
    main()
