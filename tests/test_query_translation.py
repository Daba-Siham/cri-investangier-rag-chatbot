from src.rag.query_translation import AmazighRetrievalTranslator, TRANSLATION_SYSTEM_PROMPT


class FakeLLM:
    def __init__(self, result='{"translation":"Comment le CRI m’accompagne-t-il dans la recherche de foncier ?",'
                 '"retrieval_queries":["accompagnement du CRI recherche de foncier",'
                 '"foncier terrain industriel investissement", "services CRI accès au terrain"]}'):
        self.result = result
        self.calls = []

    def generate(self, messages, **kwargs):
        self.calls.append((messages, kwargs))
        return self.result


def test_amazigh_translation_is_retrieval_only_and_deterministic():
    llm = FakeLLM()
    translator = AmazighRetrievalTranslator(llm)
    result = translator.translate("ⵎⴰⵏ ⵉⵎⵎⴰⵙⵏ ⴳ 2023؟")
    assert result["translation"].startswith("Comment le CRI")
    assert len(result["retrieval_queries"]) == 3
    assert llm.calls[0][0][0]["content"].startswith(TRANSLATION_SYSTEM_PROMPT)
    assert llm.calls[0][1]["temperature"] == 0.0
    assert llm.calls[0][1]["_response_format"]["type"] == "json_schema"


def test_empty_translation_is_rejected():
    try:
        AmazighRetrievalTranslator(FakeLLM('{"translation":"   ","retrieval_queries":[]}')).translate("ⵙⵇⵙⴰ")
    except ValueError as exc:
        assert "incomplete" in str(exc)
    else:
        raise AssertionError("empty translation should fail")


def test_malformed_translation_json_is_rejected():
    try:
        AmazighRetrievalTranslator(FakeLLM("not-json")).translate("ⵙⵇⵙⴰ")
    except ValueError as exc:
        assert "valid JSON" in str(exc)
    else:
        raise AssertionError("malformed translation should fail")
