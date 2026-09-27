import json
import re
from pathlib import Path


# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(text):
    """Normalize whitespace while preserving paragraph boundaries."""

    # Normalize Windows and older Mac line endings.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove extra spaces and tabs within each line.
    lines = []

    for line in text.split("\n"):
        line = re.sub(r"[ \t]+", " ", line).strip()

        if line:
            lines.append(line)

    # Keep separate lines to avoid merging technical instructions.
    cleaned = "\n".join(lines)

    return cleaned


def process_documents():
    files = sorted(RAW_DIR.glob("*.json"))

    if not files:
        print("No JSON files found in data/raw.")
        return

    print("AWS CLOUDASSIST - DATA CLEANING")
    print("-" * 40)

    successful = 0

    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                document = json.load(file)

            original_content = document.get("content", "")

            if not isinstance(original_content, str):
                print(f"Skipped {file_path.name}: invalid content.")
                continue

            cleaned_content = clean_text(original_content)

            if not cleaned_content:
                print(f"Skipped {file_path.name}: empty content.")
                continue

            # Preserve existing source metadata.
            document["content"] = cleaned_content

            output_path = PROCESSED_DIR / file_path.name

            with open(output_path, "w", encoding="utf-8") as file:
                json.dump(
                    document,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

            print(f"\nFile: {file_path.name}")
            print(f"Original characters: {len(original_content)}")
            print(f"Cleaned characters:  {len(cleaned_content)}")
            print(f"Saved: {output_path}")

            successful += 1

        except (OSError, json.JSONDecodeError) as error:
            print(f"Error processing {file_path.name}: {error}")

    print("\n" + "-" * 40)
    print(f"Successfully cleaned: {successful}/{len(files)}")


if __name__ == "__main__":
    process_documents()