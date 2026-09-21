"""Optional multilingual cross-encoder reranking."""

from typing import Any


class Reranker:
    def rerank(self, query: str, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
        raise NotImplementedError


class MultilingualCrossEncoderReranker(Reranker):
    """Lazy CPU-compatible CrossEncoder adapter; failures are explicit."""

    def __init__(self, model_name: str = "BAAI/bge-reranker-v2-m3", batch_size: int = 8,
                 device: str = "cpu", model: Any | None = None):
        self.model_name, self.batch_size, self.device, self._model = model_name, batch_size, device, model

    @property
    def model(self):
        if self._model is None:
            try:
                from sentence_transformers import CrossEncoder
                self._model = CrossEncoder(self.model_name, device=self.device)
            except Exception as exc:
                raise RuntimeError(f"Unable to load configured reranker {self.model_name!r} on {self.device}: {exc}") from exc
        return self._model

    def rerank(self, query: str, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not candidates:
            return []
        scores = self.model.predict([(query, c.get("text", "")) for c in candidates],
                                    batch_size=self.batch_size, show_progress_bar=False)
        output = []
        for candidate, score in zip(candidates, scores):
            item = dict(candidate)
            item["rerank_score"] = float(score)
            output.append(item)
        return output
