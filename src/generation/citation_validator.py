def validate_and_map(source_ids: list[str], source_map: dict[str, dict]) -> list[dict]:
    citations, seen = [], set()
    for source_id in source_ids:
        if source_id not in source_map:
            raise ValueError(f"Unknown citation source ID: {source_id}")
        result = source_map[source_id]
        identity = (result.get("document_id"), result.get("page"))
        if identity in seen:
            continue
        seen.add(identity)
        citations.append({"source_id": source_id, **{key: result.get(key) for key in
                        ("document_id", "filename", "page", "language", "chunk_id")}})
    return citations
