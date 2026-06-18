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
    / "chunks_small.json"
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
    
    author_text = ""
    if chunk.get("author"):
        author_text = f"Author: {chunk['author']}\n"

    documents.append(
        Document(
            page_content=f"""
Unit {chunk['unit']}

Title: {chunk['title']}

{author_text}
Section: {chunk['section']}

{chunk['text']}
""",
            metadata={
                "unit": chunk["unit"],
                "section": chunk["section"],
                "title": chunk["title"],
                "author": chunk.get("author"), 
                "chunk_id": chunk["chunk_id"]
            }
        )
    )

print(
    f"Created {len(documents)} documents"
)

# ==================================================
# EMBEDDINGS
# ==================================================

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
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

BATCH_SIZE = 5

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
                    "Rate limit hit. Waiting 60 seconds..."
                )

                time.sleep(60)

            else:
                raise

    time.sleep(5)

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