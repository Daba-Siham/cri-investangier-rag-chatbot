"""Small, deterministic language helpers shared by conversation and RAG."""

import re


# Tifinagh and Tifinagh punctuation occupy U+2D30..U+2D7F.
TIFINAGH_RE = re.compile(r"[\u2d30-\u2d7f]")


def is_tifinagh(message: str) -> bool:
    """Return True when a message contains a meaningful amount of Tifinagh."""
    tifinagh_count = len(TIFINAGH_RE.findall(message))
    letter_count = sum(char.isalpha() for char in message)
    return tifinagh_count >= 2 and (letter_count == 0 or tifinagh_count / letter_count >= 0.3)
