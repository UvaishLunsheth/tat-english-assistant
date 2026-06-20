from pathlib import Path
import sys
import re
import json
import time

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate

# ==================================================
# PROJECT PATH
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv()

# ==================================================
# VECTOR DB
# ==================================================

# ==================================================
# VECTOR DB
# ==================================================

VECTOR_DB_DIR = (
    PROJECT_ROOT
    / "vector_db"
)

# Replace the Gemini embeddings with OpenAI
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = Chroma(
    persist_directory=str(VECTOR_DB_DIR),
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 4
    }
)

# ==================================================
# LLM
# ==================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# ==================================================
# PROMPT
# ==================================================

PROMPT = PromptTemplate.from_template("""
You are an expert English Education Assistant.

The retrieved context may come from:

1. Gujarat Std 12 English Textbook
2. Pedagogy of English Volume 1
3. Pedagogy of English Volume 2

Answer ONLY from the retrieved context.

Do NOT use outside knowledge.

If the answer is not present in the context reply exactly:

I could not find the answer in the retrieved sources.

Context:
{context}

Question:
{question}

Provide:

1. Direct answer
2. Brief explanation
3. Source reference

Answer:
""")

# ==================================================
# DIRECT TITLE LOOKUP
# ==================================================

def get_title_from_unit(question):
    match = re.search(
        r"unit\s+(\d+)\s+read\s+(\d+)\s+title",
        question.lower()
    )

    if not match:
        return None

    unit_no = int(match.group(1))
    read_no = int(match.group(2))

    file_path = (
        PROJECT_ROOT
        / "data"
        / "units"
        / f"unit_{unit_no}.json"
    )

    if not file_path.exists():
        return None

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:
        unit_data = json.load(f)

    read_key = f"read_{read_no}"

    if read_key not in unit_data:
        return None

    return unit_data[read_key]["title"]

# ==================================================
# SOURCE FORMATTER
# ==================================================

SECTION_NAMES = {
    "read_1_content": "Read 1",
    "read_1_glossary": "Glossary",
    "read_1_comprehension": "Comprehension",
    "read_2_content": "Read 2",
    "read_2_glossary": "Glossary",
    "read_2_comprehension": "Comprehension",
    "vocabulary": "Vocabulary",
    "functions": "Functions",
    "writing": "Writing",
    "activities": "Activities",
    "project": "Project"
}

def build_source(doc):
    source_type = doc.metadata.get(
        "source",
        "textbook"
    )

    # ---------------------------
    # TEXTBOOK
    # ---------------------------

    if source_type == "textbook":
        author = (
            doc.metadata.get("author")
            or "No author name available"
        )

        section = SECTION_NAMES.get(
            doc.metadata.get("section"),
            doc.metadata.get("section")
        )

        return (
            f"TEXTBOOK | "
            f"Unit {doc.metadata['unit']} | "
            f"{doc.metadata['title']} | "
            f"{author} | "
            f"{section}"
        )

    # ---------------------------
    # PEDAGOGY
    # ---------------------------

    return (
        f"{source_type.upper()} | "
        f"Unit {doc.metadata['unit']} | "
        f"{doc.metadata['topic_number']} | "
        f"{doc.metadata['topic']}"
    )

# ==================================================
# CONTEXT BUILDER
# ==================================================

def build_context(docs):
    context_parts = []

    for doc in docs:
        source_type = doc.metadata.get(
            "source",
            "textbook"
        )

        # -----------------------
        # TEXTBOOK
        # -----------------------

        if source_type == "textbook":
            author = (
                doc.metadata.get("author")
                or "No author name available"
            )

            context_parts.append(
                f"""
SOURCE: TEXTBOOK

Unit: {doc.metadata['unit']}
Title: {doc.metadata['title']}
Author: {author}
Section: {doc.metadata['section']}

{doc.page_content}
"""
            )

        # -----------------------
        # PEDAGOGY
        # -----------------------

        else:
            context_parts.append(
                f"""
SOURCE: {source_type.upper()}

Unit: {doc.metadata['unit']}
Topic Number: {doc.metadata['topic_number']}
Topic: {doc.metadata['topic']}

{doc.page_content}
"""
            )

    return "\n\n".join(context_parts)

# ==================================================
# MAIN LOOP
# ==================================================

while True:
    question = input("\nQuestion: ")

    if question.lower() in [
        "exit",
        "quit"
    ]:
        break

    # =============================================
    # DIRECT UNIT TITLE LOOKUP
    # =============================================

    title = get_title_from_unit(question)

    if title:
        print("\nAnswer:\n")
        print(
            f"1. Direct answer: {title}\n\n"
            f"2. Brief explanation: "
            f"This is the lesson title stored in the unit metadata.\n\n"
            f"3. Source reference: Unit JSON file"
        )
        continue

    # =============================================
    # RETRIEVE
    # =============================================

    docs = retriever.invoke(question)


    # --- TEMPORARY DEBUG BLOCK ---
    for i, doc in enumerate(docs, start=1):
        print("\n")
        print("="*80)
        print(f"DOC {i}")
        print("="*80)
        print(doc.page_content[:1000])
        print("METADATA:", doc.metadata) 

    # =============================================
    # SOURCES
    # =============================================

    sources = []

    for doc in docs:
        source = build_source(doc)
        if source not in sources:
            sources.append(source)

    # =============================================
    # CONTEXT
    # =============================================

    context = build_context(docs)

    prompt = PROMPT.format(
        context=context,
        question=question
    )

    response = llm.invoke(prompt)

    # =============================================
    # OUTPUT
    # =============================================

    print("\nAnswer:\n")
    print(response.content)

    print("\n" + "=" * 60)
    print("SOURCES")
    print("=" * 60)

    for source in sources:
        print(f"- {source}")

    print()
    time.sleep(2)