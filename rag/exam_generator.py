from pathlib import Path
import sys

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

# ==========================================
# PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

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
        "k": 10,
        "fetch_k": 25
    }
)

# ==========================================
# LLM
# ==========================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
)

def build_context(docs):

    parts = []

    for doc in docs:

        parts.append(
            doc.page_content[:2000]
        )

    return "\n\n".join(parts)


QUESTION_PROMPT = """
You are a Gujarat TAT English paper setter.

Topic:
{topic}

Context:
{context}

IMPORTANT:

Generate questions directly about the requested topic.

Do not generate questions from unrelated examples,
assessments, activities, references, exercises,
summaries or surrounding educational discussion.

Focus on:

- definition
- meaning
- concept
- characteristics
- principles
- objectives
- importance
- merits
- demerits
- advantages
- disadvantages
- classifications
- types
- stages
- domains
- procedures

Generate:

1 MCQ
1 Fill in the Blank
1 True/False
1 Match the Following
1 Short Answer
1 Medium Answer
1 Long Answer

Do not provide answers.
"""


while True:

    topic = input(
        "\nTopic: "
    )

    if topic.lower() in [
        "exit",
        "quit"
    ]:
        break

    # ==========================================
    # Expand the database search query!
    # ==========================================
    search_query = (
        f"Definition, characteristics, principles, "
        f"merits, demerits, advantages, disadvantages, "
        f"importance of {topic}"
    )

    # Pass the expanded search query to the retriever, NOT just the topic
    docs = retriever.invoke(
        search_query
    )

    context = build_context(
        docs
    )

    prompt = QUESTION_PROMPT.format(
        topic=topic,
        context=context
    )

    response = llm.invoke(
        prompt
    )

    print()
    print("=" * 60)
    print("GENERATED QUESTIONS")
    print("=" * 60)
    print()

    print(
        response.content
    )