"""Phase 4B: validate, embed, and ingest the final retrieval artifact into v2 only."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
import statistics
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parents[1]
JSONL = ROOT / "data" / "retrieval_v2" / "retrieval_chunks.jsonl"
MANIFEST = ROOT / "data" / "retrieval_v2" / "retrieval_manifest.json"
REPORT = ROOT / "data" / "retrieval_v2" / "qdrant_ingestion_report.md"
MODEL_NAME = "intfloat/multilingual-e5-base"
TOKENIZER_NAME = MODEL_NAME
DIMENSION = 768
DISTANCE = models.Distance.COSINE
COLLECTION = "cri_chunks_multilingual_e5_v2"
BASE_COLLECTION = "cri_chunks_multilingual_e5_base"
EXPECTED_DOCUMENTS = 33
EXPECTED_PARENTS = 913
EXPECTED_RECORDS = 1901
EXPECTED_INDEXABLE = 1894
MAX_TOKENS = 500
POINT_NAMESPACE = uuid.UUID("1e4df3b2-8dd9-4a2a-a4a3-2bf1b2a743a0")
PAYLOAD_FIELDS = [
    "retrieval_chunk_id", "parent_semantic_chunk_id", "document_id", "document_family_id", "filename", "language", "document_title",
    "topic_id", "content_type", "semantic_tags", "heading_path", "page_start", "page_end", "source_pages", "page_mapping_precision",
    "primary_year", "years_mentioned", "reference_period_type", "reference_period_year", "reference_period_end_date",
    "retrieval_chunk_index", "retrieval_chunk_count", "is_subchunk", "indexable", "text",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def package_version(name: str):
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "not-installed"


def resolve_model_source():
    configured = os.getenv("E5_MODEL_PATH")
    if configured and Path(configured).exists():
        return configured
    cache = Path.home() / ".cache" / "huggingface" / "hub" / "models--intfloat--multilingual-e5-base" / "snapshots"
    snapshots = sorted((path for path in cache.glob("*") if path.is_dir()), key=lambda path: path.stat().st_mtime, reverse=True)
    return str(snapshots[0]) if snapshots else MODEL_NAME


def point_id(retrieval_chunk_id: str) -> str:
    return str(uuid.uuid5(POINT_NAMESPACE, retrieval_chunk_id))


def load_records():
    manifest = json.loads(MANIFEST.read_text(encoding="utf8"))
    actual_hash = sha256(JSONL)
    errors = []
    if manifest.get("jsonl_sha256") != actual_hash:
        errors.append(f"JSONL hash mismatch: manifest={manifest.get('jsonl_sha256')} actual={actual_hash}")
    checks = {
        "retrieval_schema_version": "2.0",
        "source_schema_version": "2.2",
        "source_semantic_document_count": EXPECTED_DOCUMENTS,
        "source_semantic_chunk_count": EXPECTED_PARENTS,
    }
    for key, expected in checks.items():
        actual = manifest.get(key)
        if actual != expected:
            errors.append(f"{key}: expected {expected}, got {actual}")
    mapping = manifest.get("page_mapping_precision_counts", {})
    if mapping.get("parent", 0) != 0 or mapping.get("exact") != EXPECTED_RECORDS:
        errors.append(f"page mapping check failed: {mapping}")
    if manifest.get("determinism_test", {}).get("status") != "PASS":
        errors.append("manifest determinism status is not PASS")
    records = [json.loads(line) for line in JSONL.read_text(encoding="utf8").splitlines() if line.strip()]
    if len(records) != EXPECTED_RECORDS:
        errors.append(f"retrieval record count: expected {EXPECTED_RECORDS}, got {len(records)}")
    indexable = [record for record in records if record.get("indexable") is True]
    if len(indexable) != EXPECTED_INDEXABLE:
        errors.append(f"indexable record count: expected {EXPECTED_INDEXABLE}, got {len(indexable)}")
    ids = [record.get("retrieval_chunk_id") for record in indexable]
    if len(ids) != len(set(ids)):
        errors.append("indexable retrieval IDs are not unique")
    for record in records:
        if record.get("page_mapping_precision") != "exact":
            errors.append(f"non-exact page mapping: {record.get('retrieval_chunk_id')}")
        if not isinstance(record.get("indexable"), bool) or not record.get("indexability_reason"):
            errors.append(f"invalid indexability fields: {record.get('retrieval_chunk_id')}")
    if errors:
        raise RuntimeError("Artifact validation failed:\n- " + "\n- ".join(errors))
    return manifest, records, actual_hash


def exact_token_validation(records, tokenizer):
    indexable = [record for record in records if record["indexable"]]
    stored = [record.get("embedding_token_count") for record in indexable]
    exact = []
    differences = []
    for record in indexable:
        count = len(tokenizer.encode(record["embedding_text"], add_special_tokens=True, truncation=False))
        exact.append(count)
        if count != record.get("embedding_token_count"):
            differences.append((record["retrieval_chunk_id"], record.get("embedding_token_count"), count))
        if count > MAX_TOKENS:
            raise RuntimeError(f"Exact final embedding input exceeds {MAX_TOKENS} tokens: {record['retrieval_chunk_id']}={count}")
    return {"stored_max": max(stored), "exact_max": max(exact), "differing_count": len(differences), "max_difference": max((abs(a - b) for _, a, b in differences), default=0), "exact_over_500": sum(value > MAX_TOKENS for value in exact), "exact_counts": exact, "differences": differences}


def compact_payload(record):
    return {field: record.get(field) for field in PAYLOAD_FIELDS}


def collection_snapshot(client, name):
    if not client.collection_exists(name):
        return {"exists": False, "name": name}
    info = client.get_collection(name)
    config = info.config.params.vectors
    if isinstance(config, dict):
        vector_config = {key: {"size": value.size, "distance": str(value.distance)} for key, value in config.items()}
    else:
        vector_config = {"size": getattr(config, "size", None), "distance": str(getattr(config, "distance", None))}
    return {"exists": True, "name": name, "points": int(client.count(collection_name=name, exact=True).count), "vectors": vector_config}


def create_indexes(client):
    created = []
    for field in ("document_id", "document_family_id", "language", "content_type", "topic_id", "semantic_tags"):
        client.create_payload_index(collection_name=COLLECTION, field_name=field, field_schema=models.PayloadSchemaType.KEYWORD, wait=True)
        created.append({"field": field, "schema": "keyword"})
    for field in ("primary_year", "reference_period_year"):
        client.create_payload_index(collection_name=COLLECTION, field_name=field, field_schema=models.PayloadSchemaType.INTEGER, wait=True)
        created.append({"field": field, "schema": "integer"})
    return created


def search(client, model, question, limit=5):
    vector = model.encode([f"query: {question}"], normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False)[0].tolist()
    if hasattr(client, "query_points"):
        response = client.query_points(collection_name=COLLECTION, query=vector, limit=limit, with_payload=True)
        return list(response.points)
    return list(client.search(collection_name=COLLECTION, query_vector=vector, limit=limit, with_payload=True))


def safe_host(url: str):
    from urllib.parse import urlsplit
    parsed = urlsplit(url)
    return f"{parsed.scheme}://{parsed.hostname or '<local>'}:{parsed.port or (443 if parsed.scheme == 'https' else 80)}"


def write_report(data):
    lines = ["# Phase 4B — Qdrant v2 ingestion report", "", f"- Status: **{data['status']}**", f"- Timestamp UTC: `{data['timestamp']}`", f"- Failure reason: `{data.get('error', 'none')}`", "", "## Configuration", "", f"- Collection: `{COLLECTION}`", f"- Existing production collection: `{BASE_COLLECTION}` (never modified)", f"- Qdrant endpoint: `{data['endpoint']}`", f"- Model: `{MODEL_NAME}`", f"- Local model source used: `{data.get('model_source')}`", f"- Tokenizer: `{TOKENIZER_NAME}`", f"- Vector dimension: {DIMENSION}", f"- Distance: COSINE", f"- Device: `{data.get('device')}`", f"- Batch size: {data.get('batch_size')}", "- Normalization: `normalize_embeddings=True`", "", "## Artifact validation", "", f"- JSONL SHA-256: `{data.get('jsonl_hash')}`", f"- Source records: {data.get('source_records')}", f"- Indexable records: {data.get('indexable_records')}", f"- Skipped non-indexable records: {data.get('skipped_non_indexable')}", "", "## Exact token validation", "", f"- Stored maximum token count: {data.get('stored_token_max')}", f"- Exact final maximum token count: {data.get('exact_token_max')}", f"- Exact inputs over 500: {data.get('exact_over_500')}", f"- Records with stored/exact count differences: {data.get('token_count_differences')}", f"- Maximum absolute difference: {data.get('max_token_difference')}", "", "## Ingestion", "", f"- Expected point count: {data.get('indexable_records')}", f"- Inserted point count: {data.get('inserted_points')}", f"- Deterministic point IDs: UUID5 with fixed namespace, derived from `retrieval_chunk_id`", f"- Payload indexes: {json.dumps(data.get('payload_indexes', []), ensure_ascii=False)}", "- Full `source_spans` stored in Qdrant: **no**", "- `embedding_text` stored in Qdrant: **no**", "", "## Vector sanity", "", f"- Dimension check: {data.get('dimension_check')}", f"- Finite values: {data.get('finite_check')}", f"- Norm min/median/max: {data.get('norm_min')} / {data.get('norm_median')} / {data.get('norm_max')}", "", "## Collection protection", "", f"- Base collection before: `{json.dumps(data.get('base_before'), ensure_ascii=False)}`", f"- Base collection after: `{json.dumps(data.get('base_after'), ensure_ascii=False)}`", f"- Base collection unchanged: **{data.get('base_unchanged')}**", "", "## Multilingual dense-vector smoke searches", ""]
    for item in data.get("smoke_tests", []):
        lines += [f"### {item['language']} — {item['question']}", "", "| Rank | Score | Language | Filename | Parent | Topic | Type | Pages | Preview |", "|---:|---:|---|---|---|---|---|---|---|"]
        for rank, result in enumerate(item["results"], 1):
            lines.append(f"| {rank} | {result['score']:.6f} | {result['language']} | {result['filename']} | {result['parent']} | {result['topic']} | {result['content_type']} | {result['pages']} | {result['preview']} |")
        lines.append("")
    lines += ["## Package versions", ""]
    for package in ("sentence-transformers", "transformers", "qdrant-client", "torch"):
        lines.append(f"- `{package}`: {data.get('packages', {}).get(package)}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--recreate", action="store_true", help="delete and recreate v2 only; production collection is always protected")
    parser.add_argument("--batch-size", type=int, default=int(os.getenv("EMBEDDING_BATCH_SIZE", "32")))
    parser.add_argument("--upsert-batch-size", type=int, default=int(os.getenv("QDRANT_UPSERT_BATCH_SIZE", "128")))
    parser.add_argument("--device", default=None, help="SentenceTransformer device, e.g. cpu or cuda")
    args = parser.parse_args()
    load_dotenv(ROOT / ".env", override=False)
    endpoint = os.getenv("QDRANT_URL", "http://localhost:6333")
    api_key = os.getenv("QDRANT_API_KEY") or None
    report = {"status": "FAIL", "timestamp": datetime.now(timezone.utc).isoformat(), "endpoint": safe_host(endpoint), "batch_size": args.batch_size, "device": args.device}
    try:
        manifest, records, artifact_hash = load_records()
        report.update({"jsonl_hash": artifact_hash, "source_records": len(records), "indexable_records": sum(r["indexable"] for r in records), "skipped_non_indexable": sum(not r["indexable"] for r in records)})
        model_source = resolve_model_source()
        local_model = Path(model_source).is_dir()
        tokenizer = AutoTokenizer.from_pretrained(model_source, local_files_only=local_model)
        token_stats = exact_token_validation(records, tokenizer)
        report.update({"stored_token_max": token_stats["stored_max"], "exact_token_max": token_stats["exact_max"], "exact_over_500": token_stats["exact_over_500"], "token_count_differences": token_stats["differing_count"], "max_token_difference": token_stats["max_difference"]})
        if token_stats["exact_over_500"]:
            raise RuntimeError("Exact token validation exceeded the safe 500-token budget")
        indexable = [record for record in records if record["indexable"]]
        point_ids = [point_id(record["retrieval_chunk_id"]) for record in indexable]
        if len(point_ids) != len(set(point_ids)):
            raise RuntimeError("Deterministic Qdrant point IDs are not unique")
        model = SentenceTransformer(model_source, device=args.device) if args.device else SentenceTransformer(model_source)
        report["model_source"] = model_source
        report["device"] = str(getattr(model, "device", args.device or "auto"))
        texts = [record["embedding_text"] for record in indexable]
        # Deterministic length bucketing reduces padding on CPU/GPU without
        # changing inputs or the final record/vector order.
        order = sorted(range(len(indexable)), key=lambda index: (indexable[index]["embedding_token_count"], indexable[index]["retrieval_chunk_id"]))
        encoded_sorted = model.encode([texts[index] for index in order], batch_size=args.batch_size, normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=True)
        vectors = [None] * len(encoded_sorted)
        for sorted_index, original_index in enumerate(order):
            vectors[original_index] = encoded_sorted[sorted_index]
        if len(vectors) != len(indexable) or any(len(vector) != DIMENSION for vector in vectors):
            raise RuntimeError("Embedding count or dimension mismatch")
        if not all(math.isfinite(float(value)) for vector in vectors for value in vector):
            raise RuntimeError("Embedding contains NaN or infinity")
        norms = [math.sqrt(sum(float(value) ** 2 for value in vector)) for vector in vectors]
        report.update({"dimension_check": "PASS", "finite_check": "PASS", "norm_min": min(norms), "norm_median": statistics.median(norms), "norm_max": max(norms), "packages": {name: package_version(name) for name in ("sentence-transformers", "transformers", "qdrant-client", "torch")}})
        client = QdrantClient(url=endpoint, api_key=api_key)
        base_before = collection_snapshot(client, BASE_COLLECTION)
        v2_before = collection_snapshot(client, COLLECTION)
        report["base_before"] = base_before
        if v2_before["exists"] and not args.recreate:
            raise RuntimeError(f"Target collection already exists; rerun with --recreate to rebuild only {COLLECTION}")
        if not base_before["exists"]:
            raise RuntimeError(f"Protected production collection does not exist: {BASE_COLLECTION}")
        print(json.dumps({"endpoint": report["endpoint"], "target": COLLECTION, "target_exists": v2_before["exists"], "expected_points": len(indexable)}))
        if v2_before["exists"] and args.recreate:
            client.delete_collection(COLLECTION)
        client.create_collection(collection_name=COLLECTION, vectors_config=models.VectorParams(size=DIMENSION, distance=DISTANCE))
        payload_indexes = create_indexes(client)
        for start in range(0, len(indexable), args.upsert_batch_size):
            batch_records = indexable[start:start + args.upsert_batch_size]
            batch_vectors = vectors[start:start + args.upsert_batch_size]
            points = [models.PointStruct(id=point_id(record["retrieval_chunk_id"]), vector=vector.tolist(), payload=compact_payload(record)) for record, vector in zip(batch_records, batch_vectors)]
            client.upsert(collection_name=COLLECTION, points=points, wait=True)
        inserted = int(client.count(collection_name=COLLECTION, exact=True).count)
        if inserted != len(indexable):
            raise RuntimeError(f"Inserted point count mismatch: expected {len(indexable)}, got {inserted}")
        smoke_questions = [("French", "Quels sont les coûts de branchement ou les démarches pour l'électricité ?"), ("English", "What investment opportunities exist in the automotive sector?"), ("Arabic", "ما هي شروط الاستفادة من برامج التمويل؟"), ("Spanish", "¿Qué servicios ofrece el CRI a los inversores?")]
        smoke = []
        for language, question in smoke_questions:
            results = []
            for result in search(client, model, question):
                payload = result.payload or {}
                results.append({"score": float(result.score), "language": payload.get("language"), "filename": payload.get("filename"), "parent": payload.get("parent_semantic_chunk_id"), "topic": payload.get("topic_id"), "content_type": payload.get("content_type"), "pages": f"{payload.get('page_start')}–{payload.get('page_end')}", "preview": " ".join(str(payload.get("text", "")).split())[:180].replace("|", "\\|")})
            smoke.append({"language": language, "question": question, "results": results})
        base_after = collection_snapshot(client, BASE_COLLECTION)
        report.update({"inserted_points": inserted, "payload_indexes": payload_indexes, "base_after": base_after, "base_unchanged": base_before == base_after, "smoke_tests": smoke, "status": "PASS"})
        if not report["base_unchanged"]:
            raise RuntimeError("Protected production collection metadata changed")
    except Exception as exc:
        report["error"] = str(exc)
        write_report(report)
        raise
    write_report(report)
    print(json.dumps({"status": "PASS", "collection": COLLECTION, "points": report["inserted_points"], "report": str(REPORT)}))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Phase 4B failed: {exc}", file=sys.stderr)
        sys.exit(1)
