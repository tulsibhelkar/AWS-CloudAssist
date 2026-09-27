import json
from pathlib import Path

import chromadb
from chromadb.errors import NotFoundError
from sentence_transformers import SentenceTransformer


# ==========================================
# 1. CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

CHUNKS_FILE = BASE_DIR / "data" / "processed" / "chunks.json"

DB_DIR = BASE_DIR / "data" / "chroma_db"

COLLECTION_NAME = "aws_cloudassist"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# ==========================================
# 2. LOAD AND VALIDATE CHUNKS
# ==========================================

def load_chunks():

    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            f"Chunks file not found: {CHUNKS_FILE}"
        )

    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    if not isinstance(chunks, list) or not chunks:
        raise ValueError("chunks.json is empty or invalid.")

    required_fields = [
        "chunk_id",
        "document_id",
        "service",
        "title",
        "source_url",
        "content",
    ]

    for index, chunk in enumerate(chunks):

        if not isinstance(chunk, dict):
            raise ValueError(
                f"Chunk {index} is not a dictionary."
            )

        for field in required_fields:

            if field not in chunk:
                raise ValueError(
                    f"Chunk {index} is missing: {field}"
                )

            if not isinstance(chunk[field], str):
                raise ValueError(
                    f"Chunk {index} has an invalid {field}."
                )

            if not chunk[field].strip():
                raise ValueError(
                    f"Chunk {index} has an empty {field}."
                )

    chunk_ids = [
        chunk["chunk_id"]
        for chunk in chunks
    ]

    if len(chunk_ids) != len(set(chunk_ids)):
        raise ValueError("Duplicate chunk IDs detected.")

    return chunks


# ==========================================
# 3. GENERATE EMBEDDINGS
# ==========================================

def generate_embeddings(chunks):

    print("\nLoading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    print("Generating embeddings...")

    embeddings = model.encode(
        texts,
        batch_size=16,
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    print(f"Embedding shape: {embeddings.shape}")

    return embeddings


# ==========================================
# 4. CREATE CHROMADB COLLECTION
# ==========================================

def create_database(chunks, embeddings):

    DB_DIR.mkdir(parents=True, exist_ok=True)

    print("\nConnecting to ChromaDB...")

    client = chromadb.PersistentClient(
        path=str(DB_DIR)
    )

    # Replace only the project's existing collection.
    # This prevents duplicate or outdated chunks on reruns.
    #
    # IMPORTANT: Any existing data in this named collection
    # will be deleted. Other collections are unaffected.

    try:
        client.delete_collection(
            name=COLLECTION_NAME
        )

        print("Existing collection deleted.")

    except NotFoundError:

        print(
            "No existing collection found. "
            "Creating a new collection."
        )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "hnsw:space": "cosine"
        },
    )

    ids = [
        chunk["chunk_id"]
        for chunk in chunks
    ]

    documents = [
        chunk["content"]
        for chunk in chunks
    ]

    metadatas = []

    for chunk in chunks:

        metadata = {
            "document_id": chunk["document_id"],
            "service": chunk["service"],
            "title": chunk["title"],
            "source_url": chunk["source_url"],
            "chunk_index": int(
                chunk.get("chunk_index", 0)
            ),
        }

        metadatas.append(metadata)

    print("\nStoring embeddings in ChromaDB...")

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
    )

    return collection


# ==========================================
# 5. MAIN FUNCTION
# ==========================================

def main():

    print("\nAWS CLOUDASSIST - EMBEDDING PIPELINE")
    print("-" * 45)

    try:

        # Load the prepared dataset.
        chunks = load_chunks()

        print(f"Loaded chunks: {len(chunks)}")

        # Generate numerical embeddings.
        embeddings = generate_embeddings(chunks)

        # Create the vector database.
        collection = create_database(
            chunks,
            embeddings
        )

        # Verify storage.
        stored_count = collection.count()

        print("\n" + "-" * 45)

        print(f"Stored chunks: {stored_count}")

        print(f"Collection: {COLLECTION_NAME}")

        print(f"Database folder: {DB_DIR}")

        if stored_count == len(chunks):

            print(
                "\nVECTOR DATABASE CREATED SUCCESSFULLY"
            )

        else:

            print(
                "\nWARNING: Stored chunk count does not match."
            )

    except Exception as error:

        print(f"\nERROR: {error}")

        raise


# ==========================================
# 6. PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()