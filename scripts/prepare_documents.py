"""Run the Task 2 document preparation pipeline."""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.chunking.chunker import chunk_documents
from src.ingestion.cleaner import normalize_text
from src.ingestion.json_loader import discover_json_files, load_documents
from src.utils.config import PROCESSED_DIR, RAW_JSON_DIR


def main() -> None:
    warning_messages: list[str] = []
    error_messages: list[str] = []
    source_files = discover_json_files(RAW_JSON_DIR)
    print(f"Found {len(source_files)} JSON documents.")
    documents = load_documents(RAW_JSON_DIR, warning_messages, error_messages)
    for document in documents:
        for page in document["pages"]:
            page["text"] = normalize_text(page.get("text"))
    chunks = chunk_documents(documents)
    pages = sum(len(document["pages"]) for document in documents)
    empty_pages = sum(not normalize_text(page.get("text")) for document in documents for page in document["pages"])
    report = {
        "documents_processed": len(documents),
        "pages_processed": pages,
        "chunks_created": len(chunks),
        "empty_pages": empty_pages,
        "warnings": warning_messages,
        "errors": error_messages,
    }
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    with (PROCESSED_DIR / "chunks.json").open("w", encoding="utf-8") as target:
        json.dump({"total_documents": len(documents), "total_pages": pages,
                   "total_chunks": len(chunks), "chunks": chunks}, target,
                  ensure_ascii=False, indent=2)
    with (PROCESSED_DIR / "processing_report.json").open("w", encoding="utf-8") as target:
        json.dump(report, target, ensure_ascii=False, indent=2)
    print(f"\nDocuments processed: {len(documents)}\nPages processed: {pages}")
    print(f"Chunks created: {len(chunks)}\nEmpty pages: {empty_pages}")
    print("\nOutput:\ndata/processed/chunks.json\ndata/processed/processing_report.json")
    if warning_messages:
        print(f"Warnings: {len(warning_messages)}")
    if error_messages:
        print(f"Errors: {len(error_messages)}")


if __name__ == "__main__":
    main()
