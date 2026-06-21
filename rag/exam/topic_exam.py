from pathlib import Path
import sys
import json

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from prompts import TOPIC_EXAM_PROMPT

# ==========================================
# PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv()

# ==========================================
# VECTOR DB
# ==========================================

VECTOR_DB_DIR = (
    PROJECT_ROOT
    / "vector_db"
)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = Chroma(
    persist_directory=str(VECTOR_DB_DIR),
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 8,
        "fetch_k": 20
    }
)

# ==========================================
# LLM
# ==========================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

def build_context(docs):

    parts = []

    for doc in docs:

        parts.append(
            doc.page_content[:2000]
        )

    return "\n\n".join(parts)

while True:

    topic = input("\nTopic: ")

    if topic.lower() in [
        "exit",
        "quit"
    ]:
        break

    docs = retriever.invoke(
        f"""
        definition
        characteristics
        principles
        importance
        advantages
        disadvantages
        {topic}
        """
    )

    context = build_context(
        docs
    )

    prompt = TOPIC_EXAM_PROMPT.format(
        topic=topic,
        context=context
    )

    response = llm.invoke(
        prompt
    )

    print()
    print("=" * 60)
    print("RAW JSON")
    print("=" * 60)

    print(
        response.content
    )