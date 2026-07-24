import logfire
import time
from flashrank import Ranker, RerankRequest

# Lazy initialization - Ranker is loaded on first use to ensure logfire.configure() has run
_ranker = None

def _get_ranker() -> Ranker:
    """
    Initializes the FlashRank engine lazily. 
    FlashRank uses a local ONNX model (ms-marco-MiniLM-L-6-v2) for ultra-fast reranking.
    """
    global _ranker
    if _ranker is None:
        logfire.info("🧠 Initializing FlashRank Model (TinyBERT) locally...")
        try :
            #we use a specific cache directory to avoid permission issues in production
            _ranker = Ranker(cache_dir= "/tmp/flashrank")
        except Exception:
            _ranker = Ranker()

    return _ranker
