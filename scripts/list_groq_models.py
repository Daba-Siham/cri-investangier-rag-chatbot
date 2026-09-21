"""List models visible to the configured Groq account."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from src.utils.config import LLM_API_KEY


def main():
    if not LLM_API_KEY:
        raise SystemExit("LLM_API_KEY is not configured.")
    from groq import Groq
    for model in Groq(api_key=LLM_API_KEY).models.list().data:
        print(model.id)


if __name__ == "__main__": main()
