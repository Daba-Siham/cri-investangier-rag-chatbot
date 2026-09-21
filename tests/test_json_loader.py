import json
from pathlib import Path

from src.ingestion.json_loader import load_documents


def test_loader_preserves_unicode_and_warns_for_empty_page():
    path = Path(".task2-loader-test.json")
    path.write_text(json.dumps({"document_id": "doc", "filename": "x.pdf",
                                "language": "ar", "pages": [
                                    {"page": 1, "text": "مرحبا بالعالم"},
                                    {"page": 2, "text": ""},
                                ]}, ensure_ascii=False), encoding="utf-8")
    try:
        messages = []
        documents = load_documents(Path("."), messages, [])
        loaded = next(document for document in documents if document["document_id"] == "doc")
        assert loaded["pages"][0]["text"] == "مرحبا بالعالم"
        assert len(messages) == 1
    finally:
        path.unlink(missing_ok=True)
