from datasets import load_dataset
from tqdm import tqdm
from client import client

# Collection name
COLLECTION_NAME = "wine"


def combine_fields(doc):
    """Combine specific fields into a single string for embeddings."""
    return f"{doc['name']} {doc['region']} {doc['variety']} {doc['notes']}"


def create_collection():
    """Create Qdrant collection if it doesn't exist."""
    if not client.collection_exists(COLLECTION_NAME):
        print(f"Creating collection '{COLLECTION_NAME}'...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=client.get_fastembed_vector_params(),
            sparse_vectors_config=client.get_fastembed_sparse_vector_params(),
        )
        print("Collection created successfully!")
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists.")


def add_documents_to_collection():
    """Load dataset, prepare documents, and add to Qdrant collection."""
    print("Loading dataset...")
    dataset = load_dataset("alfredodeza/wine-ratings", split="test")

    print("Combining fields and preparing documents...")
    combined_texts = [combine_fields(doc) for doc in dataset]

    print("Adding documents to Qdrant collection...")
    client.add(
        collection_name=COLLECTION_NAME,
        documents=combined_texts,
        metadata=dataset,
        ids=tqdm(range(len(combined_texts))),
    )
    print("Documents added successfully!")


if __name__ == "__main__":
    print("Starting Qdrant client setup...")
    create_collection()
    add_documents_to_collection()
    print("Setup complete!")
