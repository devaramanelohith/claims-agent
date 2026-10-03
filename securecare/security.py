"""Secret-handling helpers. Pure Python: no Streamlit import, no global state.

RULES THIS PROJECT FOLLOWS FOR THE VISITOR'S API KEY (OpenRouter, Gemini or OpenAI)
  1. The key lives only in the visitor's own Streamlit session (a widget value).
  2. It is passed explicitly to the LLM client; it is never written to os.environ,
     a module global, a file, a log line, the graph state, or any st.cache_* function.
  3. It is flushed from the session after every use (unless the visitor opts to keep it).
"""
from __future__ import annotations

import re

_KEY_PATTERN = re.compile(r"sk-[A-Za-z0-9_\-\*\.]{6,}")
_GOOGLE_KEY_PATTERN = re.compile(r"AIza[A-Za-z0-9_\-]{10,}")

# provider -> (required prefix, human hint shown when the check fails)
KEY_PREFIXES = {
    "openrouter": ("sk-or-", "it should start with 'sk-or-'"),
    "gemini": ("AIza", "it should start with 'AIza'"),
    "openai": ("sk-", "it should start with 'sk-'"),
}


def looks_like_api_key(value: str, provider: str = "openai") -> bool:
    """Cheap sanity check for the chosen provider; it does NOT verify the key online."""
    value = (value or "").strip()
    prefix = KEY_PREFIXES.get(provider, ("", ""))[0]
    return value.startswith(prefix) and len(value) >= 20 and " " not in value


def looks_like_openai_key(value: str) -> bool:
    return looks_like_api_key(value, "openai")


def key_hint(provider: str) -> str:
    return KEY_PREFIXES.get(provider, ("", "check the key"))[1]


def redact_secrets(text: str) -> str:
    """Mask anything that looks like an API key before text is shown or stored."""
    text = _KEY_PATTERN.sub("sk-***", text or "")
    return _GOOGLE_KEY_PATTERN.sub("AIza***", text)
