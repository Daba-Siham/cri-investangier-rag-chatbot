"""Check local RAG dependencies without printing credentials."""

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utils.config import E5_COLLECTION, LLM_API_KEY, LLM_MODEL, QDRANT_URL


def _get_json(url: str):
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    qdrant_ok = False
    collection_ok = False
    try:
        data = _get_json(QDRANT_URL.rstrip("/") + "/collections")
        qdrant_ok = True
        collections = data.get("result", {}).get("collections", [])
        collection_ok = any(item.get("name") == E5_COLLECTION for item in collections)
        print("Qdrant HTTP: OK")
        print(f"E5 collection: {'OK' if collection_ok else 'MISSING'}")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, ValueError) as exc:
        print(f"Qdrant HTTP: ERROR ({exc})")
        print("E5 collection: UNKNOWN")
    print(f"LLM API key configured: {'YES' if bool(LLM_API_KEY) else 'NO'}")
    print(f"LLM model: {LLM_MODEL}")
    return 0 if qdrant_ok and collection_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
