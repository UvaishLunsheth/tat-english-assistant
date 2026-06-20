import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TEXTBOOK_FILE = (
    PROJECT_ROOT
    / "data"
    / "chunks_small.json"
)

PEDAGOGY_1_FILE = (
    PROJECT_ROOT
    / "data"
    / "pedagogy_chunks_small.json"
)

PEDAGOGY_2_FILE = (
    PROJECT_ROOT
    / "data"
    / "pedagogy_2_chunks_small.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "all_chunks.json"
)

# --------------------------
# LOAD
# --------------------------

with open(TEXTBOOK_FILE, "r", encoding="utf-8") as f:
    textbook = json.load(f)

with open(PEDAGOGY_1_FILE, "r", encoding="utf-8") as f:
    pedagogy_1 = json.load(f)

with open(PEDAGOGY_2_FILE, "r", encoding="utf-8") as f:
    pedagogy_2 = json.load(f)
# --------------------------
# SOURCE TAG
# --------------------------

for row in textbook:

    row["source"] = "textbook"

combined = (
    textbook
    + pedagogy_1
    + pedagogy_2
)

# --------------------------
# SAVE
# --------------------------

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        combined,
        f,
        indent=2,
        ensure_ascii=False
    )

print()
print(f"Textbook chunks   : {len(textbook)}")
print(f"Pedagogy 1 chunks : {len(pedagogy_1)}")
print(f"Pedagogy 2 chunks : {len(pedagogy_2)}")
print(f"Combined chunks   : {len(combined)}")

print(combined[0].keys())
print(combined[600].keys())
print(combined[1000].keys())