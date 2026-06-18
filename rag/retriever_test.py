from pathlib import Path
import sys

from dotenv import load_dotenv

from langchain_chroma import Chroma

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv()

VECTOR_DB_DIR = (
    PROJECT_ROOT
    / "vector_db"
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

vectorstore = Chroma(

    persist_directory=str(
        VECTOR_DB_DIR
    ),

    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(

    search_type="similarity",

    search_kwargs={
        "k": 5
    }
)

query = "What is LOWESTEEM.EXE?"

docs = retriever.invoke(
    query
)

print()

print(
    "=" * 60
)

print(
    f"QUESTION: {query}"
)

print(
    "=" * 60
)

for i, doc in enumerate(docs, start=1):

    print()

    print(
        f"[RESULT {i}]"
    )

    print(
        doc.metadata
    )

    print()

    print(
        doc.page_content[:500]
    )

    print()