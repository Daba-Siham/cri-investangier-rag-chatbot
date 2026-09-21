"""Sentence-transformers adapter for multilingual E5 retrieval prefixes."""

from typing import Any

from src.embeddings.base import EmbeddingProvider


class MultilingualE5Provider(EmbeddingProvider):
    model_name = "intfloat/multilingual-e5-base"
    dimension = 768

    def __init__(self, batch_size: int = 32, device: str | None = None,
                 model: Any | None = None):
        self.batch_size = batch_size
        self.device = device
        self._model = model

    @property
    def model(self) -> Any:
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            kwargs = {"device": self.device} if self.device else {}
            self._model = SentenceTransformer(self.model_name, **kwargs)
        return self._model

    @property
    def model_revision(self) -> str | None:
        return getattr(self.model, "revision", None) if self._model is not None else None

    def _encode(self, texts: list[str]) -> list[list[float]]:
        values = self.model.encode(texts, batch_size=self.batch_size,
                                   normalize_embeddings=True,
                                   convert_to_numpy=True, show_progress_bar=False)
        return values.tolist()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._encode([f"passage: {text}" for text in texts])

    def embed_query(self, query: str) -> list[float]:
        return self._encode([f"query: {query}"])[0]
