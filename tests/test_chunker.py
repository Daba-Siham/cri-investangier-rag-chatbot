from src.chunking.chunker import chunk_documents, split_text


def test_short_text_is_one_chunk_with_metadata():
    chunks = chunk_documents([{"document_id": "doc", "filename": "x.pdf",
                               "language": "fr", "pages": [{"page": 2, "text": "Bonjour"}]}],
                             chunk_size=20, chunk_overlap=5)
    assert len(chunks) == 1
    assert chunks[0]["chunk_id"] == "doc_p2_c1"
    assert chunks[0]["metadata"] == {"document_id": "doc", "filename": "x.pdf",
                                      "page": 2, "language": "fr", "chunk_index": 1}


def test_long_text_has_deterministic_ids_page_and_overlap():
    text = "abcdefghij " * 10
    first = chunk_documents([{"document_id": "doc", "filename": "x.pdf", "pages": [
        {"page": 7, "text": text}]}], chunk_size=30, chunk_overlap=5)
    second = chunk_documents([{"document_id": "doc", "filename": "x.pdf", "pages": [
        {"page": 7, "text": text}]}], chunk_size=30, chunk_overlap=5)
    assert len(first) > 1
    assert first == second
    assert all(chunk["metadata"]["page"] == 7 for chunk in first)
    assert first[1]["text"][:5] == first[0]["text"][-5:]
    assert all(len(chunk["text"]) <= 30 for chunk in first)
