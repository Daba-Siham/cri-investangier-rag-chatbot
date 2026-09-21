from typing import Any
from pydantic import BaseModel, Field
from src.utils.config import MAX_USER_MESSAGE_CHARACTERS


class ChatRequest(BaseModel):
    message: str = Field(..., max_length=MAX_USER_MESSAGE_CHARACTERS)
    session_id: str | None = None
    include_diagnostics: bool = False


class ChatResponse(BaseModel):
    session_id: str
    status: str
    answer: str = ""
    citations: list[dict[str, Any]] = Field(default_factory=list)
    retrieval: dict[str, Any] | None = None
    llm: dict[str, Any] | None = None
    diagnostics: dict[str, Any] | None = None
    kind: str | None = None
