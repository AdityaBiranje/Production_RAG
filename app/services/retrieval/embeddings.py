import time 
import logfire 
from langchain_google_genai import  GoogleGenerativeAIEmbeddings
from app.config import settings

BATCH_SIZE = 50
_GEMINI_DIM = 3072
_FALLBACK_DIM = 768 #all-mpnet-base-v2

_active_model = None
_model_type :str |None = None #gemini or fallback

def _probe_gemini():
    """try on a small batch to see if the model is available.returns models or none """


def _load_fallback():
    """load the fallback model """
    return

def _init():
    return

def get_embeddings_dim() -> int:
    """returns the dimension of the active model , call after _init()"""
    return

def _embed_batch(batch: list[str]) -> list[list[float]]:
    """embeds a batch of text using the active model"""
    return

def embed_query(query:str)-> list[float]:
    """embeds a single query using the active model"""
    return


def embed_texts(texts: list[str]) -> list[list[float]]:
    """embeds a list of texts using the active model"""
    _init()


