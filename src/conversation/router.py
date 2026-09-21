"""Conservative local routing for social and conversation-control turns."""
import re
import logging
from typing import Any

from src.utils.language import is_tifinagh

LOGGER = logging.getLogger(__name__)


def _language(message: str) -> str:
    if is_tifinagh(message):
        return "tzm"
    if any("\u0600" <= char <= "\u08ff" for char in message):
        return "ar"
    if any(char in message for char in "¿¡") or re.search(r"\b(hola|gracias|cuál|qué)\b", message, re.I):
        return "es"
    if re.search(r"\b(bonjour|salut|merci|qui es-tu|que peux-tu|répète|où est)\b", message, re.I):
        return "fr"
    return "en"


_GREETING_WORDS = {"hi", "hii", "hiii", "hello", "hey", "bonjour", "salut", "coucou"}
_GREETING_SUFFIXES = {"chat", "chatbot", "assistant"}


def _is_simple_greeting(text: str) -> bool:
    """Recognize a deliberately small set of greeting variants without an LLM."""
    normalized = re.sub(r"[.!?؟]+$", "", text).strip()
    parts = normalized.split()
    if len(parts) == 1:
        return parts[0] in _GREETING_WORDS
    return len(parts) == 2 and parts[0] in _GREETING_WORDS and parts[1] in _GREETING_SUFFIXES


def _classified_social_action(text: str) -> str:
    """Preserve the existing localized thanks response for broad social turns."""
    if re.match(r"^(?:thanks|thank you|merci|شكرا|gracias)\b", text, re.I):
        return "thanks"
    return "greeting"


def route_message(message: str, intent_classifier: Any | None = None) -> dict[str, Any]:
    text = " ".join(message.casefold().split())
    language = _language(message)
    if _is_simple_greeting(text):
        return {"intent": "SOCIAL", "action": "greeting", "language": language}
    combined = (
        r"(?:hi|hello|hey),?\s+(?:my name is|i['’]m)\s+[^.!?؟]{1,80}|"
        r"(?:bonjour|salut),?\s+(?:je m'appelle|moi c'est)\s+[^.!?؟]{1,80}|"
        r"(?:مرحبا|السلام عليكم)\s+اسمي\s+[^.!?؟]{1,80}|"
        r"hola,?\s+(?:me llamo|soy)\s+[^.!?؟]{1,80}"
    )
    if re.fullmatch(combined + r"[.!?؟]*", text, re.I):
        return {"intent": "SOCIAL", "action": "introduction", "language": language}
    if re.fullmatch(r"ⴰⵣⵓⵍ[.!?؟]*", text, re.I):
        return {"intent": "SOCIAL", "action": "greeting", "language": language}
    if re.fullmatch(r"(?:hi|hello|hey|bonjour|salut|salam|مرحبا|السلام عليكم|hola)[.!?؟]*", text, re.I):
        return {"intent": "SOCIAL", "action": "greeting", "language": language}
    if re.fullmatch(r"(?:thanks|thank you|merci|شكرا|gracias)[.!?؟]*", text, re.I):
        return {"intent": "SOCIAL", "action": "thanks", "language": language}
    if re.fullmatch(r"(?:who are you|what can you do|qui es-tu|que peux-tu faire|ماذا يمكنك أن تفعل)[؟?.!]*", text, re.I):
        return {"intent": "SOCIAL", "action": "scope", "language": language}
    if re.fullmatch(r"(?:my name is|je m'appelle|اسمي)\s+[^.!?؟]{1,80}[.!?؟]*", text, re.I):
        return {"intent": "SOCIAL", "action": "introduction", "language": language}
    control = (r"where is the answer|you didn't answer|you did not answer|repeat(?: the answer)?|"
               r"répète|tu n'as pas répondu|où est la réponse|لم تجب|أعد الجواب")
    if re.fullmatch(rf"(?:{control})[؟?.!]*", text, re.I):
        return {"intent": "CONVERSATION_CONTROL", "action": "repeat_or_recover", "language": language}
    if intent_classifier is not None:
        try:
            classified = intent_classifier.classify(message)
            intent = str(classified["intent"]).casefold()
            classified_language = str(classified.get("language") or language).casefold()
            if intent == "social":
                return {"intent": "SOCIAL", "action": _classified_social_action(text),
                        "language": classified_language}
            if intent == "conversation_control":
                return {"intent": "CONVERSATION_CONTROL", "action": "repeat_or_recover",
                        "language": classified_language}
            if intent == "rag":
                return {"intent": "DOCUMENT_QUERY", "action": None, "language": classified_language}
            raise ValueError("unsupported intent")
        except Exception:
            LOGGER.warning("Intent classification failed; using fallback route")
    return {"intent": "DOCUMENT_QUERY", "action": None, "language": language}


def response_for_social(message: str, action: str, language: str) -> str:
    if action == "introduction":
        match = re.search(r"(?:my name is|je m'appelle|moi c'est|i['’]m|me llamo|soy|اسمي)\s+(.+?)[.!?؟]*$", message, re.I)
        name = match.group(1).strip() if match else ""
        if language == "fr": return f"Enchanté{', ' + name if name else ''} ! Je peux vous aider à trouver des informations dans les documents du CRI."
        if language == "es": return f"Encantado{', ' + name if name else ''}. Puedo ayudarte a encontrar información en los documentos del CRI."
        if language == "ar": return f"تشرفت بلقائك{('، ' + name) if name else ''}. يمكنني مساعدتك في العثور على المعلومات في وثائق المركز الجهوي للاستثمار."
        return f"Nice to meet you{', ' + name if name else ''}. I can help you find information in the CRI documents."
    if action == "scope":
        return {"fr": "Je peux répondre à vos questions à partir des documents du CRI et indiquer les sources utilisées.",
                "es": "Puedo responder preguntas basándome en los documentos del CRI e indicar las fuentes utilizadas.",
                "ar": "يمكنني الإجابة عن أسئلتك بالاعتماد على وثائق المركز الجهوي للاستثمار وذكر المصادر المستخدمة.",
                "en": "I can answer questions based on the CRI documents and provide the source documents and pages used."}[language]
    if language == "tzm":
        # Initial wording only; a future language review should improve this localization.
        return "ⴰⵣⵓⵍ!" if action == "greeting" else "ⵜⴰⵏⵎⵎⵉⵔⵜ!"
    return {"fr": "Bonjour ! Je peux vous aider avec les documents du CRI." if action == "greeting" else "Avec plaisir !",
            "es": "¡Hola! Puedo ayudarte con los documentos del CRI." if action == "greeting" else "¡Con mucho gusto!",
            "ar": "مرحباً! يمكنني مساعدتك بشأن وثائق المركز الجهوي للاستثمار." if action == "greeting" else "على الرحب والسعة!",
            "en": "Hello! I can help you with the CRI documents." if action == "greeting" else "You're welcome!"}[language]


def response_for_control(history: list[dict[str, Any]], language: str) -> dict[str, Any]:
    previous = next((item for item in reversed(history) if item.get("role") == "assistant"), None)
    if previous and previous.get("status") == "answered" and str(previous.get("content", "")).strip():
        return {"answer": str(previous["content"]), "status": "answered",
                "citations": list(previous.get("citations") or [])}
    return {"answer": {"fr": "La réponse précédente n’a pas pu être générée correctement. Veuillez réessayer votre question.",
                        "es": "La respuesta anterior no se pudo generar correctamente. Vuelve a intentarlo.",
                        "ar": "تعذّر إنشاء الرد السابق بشكل صحيح. يرجى إعادة طرح سؤالك.",
                        "en": "The previous response could not be generated correctly. Please retry your question."}[language],
            "status": "control", "citations": []}
