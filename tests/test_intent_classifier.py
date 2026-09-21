import json

from src.api.app import create_app
from src.conversation.intent_classifier import IntentClassifier
from src.conversation.memory import ConversationStore
from src.conversation.router import route_message


class FakeClassifier:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error
        self.calls = []

    def classify(self, message):
        self.calls.append(message)
        if self.error:
            raise self.error
        return self.result


class FakeLLM:
    def __init__(self, content):
        self.content = content
        self.calls = []

    def generate(self, messages, **kwargs):
        self.calls.append((messages, kwargs))
        return self.content


def test_classifier_returns_strict_structured_intent_and_uses_small_budget():
    llm = FakeLLM(json.dumps({"intent": "social", "language": "fr"}))
    result = IntentClassifier(llm).classify("bonjour ghiitaa")
    assert result == {"intent": "social", "language": "fr"}
    assert llm.calls[0][1]["max_tokens"] == 80
    assert llm.calls[0][1]["temperature"] == 0


def test_ambiguous_messages_are_classified_without_growing_greeting_dictionary():
    social = FakeClassifier({"intent": "social", "language": "fr"})
    assert route_message("bonjour ghiitaa", social)["intent"] == "SOCIAL"
    assert route_message("hiii madame", social)["intent"] == "SOCIAL"
    assert social.calls == ["bonjour ghiitaa", "hiii madame"]


def test_requested_social_examples_route_to_social():
    classifier = FakeClassifier({"intent": "social", "language": "fr"})
    messages = ("bonjour", "bonjour chat", "bonjour ghiitaa", "bonjour AI", "bonjour madame",
                "hiii", "hiii madame", "hello there", "salut tout le monde", "merci",
                "merci beaucoup", "au revoir", "ⴰⵣⵓⵍ")
    for message in messages:
        assert route_message(message, classifier)["intent"] == "SOCIAL"


def test_requested_rag_examples_route_to_document_query():
    classifier = FakeClassifier({"intent": "rag", "language": "fr"})
    messages = ("bonjour, combien de projets ont été approuvés en 2024 ?",
                "salut, comment créer une entreprise ?", "hi, what support does the CRI provide?",
                "ما هو عدد المشاريع المصادق عليها؟")
    for message in messages:
        assert route_message(message, classifier)["intent"] == "DOCUMENT_QUERY"


def test_mixed_greeting_and_question_is_document_query():
    rag = FakeClassifier({"intent": "rag", "language": "fr"})
    routed = route_message("bonjour, combien de projets ont été approuvés en 2024 ?", rag)
    assert routed["intent"] == "DOCUMENT_QUERY"


def test_classifier_failure_conservatively_falls_back_to_document_query(caplog):
    routed = route_message("bonjour AI", FakeClassifier(error=RuntimeError("provider details")))
    assert routed["intent"] == "DOCUMENT_QUERY"
    assert "Intent classification failed; using fallback route" in caplog.text


class FakeRAG:
    def __init__(self):
        self.calls = []

    def answer(self, question, retrieval_query=None):
        self.calls.append(question)
        return {"status": "answered", "answer": "answer", "citations": []}


def test_social_route_does_not_call_rag_and_informational_route_does():
    rag = FakeRAG()
    classifier = FakeClassifier({"intent": "social", "language": "fr"})
    from fastapi.testclient import TestClient
    with TestClient(create_app(rag, ConversationStore(), intent_classifier=classifier)) as api:
        api.post("/chat", json={"message": "bonjour ghiitaa"})
    assert rag.calls == []

    rag = FakeRAG()
    classifier = FakeClassifier({"intent": "rag", "language": "fr"})
    with TestClient(create_app(rag, ConversationStore(), intent_classifier=classifier)) as api:
        api.post("/chat", json={"message": "bonjour, combien de projets ont été approuvés en 2024 ?"})
    assert len(rag.calls) == 1
