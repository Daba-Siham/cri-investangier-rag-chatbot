"""Small provider interface shared by all embedding models."""

from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """Dense embedding provider independent of any vector database."""

    model_name: str
    dimension: int

    @abstractmethod
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed document passages in input order."""

    @abstractmethod
    def embed_query(self, query: str) -> list[float]:
        """Embed one user query."""

    @property
    def model_revision(self) -> str | None:
        return None
