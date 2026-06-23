from pathlib import Path
import sys
import json
import re

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from prompts import TOPIC_EXAM_PROMPT

# ==================================================
# PATHS
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv()

# ==================================================
# VECTOR DB
# ==================================================

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

# ==================================================
# LLM
# ==================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# ==================================================
# DETECT BEST SOURCE
# ==================================================

def detect_source(topic):

    topic_clean = topic.lower().strip()

    results = vectorstore.similarity_search(
        topic,
        k=20
    )

    # 1. Exact TITLE Match
    for doc in results:
        title = doc.metadata.get("title", "").lower().strip()
        if title and title == topic_clean:
            return doc.metadata.get("source", "")

    # 2. Exact TOPIC Match
    for doc in results:
        lesson_topic = doc.metadata.get("topic", "").lower().strip()
        if lesson_topic and lesson_topic == topic_clean:
            return doc.metadata.get("source", "")

    # 3. Fallback to Source Detection (Frequency Count)
    counts = {
        "textbook": 0,
        "pedagogy_1": 0,
        "pedagogy_2": 0
    }

    for doc in results:

        source = doc.metadata.get(
            "source",
            ""
        )

        if source in counts:
            counts[source] += 1

    best_source = max(
        counts,
        key=counts.get
    )

    return best_source

# ==================================================
# FILTER DOCS
# ==================================================

def filter_topic_docs(
    topic,
    docs,
    source
):

    topic = topic.lower().strip()

    filtered = []

    for doc in docs:

        if doc.metadata.get(
            "source"
        ) != source:
            continue

        title = (
            doc.metadata
            .get("title", "")
            .lower()
            .strip()
        )

        lesson_topic = (
            doc.metadata
            .get("topic", "")
            .lower()
            .strip()
        )

        if topic in title:

            filtered.append(doc)

            continue

        if topic in lesson_topic:

            filtered.append(doc)

            continue

    return filtered

# ==================================================
# BUILD CONTEXT
# ==================================================

def build_context(docs):

    parts = []

    for doc in docs:

        meta = doc.metadata

        parts.append(
            f"""
SOURCE: {meta.get('source')}

TITLE: {meta.get('title', '')}

TOPIC: {meta.get('topic', '')}

UNIT: {meta.get('unit', '')}

SECTION: {meta.get('section', '')}

CONTENT:

{doc.page_content[:1500]}
"""
        )

    return "\n\n".join(parts)

# ==================================================
# MAIN LOOP
# ==================================================

while True:

    topic = input("\nTopic: ")

    if topic.lower() in [
        "exit",
        "quit"
    ]:
        break

    # ==========================================
    # DETECT SOURCE
    # ==========================================

    source = detect_source(
        topic
    )

    print()
    print("=" * 80)
    print(f"DETECTED SOURCE : {source}")
    print("=" * 80)

    # ==========================================
    # RETRIEVE
    # ==========================================

    results = vectorstore.similarity_search(
        topic,
        k=30
    )

    docs = filter_topic_docs(
        topic=topic,
        docs=results,
        source=source
    )

    # fallback

    if len(docs) < 3:

        docs = [

            doc

            for doc in results

            if doc.metadata.get(
                "source"
            ) == source
        ][:15]

    # ==========================================
    # DEBUG
    # ==========================================

    print()
    print("=" * 80)
    print("RETRIEVED DOCUMENTS")
    print("=" * 80)

    for doc in docs:

        print(
            doc.metadata
        )

    # ==========================================
    # CONTEXT
    # ==========================================

    context = build_context(
        docs
    )

    prompt = TOPIC_EXAM_PROMPT.format(
        topic=topic,
        context=context
    )

    # ==========================================
    # GENERATE
    # ==========================================

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

    # ==========================================
    # PARSE JSON
    # ==========================================

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

        paper = json.loads(
            raw
        )

    except Exception:

        print()
        print("=" * 80)
        print("INVALID JSON")
        print("=" * 80)

        print(raw)

        continue

    # ==========================================
    # SAVE
    # ==========================================

    OUTPUT_DIR = (
        PROJECT_ROOT
        / "generated_papers"
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
            paper,
            f,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("=" * 80)
    print("PAPER SAVED")
    print("=" * 80)

    print(output_file)