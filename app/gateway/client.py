import logfire
from portkey_ai import Portkey, createHeaders , PORTKEY_GATEWAY_URL
from langchain_openai import ChatOpenAI

from app.config import settings

# Production gateway config:
#   - Fallback: primary @rag/llama-3.3-70b-versatile → @brag/llama-3.1-8b-instant on failure
#   - Cache: semantic mode (requires Portkey Enterprise — silently falls back to simple on free/starter)
#   - Retry: 2 attempts on rate limit / server error before triggering the fallback target

GATEWAY_CONFIG= {
    "startegy": {"mode": "fallback"},
    "cache": {"mode": "simple"},
    "retry":{
        "attempts":2,
        "on_status_codes": [429,503]
    },
    "targets":[
        {"override_params": {"model": f"@{settings.QROQ_SLUG}/llama-3.3-70b-versatile"}},
        {"override_params": {"model": f"@{settings.QROQ_SLUG_2}/llama-3.1-8b-instant"}},
    ]
}

portkey_client = Portkey(
    api_key= settings.PORTKEY_API_KEY,
    config = GATEWAY_CONFIG
)

