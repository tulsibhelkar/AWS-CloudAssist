import json
import time
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup


# ---------- CONFIGURATION ----------

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = "AWS-CloudAssist-StudentProject/1.0"
REQUEST_DELAY = 2

SOURCES = [
    {
        "id": "ec2_001",
        "service": "EC2",
        "url": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html",
    },
    {
        "id": "s3_001",
        "service": "S3",
        "url": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html",
    },
    {
        "id": "iam_001",
        "service": "IAM",
        "url": "https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html",
    },
]


# ---------- ROBOTS.TXT CHECK ----------

def is_allowed(url):
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    try:
        response = requests.get(
            robots_url,
            headers={"User-Agent": USER_AGENT},
            timeout=15,
        )
        response.raise_for_status()

        robots = RobotFileParser()
        robots.parse(response.text.splitlines())

        return robots.can_fetch(USER_AGENT, url)

    except requests.RequestException as error:
        print(f"Robots check failed: {error}")
        return False


# ---------- CONTENT EXTRACTION ----------

def extract_content(soup):
    """Find the documentation body using common AWS HTML containers."""

    selectors = [
        "main",
        "article",
        "#main-col-body",
        "#main-content",
        "#main-col",
        ".awsdocs-container",
        ".awsdocs-content",
        "[role='main']",
    ]

    main_content = None

    for selector in selectors:
        main_content = soup.select_one(selector)

        if main_content is not None:
            print(f"Content selector found: {selector}")
            break

    if main_content is None:
        print("Could not identify the documentation container.")
        print(
            "Page title:",
            soup.title.get_text(" ", strip=True)
            if soup.title else "Missing"
        )

        print(
            "Available IDs:",
            [tag.get("id") for tag in soup.find_all(id=True)[:30]]
        )

        return None

    # Remove irrelevant elements inside the selected content.
    for tag in main_content.select(
        "script, style, nav, footer, noscript, "
        ".awsdocs-page-header, .awsdocs-page-footer"
    ):
        tag.decompose()

    content = main_content.get_text(
        separator="\n",
        strip=True,
    )

    # Avoid saving empty or nearly empty pages.
    if len(content) < 100:
        print("Extracted content is too short.")
        return None

    return content


# ---------- DOCUMENT COLLECTION ----------

def collect_document(source):
    url = source["url"]

    if not is_allowed(url):
        print(f"Skipped: collection not permitted or not verified: {url}")
        return None

    try:
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=30,
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        title = (
            soup.title.get_text(" ", strip=True)
            if soup.title
            else "Untitled"
        )

        content = extract_content(soup)

        if content is None:
            print(f"No usable content found: {url}")
            return None

        return {
            "document_id": source["id"],
            "service": source["service"],
            "title": title,
            "source_url": response.url,
            "source_type": "official_documentation",
            "collected_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "content": content,
        }

    except requests.RequestException as error:
        print(f"Collection failed for {url}: {error}")
        return None


# ---------- MAIN PROGRAM ----------

def main():
    print("\nAWS CLOUDASSIST DATA COLLECTION")
    print("-" * 45)

    successful = 0

    for source in SOURCES:
        print(f"\nCollecting {source['service']}...")

        document = collect_document(source)

        if document is not None:
            output_file = OUTPUT_DIR / f"{source['id']}.json"

            with open(
                output_file,
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    document,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

            print(f"Saved: {output_file.name}")
            print(f"Characters: {len(document['content'])}")

            successful += 1

        time.sleep(REQUEST_DELAY)

    print("\n" + "-" * 45)
    print(f"Documents collected: {successful}/{len(SOURCES)}")


if __name__ == "__main__":
    main()