import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "chunks.json"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def create_chunks():

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    all_chunks = []

    # Read only the three cleaned source documents.
    input_files = sorted(
        file for file in PROCESSED_DIR.glob("*.json")
        if file.name != OUTPUT_FILE.name
    )

    if not input_files:
        print("No cleaned JSON documents found.")
        return

    print("\nAWS CLOUDASSIST - TEXT CHUNKING")
    print("-" * 45)

    for file_path in input_files:

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                document = json.load(file)

            content = document.get("content", "")

            if not isinstance(content, str) or not content.strip():
                print(f"Skipping invalid content: {file_path.name}")
                continue

            chunks = splitter.split_text(content)

            for index, chunk_text in enumerate(chunks):

                chunk = {
                    "chunk_id": f"{document['document_id']}_chunk_{index + 1:03d}",
                    "document_id": document["document_id"],
                    "service": document["service"],
                    "title": document["title"],
                    "source_url": document["source_url"],
                    "chunk_index": index,
                    "content": chunk_text,
                }

                all_chunks.append(chunk)

            print(f"{file_path.name}: {len(chunks)} chunks")

        except (OSError, json.JSONDecodeError, KeyError) as error:
            print(f"Error processing {file_path.name}: {error}")

    if not all_chunks:
        print("No valid chunks created.")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            all_chunks,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print("-" * 45)
    print(f"Total chunks created: {len(all_chunks)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    create_chunks()