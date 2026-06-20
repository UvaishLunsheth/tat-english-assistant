from pathlib import Path
import sys

from dotenv import load_dotenv

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

VECTOR_DB_DIR = (
    PROJECT_ROOT
    / "vector_db"
)

# ==================================================
# EMBEDDINGS
# ==================================================

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# ==================================================
# VECTOR STORE
# ==================================================

vectorstore = Chroma(
    persist_directory=str(VECTOR_DB_DIR),
    embedding_function=embeddings
)

# ==================================================
# RETRIEVER
# ==================================================

def get_retriever():

    return vectorstore.as_retriever(

        search_type="mmr",

        search_kwargs={
            "k": 8,
            "fetch_k": 30,
            "lambda_mult": 0.7
        }
    )