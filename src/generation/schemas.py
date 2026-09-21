import json


def parse_generation(raw: str) -> dict:
    try:
        value = json.loads(raw)
    except (TypeError, json.JSONDecodeError) as exc:
        raise ValueError("LLM returned malformed JSON") from exc
    if not isinstance(value, dict) or not isinstance(value.get("answer"), str):
        raise ValueError("LLM response answer must be a string")
    if not isinstance(value.get("source_ids"), list) or not all(isinstance(x, str) for x in value["source_ids"]):
        raise ValueError("LLM response source_ids must be a list of strings")
    if not isinstance(value.get("sufficient_context"), bool):
        raise ValueError("LLM response sufficient_context must be boolean")
    return value
