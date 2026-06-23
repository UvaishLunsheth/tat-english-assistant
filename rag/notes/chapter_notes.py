from pathlib import Path
import sys
import json
import re

from dotenv import load_dotenv

# ==================================================
# PATHS
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

EXAM_DIR = PROJECT_ROOT / "rag" / "exam"

if str(EXAM_DIR) not in sys.path:
    sys.path.insert(0, str(EXAM_DIR))

# ==================================================
# IMPORTS
# ==================================================

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Upgraded to OpenAI to use your API balance and avoid rate limits!
from langchain_openai import ChatOpenAI

from prompts import CHAPTER_NOTES_PROMPT

load_dotenv()

# ==================================================
# VECTOR DB
# ==================================================

VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = Chroma(
    persist_directory=str(VECTOR_DB_DIR),
    embedding_function=embeddings
)

# ==================================================
# LLM
# ==================================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# ==================================================
# FIND BEST MATCH
# ==================================================

def find_best_match(topic: str):

    docs = vectorstore.similarity_search(
        topic,
        k=20
    )

    if not docs:
        return None

    return docs[0].metadata

# ==================================================
# GET UNIT DOCS
# ==================================================

def get_unit_docs(
    source,
    unit
):

    data = vectorstore.get(
        where={
            "$and": [
                {"source": source},
                {"unit": unit}
            ]
        }
    )

    docs = []

    for text, meta in zip(
        data["documents"],
        data["metadatas"]
    ):

        docs.append({
            "text": text,
            "meta": meta
        })

    return docs

# ==================================================
# BUILD CONTEXT
# ==================================================

def build_context(docs):

    parts = []

    for item in docs:

        meta = item["meta"]

        parts.append(
            f"""
SOURCE: {meta.get('source')}

TITLE: {meta.get('title','')}

TOPIC: {meta.get('topic','')}

UNIT: {meta.get('unit','')}

SECTION: {meta.get('section','')}

CONTENT:
{item['text']}
"""
        )

    return "\n\n".join(parts)

# ==================================================
# MAIN LOOP
# ==================================================

while True:

    topic = input(
        "\nTopic: "
    ).strip()

    if topic.lower() in [
        "exit",
        "quit"
    ]:
        break

    # ======================================
    # FIND BEST MATCH
    # ======================================

    match = find_best_match(
        topic
    )

    if not match:

        print("\nTopic not found.")
        continue

    source = match["source"]
    unit = match["unit"]

    print()
    print("=" * 80)
    print("MATCH FOUND")
    print("=" * 80)

    print(
        f"Source : {source}"
    )

    print(
        f"Unit   : {unit}"
    )

    if match.get("title"):

        print(
            f"Title  : {match['title']}"
        )

    if match.get("topic"):

        print(
            f"Topic  : {match['topic']}"
        )

    # ======================================
    # GET ALL UNIT CHUNKS
    # ======================================

    docs = get_unit_docs(
        source=source,
        unit=unit
    )

    print(
        f"\nChunks Found : {len(docs)}"
    )

    # ======================================
    # BUILD CONTEXT
    # ======================================

    context = build_context(
        docs
    )

    # ======================================
    # PROMPT
    # ======================================

    prompt = CHAPTER_NOTES_PROMPT.format(
        topic=topic,
        source=source,
        context=context
    )

    # ======================================
    # GENERATE
    # ======================================

    try:

        response = llm.invoke(
            prompt
        )

    except Exception as e:

        print()
        print("=" * 80)
        print("LLM ERROR")
        print("=" * 80)

        print(str(e))

        continue

    # ======================================
    # CLEAN JSON
    # ======================================

    raw = response.content

    raw = re.sub(
        r"^```json",
        "",
        raw.strip(),
        flags=re.IGNORECASE
    )

    raw = re.sub(
        r"```$",
        "",
        raw.strip()
    )

    try:

        notes = json.loads(
            raw
        )

    except Exception:

        print()
        print("=" * 80)
        print("INVALID JSON")
        print("=" * 80)

        print(raw)

        continue

    # ======================================
    # SAVE
    # ======================================

    OUTPUT_DIR = (
        PROJECT_ROOT
        / "generated_notes"
    )

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    safe_name = re.sub(
        r"[^a-zA-Z0-9_]+",
        "_",
        topic.lower()
    )

    output_file = (
        OUTPUT_DIR
        / f"{source}_{safe_name}.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            notes,
            f,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("=" * 80)
    print("NOTES SAVED")
    print("=" * 80)

    print(output_file)