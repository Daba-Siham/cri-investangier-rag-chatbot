"""Central model selection for indexing and retrieval."""

from src.embeddings.base import EmbeddingProvider
from src.embeddings.bge_m3 import BGEM3Provider
from src.embeddings.multilingual_e5 import MultilingualE5Provider


def create_embedding_provider(model_name: str, batch_size: int = 32,
                              device: str | None = None) -> EmbeddingProvider:
    normalized = model_name.lower().replace("_", "-")
    if normalized in {"bge-m3", "baai/bge-m3"}:
        return BGEM3Provider(batch_size=batch_size, device=device)
    if normalized in {"multilingual-e5-base", "intfloat/multilingual-e5-base", "e5"}:
        return MultilingualE5Provider(batch_size=batch_size, device=device)
    raise ValueError(f"Unsupported embedding model: {model_name}")
