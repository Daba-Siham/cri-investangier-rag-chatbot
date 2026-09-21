"""Loading and light structural validation for extracted document JSON."""

import json
import warnings as warnings_module
from pathlib import Path
from typing import Any


class JSONStructureError(ValueError):
    """Raised when a source JSON does not have the required structure."""


def discover_json_files(raw_dir: Path) -> list[Path]:
    """Return all JSON files in *raw_dir*, in deterministic order."""
    return sorted(Path(raw_dir).glob("*.json"))


def load_document(path: Path, warning_messages: list[str] | None = None) -> dict[str, Any]:
    """Load one UTF-8 document and validate only its required fields."""
    warning_messages = warning_messages if warning_messages is not None else []
    path = Path(path)
    try:
        with path.open("r", encoding="utf-8") as source:
            document = json.load(source)
    except (OSError, json.JSONDecodeError) as exc:
        raise JSONStructureError(f"Could not load {path.name}: {exc}") from exc

    if not isinstance(document, dict):
        raise JSONStructureError(f"{path.name}: root must be an object")
    for field in ("document_id", "filename", "pages"):
        if field not in document:
            raise JSONStructureError(f"{path.name}: missing required field '{field}'")
    if not isinstance(document["pages"], list):
        raise JSONStructureError(f"{path.name}: 'pages' must be a list")

    for index, page in enumerate(document["pages"], start=1):
        if not isinstance(page, dict) or "page" not in page or "text" not in page:
            raise JSONStructureError(f"{path.name}: page {index} must contain 'page' and 'text'")
        if page["text"] is None or not str(page["text"]).strip():
            message = f"{path.name}: page {page['page']} is empty"
            warning_messages.append(message)
            warnings_module.warn(message, UserWarning)
    return document


def load_documents(raw_dir: Path, warning_messages: list[str] | None = None,
                   error_messages: list[str] | None = None) -> list[dict[str, Any]]:
    """Discover and load valid documents, recording bad files instead of aborting."""
    warning_messages = warning_messages if warning_messages is not None else []
    error_messages = error_messages if error_messages is not None else []
    documents = []
    for path in discover_json_files(raw_dir):
        try:
            documents.append(load_document(path, warning_messages))
        except JSONStructureError as exc:
            error_messages.append(str(exc))
            warnings_module.warn(str(exc), UserWarning)
    return documents
