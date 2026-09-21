"""Qdrant access with a native-client preference and HTTP read fallback."""

import json
import logging
import uuid
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

LOGGER = logging.getLogger(__name__)


def point_id_for_chunk(chunk_id: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"cri-document-rag:{chunk_id}"))


def _qdrant_types():
    from qdrant_client import QdrantClient, models
    return QdrantClient, models


class _QdrantHTTPError(RuntimeError):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status


class QdrantStore:
    def __init__(self, url: str = "http://localhost:6333", api_key: str | None = None,
                 client: Any | None = None):
        self.url = url.rstrip("/")
        self.api_key = api_key
        self.client = client
        self._rest = client is None
        if client is not None:
            return
        try:
            QdrantClient, _ = _qdrant_types()
            self.client = QdrantClient(url=url, api_key=api_key)
            self._rest = False
        except ModuleNotFoundError as exc:
            if exc.name == "qdrant_client":
                LOGGER.warning("qdrant-client package is unavailable; using Qdrant REST fallback.")
            else:
                LOGGER.warning("qdrant-client native dependency could not load; using REST fallback.")
            LOGGER.debug("Native Qdrant import failure", exc_info=exc)
        except ImportError as exc:
            LOGGER.warning("qdrant-client native gRPC dependency could not load; using REST fallback.")
            LOGGER.debug("Native Qdrant import failure", exc_info=exc)

    def _rest_request(self, method: str, path: str, body: dict[str, Any] | None = None) -> Any:
        headers = {"Accept": "application/json"}
        data = None
        if body is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        if self.api_key:
            headers["api-key"] = self.api_key
        request = urllib.request.Request(self.url + path, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:300]
            raise _QdrantHTTPError(exc.code, f"Qdrant HTTP {exc.code} for {method} {path}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise RuntimeError(f"Qdrant HTTP request failed for {method} {path}: {exc}") from exc
        except (ValueError, UnicodeError) as exc:
            raise RuntimeError(f"Qdrant returned invalid JSON for {method} {path}") from exc

    def _write_requires_native(self) -> None:
        if self._rest:
            raise RuntimeError("Qdrant REST fallback is read-only; native qdrant-client is required for writes.")

    def ensure_collection(self, collection_name: str, dimension: int, recreate: bool = False) -> None:
        self._write_requires_native()
        _, models = _qdrant_types()
        exists = self.client.collection_exists(collection_name)
        if exists:
            if recreate:
                self.client.delete_collection(collection_name)
            else:
                info = self.client.get_collection(collection_name)
                vectors = info.config.params.vectors
                size = vectors.get("").size if isinstance(vectors, dict) and "" in vectors else getattr(vectors, "size", None)
                distance = vectors.get("").distance if isinstance(vectors, dict) and "" in vectors else getattr(vectors, "distance", None)
                if size != dimension or (distance is not None and str(distance).lower() not in {"cosine", "distance.cosine"}):
                    raise ValueError(f"Collection {collection_name} is incompatible; use --recreate")
                return
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(collection_name=collection_name,
                vectors_config=models.VectorParams(size=dimension, distance=models.Distance.COSINE))

    def collection_exists(self, collection_name: str) -> bool:
        if not self._rest:
            return bool(self.client.collection_exists(collection_name))
        path = f"/collections/{urllib.parse.quote(collection_name, safe='')}"
        try:
            self._rest_request("GET", path)
            return True
        except _QdrantHTTPError as exc:
            if exc.status == 404:
                return False
            raise

    def get_collection(self, collection_name: str) -> Any:
        if not self._rest:
            return self.client.get_collection(collection_name)
        response = self._rest_request("GET", f"/collections/{urllib.parse.quote(collection_name, safe='')}")
        return response.get("result", response)

    def create_payload_indexes(self, collection_name: str) -> None:
        self._write_requires_native()
        _, models = _qdrant_types()
        for field in ("document_id", "filename", "language"):
            try:
                self.client.create_payload_index(collection_name, field, field_schema=models.PayloadSchemaType.KEYWORD)
            except Exception:
                pass
        try:
            self.client.create_payload_index(collection_name, "page", field_schema=models.PayloadSchemaType.INTEGER)
        except Exception:
            pass

    @staticmethod
    def payload_for_chunk(chunk: dict[str, Any]) -> dict[str, Any]:
        metadata = chunk["metadata"]
        return {"chunk_id": chunk["chunk_id"], "document_id": metadata["document_id"],
                "filename": metadata["filename"], "page": metadata["page"],
                "language": metadata.get("language"), "chunk_index": metadata["chunk_index"],
                "text": chunk["text"], "source_type": "internal_cri_document"}

    def upsert(self, collection_name: str, chunks: list[dict[str, Any]], vectors: list[list[float]], batch_size: int = 128) -> None:
        self._write_requires_native()
        _, models = _qdrant_types()
        if len(chunks) != len(vectors):
            raise ValueError("Each chunk must have exactly one vector")
        for start in range(0, len(chunks), batch_size):
            points = [models.PointStruct(id=point_id_for_chunk(chunk["chunk_id"]), vector=vector, payload=self.payload_for_chunk(chunk))
                      for chunk, vector in zip(chunks[start:start + batch_size], vectors[start:start + batch_size])]
            self.client.upsert(collection_name=collection_name, points=points, wait=True)

    def count(self, collection_name: str) -> int:
        if not self._rest:
            return int(self.client.count(collection_name=collection_name, exact=True).count)
        path = f"/collections/{urllib.parse.quote(collection_name, safe='')}/points/count"
        response = self._rest_request("POST", path, {"exact": True})
        return int(response.get("result", {}).get("count", 0))

    def search(self, collection_name: str, vector: list[float], limit: int,
               score_threshold: float | None = None, query_filter: Any | None = None) -> list[Any]:
        if not self._rest:
            if hasattr(self.client, "query_points"):
                response = self.client.query_points(collection_name=collection_name, query=vector, limit=limit,
                    score_threshold=score_threshold, query_filter=query_filter, with_payload=True)
                return list(response.points)
            return list(self.client.search(collection_name=collection_name, query_vector=vector, limit=limit,
                score_threshold=score_threshold, query_filter=query_filter, with_payload=True))
        body = {"query": vector, "limit": limit, "with_payload": True}
        if score_threshold is not None:
            body["score_threshold"] = score_threshold
        if query_filter is not None:
            body["filter"] = query_filter
        base = f"/collections/{urllib.parse.quote(collection_name, safe='')}/points"
        try:
            response = self._rest_request("POST", base + "/query", body)
        except _QdrantHTTPError as exc:
            if exc.status != 404:
                raise RuntimeError(str(exc)) from exc
            legacy = {"vector": vector, "limit": limit, "with_payload": True}
            if score_threshold is not None:
                legacy["score_threshold"] = score_threshold
            if query_filter is not None:
                legacy["filter"] = query_filter
            response = self._rest_request("POST", base + "/search", legacy)
        result = response.get("result", response)
        points = result.get("points", []) if isinstance(result, dict) else result
        return list(points or [])
