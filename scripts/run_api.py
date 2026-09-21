"""Run the Task 6 API with shared model/retrieval dependencies."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import uvicorn
from src.api.app import app
from src.utils.config import API_HOST, API_PORT


if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)
