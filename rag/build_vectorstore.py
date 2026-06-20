import json
import shutil
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

from langchain_core.documents import Document

from langchain_chroma import Chroma

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings
)
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

print(
    f"Loaded {len(chunks)} chunks"
)

# ==================================================
# CREATE DOCUMENTS
# ==================================================

documents = []

for chunk in chunks:

    source = chunk.get("source", "unknown")

    # =====================================
    # TEXTBOOK CHUNKS
    # =====================================

    if source == "textbook":

        author_text = ""

        if chunk.get("author"):
            author_text = f"Author: {chunk['author']}\n"

        page_content = f"""
Source: Textbook

Unit: {chunk['unit']}

Title: {chunk['title']}

{author_text}
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

    # =====================================
    # PEDAGOGY CHUNKS
    # =====================================

    else:

        page_content = f"""
Source: {source}

Unit: {chunk['unit']}

Topic Number: {chunk['topic_number']}

Topic: {chunk['topic']}

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

    shutil.rmtree(
        VECTOR_DB_DIR
    )

# ==================================================
# BUILD CHROMA
# ==================================================

vectorstore = Chroma(
    persist_directory=str(VECTOR_DB_DIR),
    embedding_function=embeddings
)

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

    time.sleep(10)

print()

print(
    "✅ Vector database created"
)

print(
    f"📁 {VECTOR_DB_DIR}"
)

print(
    f"📚 Embedded {len(documents)} chunks"
)