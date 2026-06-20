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
    / "pedagogy_2_topics.json"
)

# ==================================================
# TOPICS FROM INDEX
# ==================================================

TOPICS = [

    # ---------------------------
    # UNIT 1
    # ---------------------------

    ("1.1", "History of ELT in India", 9, 21),
    ("1.2", "Concept of ESL, EFL, TESOL, ESP, EAP", 21, 26),
    ("1.3", "Aims and Objectives of ELT", 26, 33),
    ("1.4", "Bloom's Taxonomy and ELT", 33, 55),

    # ---------------------------
    # UNIT 2
    # ---------------------------

    ("2.1", "Grammar Translation Method", 58, 64),
    ("2.1", "Direct Method", 64, 65),
    ("2.1", "Structural Approach", 65, 69),
    ("2.1", "Situational Approach", 69, 71),
    ("2.1", "Audio-Lingual Method", 71, 74),
    ("2.1", "Bilingual Method", 74, 77),

    ("2.2", "CLT", 77, 80),
    ("2.2", "CLL", 80, 83),
    ("2.2", "TBLT", 83, 86),
    ("2.2", "Post Method Era", 86, 88),

    ("2.3", "Teaching of LSRW", 89, 95),
    ("2.3", "Teaching of Reading", 95, 99),
    ("2.3", "Teaching of Writing", 99, 103),
    ("2.3", "Teaching of Grammar in English", 103, 107),
    ("2.3", "Teaching of Vocabulary in English", 107, 116),
    ("2.3", "Lesson Planning", 116, 126),
    ("2.3", "Preparing Tasks and Activities", 126, 130),

    ("2.4", "Co-Curricular Activities for ELT", 130, 131),
    ("2.4", "English Club", 131, 133),
    ("2.4", "Literary Club", 133, 136),
    ("2.4", "Reading Club", 136, 138),

    # ---------------------------
    # UNIT 3
    # ---------------------------

    ("3.1", "Textbook Analysis", 139, 149),
    ("3.2", "Evaluation of Teaching Learning Materials", 149, 164),
    ("3.3", "Authentic Materials and Online Resources", 164, 169),
    ("3.3", "Online Resources for ELT", 169, 176),
    ("3.4", "Preparation of TLM in ELT", 177, 184),
    ("3.4", "Use of ICT Tools for TLM", 185, 193),

    # ---------------------------
    # UNIT 4
    # ---------------------------

    ("4.1", "Question Paper Analysis", 194, 226),
    ("4.2", "Types of Questions", 227, 228),
    ("4.2", "Types of Tests", 229, 249),
    ("4.3", "Using ICT Tools for Assessment", 249, 256),
    ("4.4", "Assessment of LSRW, Grammar, Vocabulary", 256, 268),
]

# ==================================================
# LOAD OCR PAGES
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
# CREATE TOPICS
# ==================================================

topics = []

for topic_number, title, start_page, end_page in TOPICS:

    text_parts = []

    for page_no in range(start_page, end_page + 1):

        if page_no > len(pages):
            break

        text_parts.append(
            pages[page_no - 1]["text"]
        )

    topics.append(
        {
            "source": "pedagogy_2",
            "topic_number": topic_number,
            "topic": title,
            "page_start": start_page,
            "page_end": end_page,
            "text": "\n\n".join(text_parts)
        }
    )

    print(
        f"Created {topic_number} | {title}"
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
        topics,
        f,
        indent=2,
        ensure_ascii=False
    )

print()
print("=" * 50)
print(f"Topics created : {len(topics)}")
print(f"Saved : {OUTPUT_FILE}")
print("=" * 50)

print(topics[0]["topic"])
print(len(topics[0]["text"]))

print(topics[5]["topic"])
print(len(topics[5]["text"]))