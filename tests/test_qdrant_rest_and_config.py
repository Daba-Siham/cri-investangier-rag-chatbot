import json
import urllib.error

import pytest

from src.vectorstore import qdrant_store
from src.vectorstore.qdrant_store import QdrantStore
from src.utils import config


class FakeNativeClient:
    def search(self, **kwargs):
        return [{"score": 0.9, "payload": {"text": "ok"}}]

    def count(self, **kwargs):
        return type("Count", (), {"count": 3})()


def test_injected_native_client_is_preserved():
    store = QdrantStore(client=FakeNativeClient())
    assert store._rest is False
    assert store.count("c") == 3
    assert store.search("c", [1.0], 2)[0]["score"] == 0.9


def test_rest_search_request_and_result(monkeypatch):
    captured = {}

    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def read(self):
            return json.dumps({"result": {"points": [{"score": .88, "payload": {"text": "مرحبا", "language": "ar"}}]}}).encode()

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["body"] = json.loads(request.data.decode())
        captured["timeout"] = timeout
        return Response()

    monkeypatch.setattr(qdrant_store.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(qdrant_store, "_qdrant_types", lambda: (_ for _ in ()).throw(ImportError("cygrpc")))
    store = QdrantStore("http://qdrant:6333")
    results = store.search("cri", [0.1, 0.2], 10, score_threshold=.823114)
    assert captured["url"].endswith("/collections/cri/points/query")
    assert captured["body"]["limit"] == 10
    assert captured["body"]["score_threshold"] == .823114
    assert results[0]["score"] == .88
    assert results[0]["payload"]["text"] == "مرحبا"


def test_rest_fallback_does_not_report_install_message(monkeypatch, caplog):
    monkeypatch.setattr(qdrant_store, "_qdrant_types", lambda: (_ for _ in ()).throw(ImportError("cygrpc")))
    store = QdrantStore("http://localhost:6333")
    assert store._rest
    assert "Install qdrant-client" not in caplog.text
    assert "REST fallback" in caplog.text


def test_rest_http_error_is_clear(monkeypatch):
    def failed(*args, **kwargs):
        raise urllib.error.URLError("connection refused")
    monkeypatch.setattr(qdrant_store.urllib.request, "urlopen", failed)
    store = object.__new__(QdrantStore)
    store.url, store.api_key, store._rest = "http://bad", None, True
    with pytest.raises(RuntimeError, match="Qdrant HTTP request failed"):
        store.search("c", [1.0], 1)


def test_dotenv_values_are_loaded_without_replacing_os_environment(monkeypatch):
    monkeypatch.delenv("QDRANT_URL", raising=False)
    monkeypatch.setenv("QDRANT_URL", "http://os-environment:6333")
    import importlib
    loaded = importlib.reload(config)
    assert loaded.QDRANT_URL == "http://os-environment:6333"
    assert loaded.LLM_MODEL
    assert loaded.RETRIEVAL_CANDIDATE_K == 10
