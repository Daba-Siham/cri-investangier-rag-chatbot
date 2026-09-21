"""Final evidence selection and documentary context formatting."""

from typing import Any


def select_context(results: list[dict[str, Any]], final_k: int, max_characters: int) -> tuple[list[dict[str, Any]], bool]:
    selected, used = [], 0
    limited = False
    for result in results:
        text = result.get("text", "")
        addition = len(text) + 1
        if selected and used + addition > max_characters:
            limited = True
            break
        selected.append(result)
        used += addition
        if len(selected) >= final_k:
            break
    return selected, limited


def format_context(results: list[dict[str, Any]]) -> str:
    blocks = []
    for index, result in enumerate(results, 1):
        blocks.append(f"[SOURCE {index}]\nDocument: {result.get('filename') or result.get('document_id')}\n"
                      f"Page: {result.get('page')}\nLanguage: {result.get('language')}\nText:\n{result.get('text', '')}")
    return "\n\n".join(blocks)
