import json
import shutil
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# ==================================================
# PATHS
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv()

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "all_chunks.json"
)

VECTOR_DB_DIR = (
    PROJECT_ROOT
    / "vector_db"
)

# ==================================================
# LOAD CHUNKS
# ==================================================

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:
    chunks = json.load(f)

print()
print(f"Loaded {len(chunks)} chunks")

# ==================================================
# CREATE DOCUMENTS
# ==================================================

documents = []

for chunk in chunks:

    source = chunk.get(
        "source",
        "unknown"
    )

    # ==================================================
    # TEXTBOOK
    # ==================================================

    if source == "textbook":

        author = chunk.get(
            "author",
            ""
        )

        page_content = f"""
Source: Textbook

Unit: {chunk['unit']}

Title: {chunk['title']}

Author: {author}
Section: {chunk['section']}

{chunk['text']}
"""

        metadata = {
            "source": source,
            "unit": chunk["unit"],
            "title": chunk["title"],
            "section": chunk["section"],
            "author": chunk.get("author"),
            "chunk_id": chunk["chunk_id"]
        }

    # ==================================================
    # PEDAGOGY 1
    # ==================================================

    elif source == "pedagogy_1":

        page_content = f"""
Source: Pedagogy 1

Unit: {chunk['unit']}

Topic Number: {chunk['topic_number']}

Topic: {chunk['topic']}

Keywords:
{chunk['topic']}

{chunk['text']}
"""

        metadata = {
            "source": source,
            "unit": chunk["unit"],
            "topic_number": chunk["topic_number"],
            "topic": chunk["topic"],
            "page_start": chunk.get("page_start"),
            "page_end": chunk.get("page_end"),
            "chunk_id": chunk["chunk_id"]
        }

    # ==================================================
    # PEDAGOGY 2
    # ==================================================

    elif source == "pedagogy_2":

        page_content = f"""
Source: Pedagogy 2

Block: {chunk['block']}
Unit: {chunk['unit']}
Global Unit: {chunk['global_unit']}

Title: {chunk['title']}

Keywords:
{chunk['title']}

{chunk['text']}
"""
        

        metadata = {
            "source": source,
            "block": chunk["block"],
            "unit": chunk["unit"],
            "global_unit": chunk["global_unit"],
            "title": chunk["title"],
            "page_start": chunk["page_start"],
            "page_end": chunk["page_end"],
            "chunk_id": chunk["chunk_id"]
        }

    else:
        continue

    documents.append(
        Document(
            page_content=page_content,
            metadata=metadata
        )
    )

print(
    f"Created {len(documents)} documents"
)

# ==================================================
# EMBEDDINGS
# ==================================================

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# ==================================================
# DELETE OLD VECTOR DB
# ==================================================

if VECTOR_DB_DIR.exists():

    print()
    print("Deleting old vector DB...")

    shutil.rmtree(
        VECTOR_DB_DIR
    )

# ==================================================
# CREATE CHROMA
# ==================================================

vectorstore = Chroma(
    persist_directory=str(VECTOR_DB_DIR),
    embedding_function=embeddings
)

# ==================================================
# ADD DOCUMENTS
# ==================================================

BATCH_SIZE = 100

for i in range(0, len(documents), BATCH_SIZE):

    batch = documents[i:i+BATCH_SIZE]

    while True:

        try:

            vectorstore.add_documents(
                batch
            )

            print(
                f"Done batch {(i // BATCH_SIZE) + 1}"
            )

            break

        except Exception as e:

            if "RESOURCE_EXHAUSTED" in str(e):

                print(
                    "Rate limit hit. Waiting 10 seconds..."
                )

                time.sleep(10)

            else:
                raise

    time.sleep(1)

# ==================================================
# SUMMARY
# ==================================================

print()
print("✅ Vector database created")
print(f"📁 {VECTOR_DB_DIR}")
print(f"📚 Embedded {len(documents)} chunks")

print()
print("Metadata examples")
print("-" * 50)
print(documents[0].metadata)
print(documents[-1].metadata)