"""Repeat real indexed RAG generations and report categorized stability."""
import argparse, json, os, re, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("HF_HUB_OFFLINE", "1")

from src.embeddings.factory import create_embedding_provider
from src.generation.answer_generator import AnswerGenerator
from src.generation.llm_client import LLMClient
from src.rag.rag_service import RAGService
from src.retrieval.retrieval_pipeline import RetrievalPipeline
from src.retrieval.semantic_retriever import SemanticRetriever
from src.utils.config import E5_COLLECTION, E5_RELEVANCE_THRESHOLD, EMBEDDING_BATCH_SIZE, QDRANT_API_KEY, QDRANT_URL
from src.vectorstore.qdrant_store import QdrantStore

QUESTIONS = [
    ("Arabic", "\u0643\u0645 \u0639\u062f\u062f \u0627\u0644\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u062a\u064a \u0648\u0627\u0641\u0642\u062a \u0639\u0644\u064a\u0647\u0627 \u0627\u0644\u0644\u062c\u0646\u0629 \u0627\u0644\u062c\u0647\u0648\u064a\u0629 \u0627\u0644\u0645\u0648\u062d\u062f\u0629 \u0644\u0644\u0627\u0633\u062a\u062b\u0645\u0627\u0631 \u062e\u0644\u0627\u0644 \u0633\u0646\u0629 2023", ("709",)),
    ("French", "Combien de projets ont été approuvés par la CRUI au premier semestre 2024 ?", ("379",)),
    ("Spanish", "¿Cuántas nuevas empresas fueron creadas en la región en 2025?", ("15286",)),
    ("English", "How many new companies were created in the region in 2025?", ("15286",)),
]

def normalize_numeric_text(text: str) -> str:
    text = text.replace("\u00a0", " ").replace("\u202f", " ")
    return re.sub(r"(?<=\d)[,. ](?=\d)", "", text)

def marker_matches(answer: str, markers: tuple[str, ...]) -> bool:
    normalized = normalize_numeric_text(answer)
    return any(normalize_numeric_text(marker) in normalized for marker in markers)

def safe_error(result: dict) -> str | None:
    error = result.get("error")
    return str(error).replace("\n", " ")[:160] if error else None

def classify(result: dict, markers: tuple[str, ...]) -> str:
    status = result.get("status")
    if status == "answered":
        return "answered" if marker_matches(result.get("answer", ""), markers) else "answer_marker_mismatches"
    if status == "insufficient_evidence":
        return "model_context_rejections" if result.get("insufficient_evidence_reason") == "model_context_rejection" else "retrieval_insufficient"
    error_type = result.get("error_type")
    if error_type == "structured_output_error": return "structured_output_errors"
    if error_type in {"connection_error", "timeout", "server_error"}: return "transport_errors"
    if error_type == "invalid_citations": return "invalid_citations"
    if error_type == "malformed_generations": return "malformed_generations"
    return "other_errors"

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--runs", type=int, default=5); args = parser.parse_args()
    if args.runs < 1: parser.error("--runs must be positive")
    embedding = create_embedding_provider("multilingual-e5-base", EMBEDDING_BATCH_SIZE)
    pipeline = RetrievalPipeline(SemanticRetriever(embedding, QdrantStore(QDRANT_URL, QDRANT_API_KEY), E5_COLLECTION), E5_RELEVANCE_THRESHOLD, enable_reranker=False)
    service = RAGService(pipeline, AnswerGenerator(LLMClient()))
    report = []
    for language, question, markers in QUESTIONS:
        categories = {key: 0 for key in ("answered", "structured_output_errors", "transport_errors", "model_context_rejections", "invalid_citations", "malformed_generations", "retrieval_insufficient", "answer_marker_mismatches", "other_errors")}; retries, transport_retries, durations = 0, 0, []
        for run in range(args.runs):
            started = time.perf_counter()
            try:
                result = service.answer(question); duration = time.perf_counter() - started; llm = result.get("llm") or {}
                retries += int(bool(llm.get("structured_retry_used"))); transport_retries += int(llm.get("transport_retries", 0)); categories[classify(result, markers)] += 1; durations.append(duration)
                print(f"{language} {run + 1}/{args.runs}: status={result.get('status')} error_type={result.get('error_type')} error={safe_error(result)!r} retry={'structured' if llm.get('structured_retry_used') else 'none'} duration={duration:.1f}s llm_called={llm.get('llm_called')}", flush=True)
            except Exception as exc:
                duration = time.perf_counter() - started; categories["other_errors"] += 1; durations.append(duration)
                print(f"{language} {run + 1}/{args.runs}: status=exception error_type={type(exc).__name__} error={str(exc)[:160]!r} retry=none duration={duration:.1f}s", flush=True)
        report.append({"language": language, "attempts": args.runs, **categories, "success_rate": round(categories["answered"] / args.runs, 3), "structured_retries": retries, "transport_retries": transport_retries, "average_duration_seconds": round(sum(durations) / len(durations), 3)})
    print(json.dumps(report, ensure_ascii=False, indent=2)); return 0

if __name__ == "__main__": raise SystemExit(main())
