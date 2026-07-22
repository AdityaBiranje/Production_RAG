import os
import sys
import uuid
import json
import logfire

from qdrant_client import QdrantClient
from qdrant_client.http import models

from app.config import settings
from app.services.retrieval.embeddings import embed_texts, get_embedding_dim
from app.ingestion.loaders.pdf import parse_pdf
from app.ingestion.loaders.html import parse_html
from app.ingestion.loaders.text import parse_text
from app.ingestion.loaders.office import parse_office
from app.ingestion.chunking.splitter import chunk_text

logfire.configure(service_name="enterprise-ingestion-service")

# Local folder where parsed + chunked JSON metadata is saved (replaces GCS processed bucket)
PROCESSED_DATA_DIR = "processed_data"

# Initialize Qdrant Client
qdrant_client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
)

def save_processed_locally(data: dict, source_type: str, file_name: str) -> str:
    """Save parsed chunk metadata as JSON in processed_data/<source_type>/."""
    folder = os.path.join(PROCESSED_DATA_DIR, source_type)
    os.makedirs(folder,exist_ok = True)
    dest = os.path.join(folder,f"{file_name}.json")
    with open(dest, "w",encoding= "utf-8") as f:
        json.dump(data,f, ensure_ascii=False, indent=2)
    return dest

def process_file(file_path: str, source_type: str, file_name: str):
    """Parse → chunk → save locally → embed → index in Qdrant."""
    with logfire.span("Processing File", file = file_name, source = source_type):
        try:
             # Step 1: Parse the file based on its type
            ext =  file_name.lower().rsplit(".", 1)[-1]
            if ext == "pdf":
                full_text = parse_pdf(file_path)
            elif ext in ("html","htm"):
                full_text = parse_html(file_path)
            elif ext == "txt":
                full_text = parse_text(file_path)
            elif ext in ("docx","pptx","doc"):
                #from app.ingestion.loaders.office import parse_office
                full_text = parse_office(file_path)
            else:
                logfire.warning(f"Skipping unsupported file type: {file_name}")
                return
            
            if not full_text or not full_text.strip():
                logfire.warning(f"No text extracted from {file_name} - Skipping.")
                return

            # Step 2: Chunk the text
            chunks = chunk_text(full_text)
            if not chunks:
                return
            
            #step 3 : save processed metadata locally
            processed_data = {
                "filename": file_name,
                "source_type": source_type,
                "chunks": chunks,
            }
            local_path = save_processed_locally(processed_data, source_type, file_name)
            logfire.info(f"✅ Processed data saved locally at {local_path}")

            # Step 4: Embed and index in Qdrant
            with logfire.span("vectorizing & indexing"):
                embeddings = embed_texts(chunks)
                points = [
                    models.pointstruct(
                        id = str(uuid.uuid4()),
                        vector = vector,
                        payload ={
                            "text":chunk,
                            "source": file_name,
                            "source_type": source_type,
                        },
                    )
                    for chunk, vector in zip(chunks,embeddings)
                ]

                qdrant_client.upsert(
                    collection_name = settings.QDRANT_COLLECTION,
                )

                logfire.info(f"Indexed {len(points)} points to qdrant from {file_name}.")

        except Exception as e:
            logfire.error(f"failed to process {file_name}: {e}")
        

