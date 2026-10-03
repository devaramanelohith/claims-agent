"""LLM factory. The ONLY place a chat-model client is created.

Supported providers (see PROVIDERS in config.py):
  openrouter -> ChatOpenAI pointed at OpenRouter's OpenAI-compatible endpoint
  gemini     -> ChatGoogleGenerativeAI (Google AI Studio key)
  openai     -> ChatOpenAI

SECURITY: never wrap `build_llm` (or anything that receives an api_key) in
st.cache_resource / st.cache_data / functools.lru_cache. Cached objects are shared
across every visitor of the app, which is exactly how keys leak between users.
"""
from __future__ import annotations

from typing import Any, Optional

from securecare.config import DEFAULT_PROVIDER, LLM_TIMEOUT_SECONDS, OPENROUTER_BASE_URL, PROVIDERS


def build_llm(api_key: str, model: Optional[str] = None, provider: str = DEFAULT_PROVIDER) -> Any:
    """Create a fresh, short-lived client. The key is passed explicitly, never via os.environ."""
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown LLM provider: {provider!r}")
    model = model or PROVIDERS[provider]["models"][0]

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=0,
            timeout=LLM_TIMEOUT_SECONDS,
            max_retries=1,
        )

    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=OPENROUTER_BASE_URL if provider == "openrouter" else None,
        temperature=0,
        timeout=LLM_TIMEOUT_SECONDS,
        max_retries=1,
    )
