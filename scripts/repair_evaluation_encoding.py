"""Repair reversible mojibake in evaluation-only text files.

This intentionally touches no source documents, chunks, indexes, or retrieval
code. It maps the byte values represented by CP1252/Latin-1 artifacts back to
UTF-8 and writes explicit UTF-8 JSON/text.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def repair_text(text: str) -> str:
    suspicious = {0x00C2, 0x00C3, 0x00D8, 0x00D9}
    if not any(ord(char) in suspicious for char in text):
        return text
    raw = bytes(ord(char) if ord(char) < 256 else char.encode("cp1252")[0] for char in text)
    return raw.decode("utf-8")


def repair_value(value):
    if isinstance(value, str):
        return repair_text(value)
    if isinstance(value, list):
        return [repair_value(item) for item in value]
    if isinstance(value, dict):
        return {key: repair_value(item) for key, item in value.items()}
    return value


def main() -> None:
    question_path = ROOT / "evaluation" / "retrieval_questions.json"
    questions = json.loads(question_path.read_text(encoding="utf-8"))
    questions = repair_value(questions)
    question_path.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    review_path = ROOT / "evaluation" / "retrieval_questions_review.md"
    review_path.write_text(repair_text(review_path.read_text(encoding="utf-8")), encoding="utf-8")


if __name__ == "__main__":
    main()
