"""Conservative, Unicode-preserving text cleanup."""

import re


_INVISIBLE = "".join(chr(code) for code in range(32) if code not in (9, 10, 13))
_INVISIBLE_RE = re.compile(f"[{re.escape(_INVISIBLE)}]")


def normalize_text(text: str | None) -> str:
    """Normalize whitespace without changing words, punctuation, or meaning."""
    if text is None:
        return ""
    cleaned = _INVISIBLE_RE.sub("", str(text)).replace("\u00a0", " ")
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n[ \t]+", "\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()
