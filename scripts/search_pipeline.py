"""CLI for Task 4 retrieval-only evidence selection."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.embeddings.factory import create_embedding_provider
from src.retrieval.retrieval_pipeline import RetrievalPipeline
from src.retrieval.reranker import MultilingualCrossEncoderReranker
from src.retrieval.semantic_retriever import SemanticRetriever
from src.utils.config import (E5_COLLECTION, E5_RELEVANCE_THRESHOLD,
                              ENABLE_RERANKER,
                              EMBEDDING_BATCH_SIZE, QDRANT_API_KEY,
                              QDRANT_URL, RETRIEVAL_CANDIDATE_K,
                              RETRIEVAL_FINAL_K, RERANKER_BATCH_SIZE,
                              RERANKER_MODEL)
from src.vectorstore.qdrant_store import QdrantStore


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--candidate-k", type=int, default=RETRIEVAL_CANDIDATE_K)
    parser.add_argument("--final-k", type=int, default=RETRIEVAL_FINAL_K)
    parser.add_argument("--threshold", type=float, default=E5_RELEVANCE_THRESHOLD)
    parser.add_argument("--reranker", action="store_true", help="Explicitly enable the configured cross-encoder reranker")
    parser.add_argument("--diagnostics", action="store_true")
    args = parser.parse_args()
    provider = create_embedding_provider("multilingual-e5-base", EMBEDDING_BATCH_SIZE)
    retriever = SemanticRetriever(provider, QdrantStore(QDRANT_URL, QDRANT_API_KEY), E5_COLLECTION)
    enable_reranker = args.reranker or ENABLE_RERANKER
    reranker = MultilingualCrossEncoderReranker(RERANKER_MODEL, RERANKER_BATCH_SIZE) if enable_reranker else None
    pipeline = RetrievalPipeline(retriever, args.threshold, reranker, enable_reranker)
    output = pipeline.retrieve(args.query, args.candidate_k, args.final_k, args.diagnostics)
    print(f"status={output['status']} candidates={output['candidate_count']} accepted={output['accepted_count']} selected={output['selected_count']}")
    for result in output["results"]:
        print(f"rank={result.get('rank')} retrieval={result['retrieval_score']:.4f} "
              f"rerank={result['rerank_score']} final={result['final_score']:.4f} "
              f"filename={result.get('filename')} page={result.get('page')} language={result.get('language')} "
              f"chunk_id={result.get('chunk_id')}\n  {' '.join(result.get('text', '').split())[:300]}\n")
    if args.diagnostics:
        print(json.dumps(output.get("diagnostics", []), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
