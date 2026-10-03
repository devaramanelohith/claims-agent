from securecare.formatting import format_inr
from securecare.agents.llm import build_llm
from securecare.security import looks_like_api_key, looks_like_openai_key, redact_secrets


def test_key_shape_check():
    assert looks_like_openai_key("sk-" + "a" * 30)
    assert not looks_like_openai_key("hello") and not looks_like_openai_key("")
    assert looks_like_api_key("sk-or-v1-" + "a" * 30, "openrouter")
    assert not looks_like_api_key("sk-" + "a" * 30, "openrouter")
    assert looks_like_api_key("AIza" + "a" * 35, "gemini")
    assert not looks_like_api_key("sk-" + "a" * 30, "gemini")


def test_build_llm_per_provider():
    router = build_llm("sk-or-v1-" + "a" * 30, provider="openrouter")
    assert "openrouter.ai" in str(router.openai_api_base) and router.model_name == "openai/gpt-4o-mini"
    gemini = build_llm("AIza" + "a" * 35, provider="gemini")
    assert type(gemini).__name__ == "ChatGoogleGenerativeAI" and "gemini" in gemini.model


def test_redaction():
    assert redact_secrets("bad key sk-proj-abcdef123456789 used") == "bad key sk-*** used"
    assert redact_secrets("key AIzaSyA1b2C3d4E5f6G7h8 bad") == "key AIza*** bad"


def test_inr_format():
    assert format_inr(127500) == "₹1,27,500"
    assert format_inr(999) == "₹999"
    assert format_inr(10000000) == "₹1,00,00,000"
