import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

STD11_FILE = (
    PROJECT_ROOT
    / "data"
    / "std11_chunks_small.json"
)

STD12_FILE = (
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

# ==================================================
# LOAD
# ==================================================

with open(STD11_FILE, "r", encoding="utf-8") as f:
    std11 = json.load(f)

with open(STD12_FILE, "r", encoding="utf-8") as f:
    std12 = json.load(f)

with open(PEDAGOGY_1_FILE, "r", encoding="utf-8") as f:
    pedagogy_1 = json.load(f)

with open(PEDAGOGY_2_FILE, "r", encoding="utf-8") as f:
    pedagogy_2 = json.load(f)

# ==================================================
# SOURCE TAGS
# ==================================================

for row in std11:
    row["source"] = "std11_textbook"

for row in std12:
    row["source"] = "std12_textbook"

for row in pedagogy_1:
    row["source"] = "pedagogy_1"

for row in pedagogy_2:
    row["source"] = "pedagogy_2"

# ==================================================
# COMBINE
# ==================================================

combined = (
    std11
    + std12
    + pedagogy_1
    + pedagogy_2
)

# ==================================================
# SAVE
# ==================================================

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

# ==================================================
# STATS
# ==================================================

print()
print("=" * 70)
print("SOURCE COUNTS")
print("=" * 70)

print(f"Std 11 Textbook : {len(std11)}")
print(f"Std 12 Textbook : {len(std12)}")
print(f"Pedagogy 1      : {len(pedagogy_1)}")
print(f"Pedagogy 2      : {len(pedagogy_2)}")

print("-" * 70)

print(f"TOTAL CHUNKS    : {len(combined)}")

print("=" * 70)

print()
print("SAMPLE KEYS")
print("=" * 70)

print()
print("STD11")
print(std11[0].keys())

print()
print("STD12")
print(std12[0].keys())

print()
print("PEDAGOGY 1")
print(pedagogy_1[0].keys())

print()
print("PEDAGOGY 2")
print(pedagogy_2[0].keys())