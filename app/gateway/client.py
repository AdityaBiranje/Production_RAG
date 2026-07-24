import logfire
from portkey_ai import Portkey, createHeaders , PORTKEY_GATEWAY_URL
from langchain_openai import ChatOpenAI

from app.config import settings

# Production gateway config:
#   - Fallback: primary @rag/llama-3.3-70b-versatile → @brag/llama-3.1-8b-instant on failure
#   - Cache: semantic mode (requires Portkey Enterprise — silently falls back to simple on free/starter)
#   - Retry: 2 attempts on rate limit / server error before triggering the fallback target

