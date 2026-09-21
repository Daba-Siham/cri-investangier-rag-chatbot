"""Deterministic first-pass evaluation of grounded answers."""
import argparse
import json
import re
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from src.embeddings.factory import create_embedding_provider
from src.generation.answer_generator import AnswerGenerator
from src.generation.llm_client import LLMClient
from src.rag.rag_service import RAGService, detect_language
from src.retrieval.retrieval_pipeline import RetrievalPipeline
from src.retrieval.semantic_retriever import SemanticRetriever
from src.utils.config import (E5_COLLECTION, E5_RELEVANCE_THRESHOLD,
                              EMBEDDING_BATCH_SIZE, QDRANT_API_KEY, QDRANT_URL)
from src.vectorstore.qdrant_store import QdrantStore


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", type=Path, default=ROOT / "evaluation" / "generation_questions.json")
    args = parser.parse_args()
    questions = json.loads(args.questions.read_text(encoding="utf-8"))
    provider = create_embedding_provider("multilingual-e5-base", EMBEDDING_BATCH_SIZE)
    retriever = SemanticRetriever(provider, QdrantStore(QDRANT_URL, QDRANT_API_KEY), E5_COLLECTION)
    service = RAGService(RetrievalPipeline(retriever, E5_RELEVANCE_THRESHOLD, enable_reranker=False), AnswerGenerator(LLMClient()))
    rows, latencies = [], []
    for question in questions:
        started = time.perf_counter(); response = service.answer(question["question"]); latencies.append((time.perf_counter() - started) * 1000)
        citation_keys = {(c.get("document_id"), c.get("page")) for c in response.get("citations", [])}
        expected_keys = {(s["document_id"], s["page"]) for s in question.get("expected_sources", [])}
        answer = response.get("answer", "")
        rows.append({"id": question["id"], "question": question["question"], "expected_fact": question.get("expected_fact", ""),
                     "generated_answer": answer, "expected_sources": question.get("expected_sources", []),
                     "returned_citations": response.get("citations", []),
                     "correct_language": detect_language(answer) == question.get("query_language") if answer else not question.get("answerable"),
                     "citation_valid": bool(response.get("citations")) if question.get("answerable") else not response.get("citations"),
                     "citation_expected_source": bool(citation_keys & expected_keys) if expected_keys else not citation_keys,
                     "fact_signal": bool(re.search(r"\d", answer)) if question.get("expected_fact") else not answer,
                     "status": response.get("status"), "llm_called": response.get("llm", {}).get("llm_called")})
    answerable = [r for r, q in zip(rows, questions) if q.get("answerable")]
    unanswerable = [r for r, q in zip(rows, questions) if not q.get("answerable")]
    summary = {"question_count": len(rows), "answerable_count": len(answerable),
               "answer_rate": sum(r["status"] == "answered" for r in answerable) / len(answerable),
               "refusal_accuracy": sum(r["status"] == "insufficient_evidence" for r in unanswerable) / len(unanswerable),
               "citation_validity_rate": sum(r["citation_valid"] for r in answerable) / len(answerable),
               "citation_expected_source_accuracy": sum(r["citation_expected_source"] for r in answerable) / len(answerable),
               "unsupported_citation_rate": sum(not r["citation_valid"] for r in answerable) / len(answerable),
               "language_accuracy": sum(r["correct_language"] for r in rows) / len(rows),
               "numeric_fact_signal_rate": sum(r["fact_signal"] for r in answerable) / len(answerable),
               "average_latency_ms": statistics.mean(latencies)}
    outdir = ROOT / "evaluation" / "results"; outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "generation_results.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    review = ["| ID | Question | Expected fact | Generated answer | Returned citation | Status |", "|---|---|---|---|---|---|"]
    for row in rows:
        cells = [row["id"], row["question"], row["expected_fact"], row["generated_answer"], str(row["returned_citations"]), row["status"]]
        review.append("| " + " | ".join(cell.replace("|", "\\|") for cell in cells) + " |")
    (outdir / "generation_review.md").write_text("\n".join(review) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__": main()
