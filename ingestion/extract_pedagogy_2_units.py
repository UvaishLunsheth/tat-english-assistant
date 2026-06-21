import json
from pathlib import Path

# ==================================================
# PATHS
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "pedagogy"
    / "pedagogy_2_raw_pages.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "pedagogy_2_units.json"
)

# ==================================================
# UNIT MAP
# ==================================================

UNITS = [

    # ------------------
    # BLOCK 1
    # ------------------

    (1, 1,
     "Curriculum - Concept and Meaning, Principles of Curriculum Construction",
     11, 29),

    (1, 2,
     "Different Approaches of Curriculum Organization",
     30, 47),

    (1, 3,
     "Characteristics of a Good English Text Book",
     48, 63),

    (1, 4,
     "Authentic Materials for English Language Teaching and Language Laboratory",
     64, 77),

    # ------------------
    # BLOCK 2
    # ------------------

    (2, 5,
     "Approach, Method and Technique",
     78, 95),

    (2, 6,
     "Approaches - Structural, Communicative, TPR, Thematic, Inductive, Deductive, Whole Language, Constructive, Multilingual",
     96, 110),

    (2, 7,
     "Methods - Grammar Translation, Direct, Bilingual, Dr. West, Structural Situational, Audio Lingual, Natural Method",
     111, 126),

    (2, 8,
     "Techniques - Group Work, Pair Work, Role Play and Dramatisation",
     127, 143),

    # ------------------
    # BLOCK 3
    # ------------------

    (3, 9,
     "Listening and Speaking",
     144, 150),

    (3, 10,
     "Reading",
     151, 170),

    (3, 11,
     "Writing",
     171, 182),

    (3, 12,
     "Introduction to Phonetics",
     183, 202),

    # ------------------
    # BLOCK 4
    # ------------------

    (4, 13,
     "Teaching of Prose and Teaching of Poetry",
     203, 221),

    (4, 14,
     "Resources of Teaching - Multimedia, Online Resources and Social Networking",
     222, 244),

    (4, 15,
     "Planning - Year Plan, Unit Plan, Lesson Plan",
     245, 270),

    (4, 16,
     "Microteaching",
     271, 297),
]

# ==================================================
# LOAD PAGES
# ==================================================

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    pages = json.load(f)

print(
    f"Pages loaded : {len(pages)}"
)

# ==================================================
# BUILD UNITS
# ==================================================

units = []

global_unit = 1

for block_no, unit_no, title, start_page, end_page in UNITS:

    text_parts = []

    for page_no in range(
        start_page,
        end_page + 1
    ):

        if page_no > len(pages):
            break

        text_parts.append(
            pages[page_no - 1]["text"]
        )

    units.append({

        "source": "pedagogy_2",

        "block": block_no,

        "unit": unit_no,

        "global_unit": global_unit,

        "title": title,

        "page_start": start_page,

        "page_end": end_page,

        "text": "\n\n".join(text_parts)
    })

    print(
        f"Created Unit {unit_no} | {title}"
    )

    # Indented to be INSIDE the for loop
    global_unit += 1

# ==================================================
# SAVE
# ==================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        units,
        f,
        indent=2,
        ensure_ascii=False
    )

# ==================================================
# SUMMARY
# ==================================================

print()
print("=" * 60)

print(
    f"Units created : {len(units)}"
)

print(
    f"Saved : {OUTPUT_FILE}"
)

print("=" * 60)

print()
print("FIRST UNIT")
print(units[0]["title"])
print(len(units[0]["text"]))

print()
print("LAST UNIT")
print(units[-1]["title"])
print(len(units[-1]["text"]))
print()
print(units[0].keys())