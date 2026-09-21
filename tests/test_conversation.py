from src.conversation.memory import ConversationStore
from src.conversation.query_rewriter import QueryRewriter, needs_rewrite


def test_history_is_bounded_and_contains_visible_messages_only():
    store = ConversationStore(max_messages=2)
    store.append("s", "user", "one")
    store.append("s", "assistant", "two")
    store.append("s", "user", "three")
    history = store.get("s")
    assert [item["content"] for item in history] == ["two", "three"]
    assert all(set(item) >= {"role", "content", "timestamp"} for item in history)


def test_conservative_rewriter_replaces_previous_year():
    history = [{"role": "user", "content": "Combien de projets en 2024 ?"}]
    message = "Et en 2025 ?"
    assert needs_rewrite(message, history)
    assert QueryRewriter().rewrite(message, history) == "Combien de projets en 2025 ?"


def test_control_turn_does_not_replace_documentary_followup_base():
    history = [
        {"role": "user", "content": "Combien de projets ont été approuvés par la CRUI au premier semestre 2024 ?", "kind": "document"},
        {"role": "user", "content": "repeat", "kind": "control"},
    ]
    rewritten = QueryRewriter().rewrite("Et en 2025 ?", history)
    assert "repeat" not in rewritten and "CRUI" in rewritten and "2025" in rewritten


def test_social_turn_does_not_replace_documentary_followup_base():
    history = [
        {"role": "user", "content": "What projects in 2024?", "kind": "document"},
        {"role": "user", "content": "hi my name is siham", "kind": "social"},
    ]
    assert QueryRewriter().rewrite("Et en 2025 ?", history) == "What projects in 2025?"


def test_legacy_history_ignores_recognized_control_messages():
    history = [{"role": "user", "content": "What projects in 2024?"}, {"role": "user", "content": "repeat"}]
    assert QueryRewriter().rewrite("Et en 2025 ?", history) == "What projects in 2025?"


def test_standalone_message_bypasses_rewriter():
    assert not needs_rewrite("Combien de projets en 2024 ?", [{"role": "user", "content": "hello"}])
