"""Bounded, process-local conversation state; never a documentary source."""

from datetime import datetime, timezone
from threading import Lock
from typing import Any


class ConversationStore:
    def __init__(self, max_messages: int = 10):
        self.max_messages = max(1, max_messages)
        self._sessions: dict[str, list[dict[str, Any]]] = {}
        self._lock = Lock()

    def get(self, session_id: str) -> list[dict[str, Any]]:
        with self._lock:
            return [dict(message) for message in self._sessions.get(session_id, [])]

    def append(self, session_id: str, role: str, content: str, **metadata: Any) -> None:
        message = {"role": role, "content": content,
                   "timestamp": datetime.now(timezone.utc).isoformat()}
        message.update(metadata)
        with self._lock:
            history = self._sessions.setdefault(session_id, [])
            history.append(message)
            del history[:-self.max_messages]

    def delete(self, session_id: str) -> bool:
        with self._lock:
            return self._sessions.pop(session_id, None) is not None

    def exists(self, session_id: str) -> bool:
        with self._lock:
            return session_id in self._sessions
