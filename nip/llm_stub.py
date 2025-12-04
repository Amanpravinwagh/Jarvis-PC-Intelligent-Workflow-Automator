# Optional LLM integration stub. Replace with OpenAI or other LLM call.
# This file provides `interpret_via_llm(text)` that returns structured actions.
# Keep your API key secret if you wire an external LLM.

def interpret_via_llm(text: str) -> dict:
    # Example return format
    # { "task": "custom", "actions": [ {"type":"open_app","value":"notepad"}, ... ] }
    # This is a stub. Integrate with OpenAI or another LLM if you want richer parsing.
    return {"task": "unknown", "actions": []}
