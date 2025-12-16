import os
from typing import List, Dict, Any

import ollama

DEFAULT_MODEL = os.getenv("BUDDY_MODEL", "phi3:mini")  # or "llama3:8b"


def chat_ollama(
    messages: List[Dict[str, str]],
    model: str | None = None,
    temperature: float = 0.1,
) -> str:
    model = model or DEFAULT_MODEL
    resp = ollama.chat(
        model=model,
        messages=messages,
        options={"temperature": temperature},
    )
    return resp["message"]["content"]
