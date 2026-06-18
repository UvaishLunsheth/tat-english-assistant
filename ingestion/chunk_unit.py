import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

UNITS_DIR = PROJECT_ROOT / "data" / "units"

chunks = []

for file in sorted(UNITS_DIR.glob("unit_*.json")):

    with open(file, "r", encoding="utf-8") as f:
        unit = json.load(f)

    unit_number = unit["unit_number"]

    # =====================================
    # READ 1
    # =====================================

    read_1 = unit["read_1"]

    chunks.append({
        "unit": unit_number,
        "section": "read_1_content",
        "title": read_1["title"],
        "author": read_1.get("author"),
        "text": read_1["content"]
    })

    chunks.append({
        "unit": unit_number,
        "section": "read_1_glossary",
        "title": read_1["title"],
        "author": read_1.get("author"),
        "text": read_1["glossary"]
    })

    chunks.append({
        "unit": unit_number,
        "section": "read_1_comprehension",
        "title": read_1["title"],
        "author": read_1.get("author"),
        "text": read_1["comprehension"]
    })

    # =====================================
    # READ 2
    # =====================================

    if unit.get("read_2"):

        read_2 = unit["read_2"]

        chunks.append({
            "unit": unit_number,
            "section": "read_2_content",
            "title": read_2["title"],
            "author": read_2.get("author"),
            "text": read_2["content"]
        })

        chunks.append({
            "unit": unit_number,
            "section": "read_2_glossary",
            "title": read_2["title"],
            "author": read_2.get("author"),
            "text": read_2["glossary"]
        })

        chunks.append({
            "unit": unit_number,
            "section": "read_2_comprehension",
            "title": read_2["title"],
            "author": read_2.get("author"),
            "text": read_2["comprehension"]
        })

    # =====================================
    # OTHER SECTIONS
    # =====================================

    for section in [
        "vocabulary",
        "functions",
        "writing",
        "activities",
        "project"
    ]:

        value = unit.get(section)

        if value:

            chunks.append({
                "unit": unit_number,
                "section": section,
                "title": section.title(),
                "author": None,
                "text": value
            })

# =====================================
# SAVE
# =====================================

output_path = (
    PROJECT_ROOT
    / "data"
    / "chunks.json"
)

with open(
    output_path,
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
print(f"✅ Saved {len(chunks)} chunks")
print(f"📁 {output_path}")