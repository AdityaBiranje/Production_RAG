import logfire
from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.config import settings
from app.services.retrieval.embeddings import embed_query

#initialize qdrant client
client = QdrantClient(
    url = settings.QDRANT_URL,
    api_key= settings.QDRANT_API_KEY
)

