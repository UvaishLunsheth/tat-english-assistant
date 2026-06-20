import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "pedagogy_2_topics.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "pedagogy_2_chunks.json"
)

# =====================================
# LOAD TOPICS
# =====================================

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    topics = json.load(f)

# =====================================
# BUILD CHUNKS
# =====================================

chunks = []

for topic in topics:

    try:

        unit_number = int(
            topic["topic_number"].split(".")[0]
        )

    except Exception:

        unit_number = None

    chunks.append({

        "source": "pedagogy_2",

        "unit": unit_number,

        "topic_number": topic["topic_number"],

        "topic": topic["topic"],

        "page_start": topic["page_start"],

        "page_end": topic["page_end"],

        "text": topic["text"]
    })

# =====================================
# SAVE
# =====================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        chunks,
        f,
        indent=2,
        ensure_ascii=False
    )

print()
print(f"Topics loaded : {len(topics)}")
print(f"Chunks created: {len(chunks)}")
print(chunks[20])
print(f"Saved        : {OUTPUT_FILE}")