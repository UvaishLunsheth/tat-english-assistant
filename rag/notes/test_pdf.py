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
from langchain_google_genai import ChatGoogleGenerativeAI

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

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# ==================================================
# DETECT SOURCE
# ==================================================

def detect_source(topic):

    docs = vectorstore.similarity_search(
        "Direct method",
        k=20
    )

    counts = {}

    for doc in docs:
        print(doc.metadata)
        print("-" * 80)

    

# ==================================================
# FIND TOPIC UNIT
# ==================================================

def find_topic_metadata(
    topic,
    source
):

    docs = vectorstore.similarity_search(
        topic,
        k=50
    )

    topic = topic.lower().strip()

    for doc in docs:

        meta = doc.metadata

        if meta.get("source") != source:
            continue

        title = str(
            meta.get("title", "")
        ).lower()

        lesson_topic = str(
            meta.get("topic", "")
        ).lower()

        if topic in title or topic in lesson_topic:

            return {
                "unit": meta.get("unit"),
                "title": meta.get("title", ""),
                "topic": meta.get("topic", "")
            }

    return None

# ==================================================
# GET ALL CHUNKS OF UNIT
# ==================================================

def get_unit_docs(
    source,
    unit
):

    data = vectorstore.get()

    docs = []

    for text, meta in zip(
        data["documents"],
        data["metadatas"]
    ):

        if meta.get("source") != source:
            continue

        if meta.get("unit") != unit:
            continue

        docs.append(
            {
                "text": text,
                "meta": meta
            }
        )

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

TITLE: {meta.get('title', '')}

TOPIC: {meta.get('topic', '')}

UNIT: {meta.get('unit', '')}

SECTION: {meta.get('section', '')}

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
    )

    if topic.lower() in [
        "exit",
        "quit"
    ]:
        break

    # ======================================
    # DETECT SOURCE
    # ======================================

    source = detect_source(
        topic
    )

    print()
    print("=" * 80)
    print(
        f"DETECTED SOURCE : {source}"
    )
    print("=" * 80)

    # ======================================
    # FIND UNIT
    # ======================================

    info = find_topic_metadata(
        topic,
        source
    )

    if info is None:

        print(
            "\nTopic not found."
        )

        continue

    print(
        f"\nUNIT : {info['unit']}"
    )

    print(
        f"TITLE : {info['title']}"
    )

    # ======================================
    # GET ALL CHUNKS
    # ======================================

    docs = get_unit_docs(
        source=source,
        unit=info["unit"]
    )

    print(
        f"CHUNKS FOUND : {len(docs)}"
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

    safe_name = (
        topic.lower()
        .replace(" ", "_")
    )

    output_file = (
        OUTPUT_DIR
        / f"{safe_name}.json"
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