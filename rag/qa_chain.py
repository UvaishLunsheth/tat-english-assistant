from pathlib import Path
import sys
import time
import re
import json

from dotenv import load_dotenv

from langchain_chroma import Chroma

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_openai import ChatOpenAI

#  NEW CORRECT WAY
from langchain_core.prompts import PromptTemplate

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv()

# ======================================
# VECTOR DB
# ======================================

VECTOR_DB_DIR = (
    PROJECT_ROOT
    / "vector_db"
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

vectorstore = Chroma(
    persist_directory=str(VECTOR_DB_DIR),
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 5
    }
)

# ======================================
# LLM
# ======================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0
)

# ======================================
# PROMPT
# ======================================

PROMPT = PromptTemplate.from_template("""
You are an expert Gujarat Std 12 English teacher.

Answer ONLY from the retrieved context.

Do not use outside knowledge.

If the answer is not clearly present in the context, reply exactly:

I could not find the answer in the textbook.

When the question asks about:
- author
- title
- unit
- lesson name

use the metadata provided in the context.

Context:
{context}

Question:
{question}

Provide:

1. Direct answer
2. Brief explanation
3. Reference to lesson

Answer:
""")


def get_title_from_unit(question):
    match = re.search(r"unit\s+(\d+)\s+read\s+(\d+)\s+title", question.lower())
    if not match:
        return None
        
    unit_no = int(match.group(1))
    read_no = int(match.group(2))
    
    file_path = PROJECT_ROOT / "data" / "units" / f"unit_{unit_no}.json"
    
    if not file_path.exists():
        return None
        
    with open(file_path, "r", encoding="utf-8") as f:
        unit = json.load(f)
        
    read_key = f"read_{read_no}"
    if read_key not in unit:
        return None
        
    return unit[read_key]["title"]
# ======================================
# QA LOOP
# ======================================

while True:

    question = input("\nQuestion: ")

    if question.lower() in [
        "exit",
        "quit"
    ]:
        break

    # --- ADD THE NEW BLOCK HERE ---
    title_answer = get_title_from_unit(question)
    
    if title_answer:
        # Extract unit/read numbers again just for the print statement
        match = re.search(r"unit\s+(\d+)\s+read\s+(\d+)", question.lower())
        u_no = match.group(1) if match else "X"
        r_no = match.group(2) if match else "Y"
        
        print("\nAnswer:\n")
        print(f"1. Direct answer: {title_answer}\n"
              f"2. Brief explanation: This is the title of Read {r_no} in Unit {u_no}.\n"
              f"3. Reference to lesson: Unit {u_no}")
        print("\n" + "=" * 60)
        print("SOURCES")
        print("=" * 60)
        print(f"- Direct Metadata Lookup | Unit {u_no} JSON")
        
        # Skip the RAG retrieval and go to the next question
        continue 
    # -------------------------------


    docs = retriever.invoke(
        question
    )
    


    match = re.search(
        r"unit\s+(\d+)\s+read\s+(\d+)\s+title",
        question.lower()
    )

    if match:
        unit_no = int(match.group(1))
        read_no = int(match.group(2))

        # Load unit JSON directly
        pass # <-- Added this so the 'if' block doesn't throw an error while empty

    # --------------------------
    # SOURCES
    # --------------------------

    sources = []

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

    for doc in docs:

        section = SECTION_NAMES.get(
            doc.metadata["section"],
            doc.metadata["section"]
        )

        author = doc.metadata.get("author")
        if not author:
            author = "No author name available"

        source = (
            f"Unit {doc.metadata['unit']} | "
            f"{doc.metadata['title']} | "
            f"{author} | "
            f"{section}"
        )

        if source not in sources:
            sources.append(source)

    # --------------------------
    # CONTEXT
    # --------------------------

    context_parts = []

    for doc in docs:

        author = doc.metadata.get("author")

        if not author:
            author = "No author name available"

        context_parts.append(
            f"""
Unit: {doc.metadata['unit']}
Title: {doc.metadata['title']}
Author: {author}
Section: {doc.metadata['section']}

{doc.page_content}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    prompt = PROMPT.format(
        context=context,
        question=question
    )
    
    response = llm.invoke(
        prompt
    )

    # --------------------------
    # OUTPUT
    # --------------------------

    print("\nAnswer:\n")

    print(
        response.content
    )

    print("\n" + "=" * 60)
    print("SOURCES")
    print("=" * 60)

    for source in sources:

        print(
            f"- {source}"
        )

        time.sleep(5)

        