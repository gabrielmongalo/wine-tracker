from functools import lru_cache
import os


from qdrant_client import QdrantClient

# Ensure API Key is set
api_key = os.environ.get("QDRANT_API_KEY")
qdrant_url = os.environ.get("QDRANT_URL")


@lru_cache(maxsize=1)
def get_client() -> QdrantClient:
    """
    Lazily initialize and cache the Qdrant client.
    Ensures models are set only once and the same instance is reused.
    """
    # Get API key from environment variables
    api_key = os.getenv("QDRANT_API_KEY")
    if not api_key:
        # If no api key it will store the data in memory
        client = QdrantClient(":memory:")
    else:
        # Initialize Qdrant client with designidated cluster
        client = QdrantClient(
            url=qdrant_url,
            api_key=api_key,
        )

    # Set dense and sparse models
    client.set_model("sentence-transformers/all-MiniLM-L6-v2")
    client.set_sparse_model("Qdrant/bm25")

    return client
