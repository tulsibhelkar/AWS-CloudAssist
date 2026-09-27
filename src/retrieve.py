from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# ---------- CONFIGURATION ----------

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "data" / "chroma_db"

COLLECTION_NAME = "aws_cloudassist"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# ---------- LOAD MODEL AND DATABASE ----------

print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

print("Connecting to ChromaDB...")
client = chromadb.PersistentClient(path=str(DB_DIR))

try:
    collection = client.get_collection(name=COLLECTION_NAME)
except ValueError:
    raise SystemExit(
        "ERROR: Collection not found. Run create_embeddings.py first."
    )

print(f"Database connected. Total chunks: {collection.count()}")


# ---------- RETRIEVAL FUNCTION ----------

def retrieve_documents(question, top_k=3):
    """Retrieve the most relevant AWS documentation chunks."""

    if not question.strip():
        print("Please enter a valid question.")
        return []

    if collection.count() == 0:
        print("The vector database is empty.")
        return []

    # Convert the user's question into an embedding.
    question_embedding = model.encode(
        question,
        normalize_embeddings=True,
    ).tolist()

    # Search for similar document chunks.
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    retrieved = []

    for index, chunk_id in enumerate(results["ids"][0]):
        retrieved.append(
            {
                "chunk_id": chunk_id,
                "content": results["documents"][0][index],
                "metadata": results["metadatas"][0][index],
                "distance": results["distances"][0][index],
            }
        )

    return retrieved


# ---------- MAIN PROGRAM ----------

def main():
    print("\nAWS CLOUDASSIST - RETRIEVAL TEST")
    print("-" * 50)

    while True:
        question = input(
            "\nEnter your AWS question (or type exit): "
        ).strip()

        if question.lower() in {"exit", "quit"}:
            print("Retrieval test finished.")
            break

        results = retrieve_documents(question)

        if not results:
            continue

        for index, result in enumerate(results, start=1):
            metadata = result["metadata"]

            print(f"\n{'=' * 50}")
            print(f"RESULT {index}")
            print(f"{'=' * 50}")

            print(f"Service: {metadata['service']}")
            print(f"Title: {metadata['title']}")
            print(f"Chunk ID: {result['chunk_id']}")
            print(f"Cosine distance: {result['distance']:.4f}")
            print(f"Source: {metadata['source_url']}")

            print("\nRetrieved content:")
            print(result["content"][:800])

        print("\n" + "-" * 50)


if __name__ == "__main__":
    main()