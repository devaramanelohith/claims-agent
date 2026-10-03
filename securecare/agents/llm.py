"""LLM factory. The ONLY place a ChatOpenAI client is created.

SECURITY: never wrap `build_llm` (or anything that receives an api_key) in
st.cache_resource / st.cache_data / functools.lru_cache. Cached objects are shared
across every visitor of the app, which is exactly how keys leak between users.
"""
from __future__ import annotations

from langchain_openai import ChatOpenAI

from securecare.config import DEFAULT_MODEL, LLM_TIMEOUT_SECONDS


def build_llm(api_key: str, model: str = DEFAULT_MODEL) -> ChatOpenAI:
    """Create a fresh, short-lived client. The key is passed explicitly, never via os.environ."""
    return ChatOpenAI(
        model=model,
        api_key=api_key,
        temperature=0,
        timeout=LLM_TIMEOUT_SECONDS,
        max_retries=1,
    )
