from pathlib import Path
import os
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env", override=False)
RAW_JSON_DIR = PROJECT_ROOT / "data" / "raw" / "json"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# The splitter is character-based.  These values are sensible approximations
# of 700/100 tokens for normal prose, including Arabic and Latin scripts.
CHUNK_SIZE = 2800
CHUNK_OVERLAP = 400

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or None
BGE_M3_COLLECTION = os.getenv("BGE_M3_COLLECTION", "cri_chunks_bge_m3")
E5_COLLECTION = os.getenv("E5_COLLECTION", "cri_chunks_multilingual_e5_base")
EMBEDDING_BATCH_SIZE = int(os.getenv("EMBEDDING_BATCH_SIZE", "32"))
QDRANT_UPSERT_BATCH_SIZE = int(os.getenv("QDRANT_UPSERT_BATCH_SIZE", "128"))
DEFAULT_TOP_K = int(os.getenv("DEFAULT_TOP_K", "8"))

# Task 4 retrieval settings. BGE-M3 remains available through its existing
# collection/provider configuration; E5 is the primary production path.
RETRIEVAL_CANDIDATE_K = int(os.getenv("RETRIEVAL_CANDIDATE_K", "10"))
RETRIEVAL_FINAL_K = int(os.getenv("RETRIEVAL_FINAL_K", "5"))
E5_RELEVANCE_THRESHOLD = float(os.getenv("E5_RELEVANCE_THRESHOLD", "0.823114"))
ENABLE_RERANKER = os.getenv("ENABLE_RERANKER", "false").lower() in {"1", "true", "yes", "on"}
RERANKER_MODEL = os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-v2-m3")
RERANKER_BATCH_SIZE = int(os.getenv("RERANKER_BATCH_SIZE", "8"))
TEMPORAL_BONUS = float(os.getenv("TEMPORAL_BONUS", "0.03"))
TEMPORAL_PENALTY = float(os.getenv("TEMPORAL_PENALTY", "0.03"))
EXACT_MATCH_BONUS = float(os.getenv("EXACT_MATCH_BONUS", "0.01"))
MAX_CHUNKS_PER_DOCUMENT = int(os.getenv("MAX_CHUNKS_PER_DOCUMENT", "2"))
MAX_CONTEXT_CHARACTERS = int(os.getenv("MAX_CONTEXT_CHARACTERS", "12000"))
LLM_API_KEY = os.getenv("LLM_API_KEY") or None
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "")
LLM_MODEL = os.getenv("LLM_MODEL", "")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.0"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1024"))
LLM_REASONING_EFFORT = os.getenv("LLM_REASONING_EFFORT", "none").strip() or None
LLM_MAX_RETRIES = int(os.getenv("LLM_MAX_RETRIES", "1"))
LLM_TIMEOUT_SECONDS = float(os.getenv("LLM_TIMEOUT_SECONDS", "30"))
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "10"))
MAX_USER_MESSAGE_CHARACTERS = int(os.getenv("MAX_USER_MESSAGE_CHARACTERS", "5000"))
CORS_ORIGINS = [origin.strip() for origin in os.getenv(
    "CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",") if origin.strip()]
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))
ENABLE_SESSION_INSPECTION = os.getenv("ENABLE_SESSION_INSPECTION", "false").lower() in {"1", "true", "yes", "on"}
