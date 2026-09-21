"""Build one persistent Qdrant collection from the immutable chunks dataset."""

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.embeddings.factory import create_embedding_provider
from src.utils.config import (BGE_M3_COLLECTION, E5_COLLECTION, EMBEDDING_BATCH_SIZE,
                              PROCESSED_DIR, QDRANT_API_KEY, QDRANT_URL,
                              QDRANT_UPSERT_BATCH_SIZE, CHUNK_OVERLAP, CHUNK_SIZE)
from src.vectorstore.qdrant_store import QdrantStore


def load_chunks(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("chunks"), list):
        raise ValueError("chunks.json must contain a chunks list")
    for chunk in data["chunks"]:
        if not all(field in chunk for field in ("chunk_id", "text", "metadata")):
            raise ValueError("Every chunk needs chunk_id, text, and metadata")
    return data["chunks"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=("bge-m3", "multilingual-e5-base"))
    parser.add_argument("--recreate", action="store_true")
    parser.add_argument("--device", default=None)
    parser.add_argument("--batch-size", type=int, default=EMBEDDING_BATCH_SIZE)
    parser.add_argument("--upsert-batch-size", type=int, default=QDRANT_UPSERT_BATCH_SIZE)
    parser.add_argument("--source", type=Path, default=PROCESSED_DIR / "chunks.json")
    args = parser.parse_args()
    chunks = load_chunks(args.source)
    provider = create_embedding_provider(args.model, args.batch_size, args.device)
    collection = BGE_M3_COLLECTION if args.model == "bge-m3" else E5_COLLECTION
    store = QdrantStore(QDRANT_URL, QDRANT_API_KEY)
    store.ensure_collection(collection, provider.dimension, args.recreate)
    started = time.perf_counter()
    for start in range(0, len(chunks), args.batch_size):
        batch = chunks[start:start + args.batch_size]
        vectors = provider.embed_documents([chunk["text"] for chunk in batch])
        store.upsert(collection, batch, vectors, args.upsert_batch_size)
        print(f"Embedded/indexed {min(start + len(batch), len(chunks))}/{len(chunks)}", flush=True)
    store.create_payload_indexes(collection)
    count = store.count(collection)
    source_hash = hashlib.sha256(args.source.read_bytes()).hexdigest()
    manifest = {"collection_name": collection, "embedding_model": provider.model_name,
        "embedding_dimension": provider.dimension, "distance": "Cosine",
        "source_file": str(args.source.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "source_hash": source_hash, "total_chunks": len(chunks),
        "indexed_points": count, "model_revision": provider.model_revision,
        "chunk_size": CHUNK_SIZE, "chunk_overlap": CHUNK_OVERLAP,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "indexing_duration_seconds": time.perf_counter() - started}
    manifest_dir = PROJECT_ROOT / "data" / "vector_db" / "manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    (manifest_dir / ("bge_m3_manifest.json" if args.model == "bge-m3" else "multilingual_e5_base_manifest.json")).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"collection": collection, "source_chunks": len(chunks),
                      "indexed_points": count, "dimension": provider.dimension,
                      "duration_seconds": manifest["indexing_duration_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
