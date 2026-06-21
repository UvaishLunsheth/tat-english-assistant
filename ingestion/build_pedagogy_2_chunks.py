import json
from pathlib import Path

# =====================================
# PATHS
# =====================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "pedagogy_2_units.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "pedagogy_2_chunks_small.json"
)

# =====================================
# CHUNK SETTINGS
# =====================================

CHUNK_SIZE = 1000
OVERLAP = 200

# =====================================
# LOAD UNITS
# =====================================

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    units = json.load(f)

# =====================================
# BUILD CHUNKS
# =====================================

chunks = []

for unit in units:

    text = unit["text"]

    start = 0
    chunk_id = 0

    while start < len(text):

        end = start + CHUNK_SIZE

        chunk_text = text[start:end]

        chunks.append({

            "source": "pedagogy_2",

            "block": unit["block"],

            "unit": unit["unit"],

            "global_unit": unit["global_unit"],

            "title": unit["title"],

            "page_start": unit["page_start"],

            "page_end": unit["page_end"],

            "chunk_id": chunk_id,

            "char_count": len(chunk_text),

            "text": chunk_text
        })

        chunk_id += 1

        start += (
            CHUNK_SIZE
            - OVERLAP
        )

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

# =====================================
# SUMMARY
# =====================================

print()
print("=" * 60)

print(
    f"Units loaded : {len(units)}"
)

print(
    f"Chunks created : {len(chunks)}"
)

print(
    f"Saved : {OUTPUT_FILE}"
)

print("=" * 60)

print()
print("FIRST CHUNK")
print(chunks[0].keys())

print()
print(chunks[0]["title"])

print()
print(chunks[0]["char_count"])

print(chunks[0].keys())