from src.conversation.router import response_for_control, route_message


def test_social_messages_bypass_document_retrieval():
    assert route_message("hi")["intent"] == "SOCIAL"
    assert route_message("bonjour")["action"] == "greeting"
    assert route_message("مرحبا")["language"] == "ar"
    assert route_message("my name is Siham")["action"] == "introduction"
    assert route_message("what can you do?")["action"] == "scope"
    assert route_message("hi my name is Siham")["intent"] == "SOCIAL"
    assert route_message("bonjour je m'appelle Siham")["intent"] == "SOCIAL"
    assert route_message("مرحبا اسمي سهام")["intent"] == "SOCIAL"
    assert route_message("hola, me llamo Siham")["intent"] == "SOCIAL"


def test_common_greeting_variants_are_social():
    for message in ("bonjour chat", "salut chat", "hello chat", "hii", "hiii", "coucou"):
        routed = route_message(message)
        assert routed["intent"] == "SOCIAL"
        assert routed["action"] == "greeting"


def test_tifinagh_greeting_is_social_and_language_is_tzm():
    routed = route_message("ⴰⵣⵓⵍ")
    assert routed == {"intent": "SOCIAL", "action": "greeting", "language": "tzm"}


def test_tifinagh_information_question_remains_a_document_query():
    routed = route_message("ⵎⴰⵏ ⵉⵎⵙⵙⵉⵔⵏ ⵏ ⵜⵎⵏⴰⴹⵜ؟")
    assert routed["intent"] == "DOCUMENT_QUERY" and routed["language"] == "tzm"


def test_external_knowledge_question_defaults_to_document_query():
    assert route_message("What is the weather today?")["intent"] == "DOCUMENT_QUERY"
    assert route_message("What is Bitcoin worth?")["intent"] == "DOCUMENT_QUERY"


def test_control_repeats_only_a_valid_previous_answer():
    result = response_for_control([{"role": "assistant", "content": "709", "status": "answered", "citations": [{"page": 25}]}], "en")
    assert result["answer"] == "709" and result["status"] == "answered"
    assert result["citations"] == [{"page": 25}]
    result = response_for_control([{"role": "assistant", "content": "", "status": "generation_error"}], "en")
    assert result["status"] == "control" and "retry" in result["answer"].lower()
