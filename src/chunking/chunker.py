"""Page-preserving recursive chunking for multilingual text."""

from typing import Any

from src.utils.config import CHUNK_OVERLAP, CHUNK_SIZE


SEPARATORS = ("\n\n", "\n", ". ", "؟ ", "؛ ", "، ", " ", "")


def _split_recursive(text: str, limit: int, separators: tuple[str, ...]) -> list[str]:
    if len(text) <= limit:
        return [text]
    separator = separators[-1]
    remaining = separators
    for candidate in separators:
        if candidate and candidate in text:
            separator = candidate
            remaining = separators[separators.index(candidate) + 1:]
            break
    if separator == "":
        return [text[i:i + limit] for i in range(0, len(text), limit)]
    pieces = text.split(separator)
    result: list[str] = []
    current = ""
    for piece in pieces:
        candidate = piece if not current else current + separator + piece
        if len(candidate) <= limit:
            current = candidate
        else:
            if current:
                result.extend(_split_recursive(current, limit, remaining))
            current = piece
    if current:
        result.extend(_split_recursive(current, limit, remaining))
    return [part for part in result if part]


def split_text(text: str, chunk_size: int = CHUNK_SIZE,
               chunk_overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text recursively, applying character overlap between chunks."""
    if not text:
        return []
    if chunk_size <= 0 or chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_size must be positive and overlap must be smaller")
    pieces = _split_recursive(text, chunk_size, SEPARATORS)
    chunks: list[str] = []
    for piece in pieces:
        if not chunks:
            chunks.append(piece.strip())
            continue
        remaining_piece = piece
        while remaining_piece:
            prefix = chunks[-1][-chunk_overlap:] if chunk_overlap else ""
            available = chunk_size - len(prefix)
            # Limit newly added content so the overlap prefix can never make
            # the final chunk exceed chunk_size.
            chunks.append((prefix + remaining_piece[:available]).strip())
            remaining_piece = remaining_piece[available:]
    return [chunk for chunk in chunks if chunk]


def chunk_documents(documents: list[dict[str, Any]], chunk_size: int = CHUNK_SIZE,
                    chunk_overlap: int = CHUNK_OVERLAP) -> list[dict[str, Any]]:
    """Create traceable chunks from each page, never crossing page boundaries."""
    output = []
    for document in documents:
        for page in document["pages"]:
            page_chunks = split_text(str(page.get("text") or ""), chunk_size, chunk_overlap)
            for index, text in enumerate(page_chunks, start=1):
                metadata = {
                    "document_id": document["document_id"],
                    "filename": document["filename"],
                    "page": page["page"],
                    "language": document.get("language"),
                    "chunk_index": index,
                }
                output.append({
                    "chunk_id": f"{document['document_id']}_p{page['page']}_c{index}",
                    "text": text,
                    "metadata": metadata,
                })
    return output
