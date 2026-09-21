"""Conservative follow-up query rewriting without answering or adding facts."""

import re
from typing import Any

from src.conversation.router import route_message

YEAR_RE = re.compile(r"\b(?:19|20)\d{2}\b")

_FOLLOW_UP_PATTERNS = (
    r"^\s*(?:et|and|y|وماذا عن|وفي سنة|ونفس الشيء)\b",
    r"^\s*(?:what about|and for|the same)\b",
    r"^\s*(?:et pour|et celui|et elle|et eux|la même chose)\b",
    r"^\s*(?:¿?y en|¿?y para|lo mismo)\b",
)


def needs_rewrite(message: str, history: list[dict[str, Any]]) -> bool:
    if not history or len(message.strip()) > 240:
        return False
    return any(re.search(pattern, message, re.IGNORECASE) for pattern in _FOLLOW_UP_PATTERNS)


def _documentary_user_messages(history: list[dict[str, Any]]) -> list[str]:
    """Return documentary user turns, including a conservative legacy fallback."""
    messages = []
    for item in reversed(history):
        if item.get("role") != "user" or not item.get("content"):
            continue
        kind = item.get("kind")
        if kind == "document":
            messages.append(item["content"])
        elif kind is None and route_message(item["content"]).get("intent") == "DOCUMENT_QUERY":
            messages.append(item["content"])
    return messages


class QueryRewriter:
    """Rewrite clear follow-ups from the latest documentary user turn."""

    def rewrite(self, current_message: str, history: list[dict[str, Any]]) -> str:
        previous = next(iter(_documentary_user_messages(history)), "")
        if not previous:
            return current_message
        current_years = YEAR_RE.findall(current_message)
        if current_years:
            replacement = current_years[-1]
            rewritten = YEAR_RE.sub(replacement, previous, count=1)
            if rewritten != previous:
                return rewritten
        return f"{previous.rstrip(' ?؟')} {current_message.strip()}"
