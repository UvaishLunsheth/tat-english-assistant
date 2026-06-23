import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

UNITS_DIR = (
    PROJECT_ROOT
    / "data"
    / "std11_units"
)

chunks = []

for file in sorted(
    UNITS_DIR.glob("unit_*.json")
):

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        unit = json.load(f)

    unit_number = unit["unit_number"]

    # =====================================
    # READS (DYNAMIC)
    # =====================================

    for index, read in enumerate(
        unit["reads"],
        start=1
    ):

        chunks.append({

            "unit": unit_number,

            "section": f"read_{index}_content",

            "title": read["title"],

            "author": read.get("author"),

            "text": read["content"]
        })

        chunks.append({

            "unit": unit_number,

            "section": f"read_{index}_glossary",

            "title": read["title"],

            "author": read.get("author"),

            "text": read["glossary"]
        })

        chunks.append({

            "unit": unit_number,

            "section": f"read_{index}_comprehension",

            "title": read["title"],

            "author": read.get("author"),

            "text": read["comprehension"]
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
    / "std11_chunks.json"
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
print("=" * 60)
print(f"Total chunks : {len(chunks)}")
print(f"Saved to     : {output_path}")
print("=" * 60)