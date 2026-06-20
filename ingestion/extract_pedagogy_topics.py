import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "pedagogy"
    / "pedagogy_1_raw_pages.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "pedagogy_topics.json"
)

# =====================================
# LOAD PAGES
# =====================================

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:
    pages = json.load(f)

# =====================================
# TOPIC PATTERN
# =====================================

TOPIC_PATTERN = re.compile(
    r"^\s*(\d+\.\d+)\s+([A-Za-z].+?)\s*$",
    re.MULTILINE
)

topics = []
current_topic = None

# =====================================
# PROCESS PAGES
# =====================================

for page in pages:

    page_no = page["page"]
    text = page["text"]

    # ---------------------------------
    # SKIP TABLE OF CONTENTS PAGES
    # ---------------------------------

    lower_text = text.lower()

    if (
        "structure" in lower_text
        and "suggested reading" in lower_text
    ):
        print(f"⏭ Skipping TOC page {page_no}")
        continue

    matches = list(
        TOPIC_PATTERN.finditer(text)
    )

    # ---------------------------------
    # TABLE OF CONTENTS PAGE
    # ---------------------------------

    if len(matches) >= 5:

        print(
            f"⏭ Skipping TOC page {page_no}"
        )

        continue

    # ---------------------------------
    # NO NEW TOPIC ON PAGE
    # ---------------------------------

    if not matches:

        if current_topic:

            current_topic["text"] += (
                "\n\n" + text
            )

            current_topic["page_end"] = page_no

        continue

    # ---------------------------------
    # TOPICS FOUND
    # ---------------------------------

    for i, match in enumerate(matches):

        topic_number = match.group(1).strip()
        topic_title = match.group(2).strip()

        print(
            f"Found topic {topic_number} "
            f"on page {page_no}"
        )

        start_pos = match.end()

        if i < len(matches) - 1:

            end_pos = (
                matches[i + 1].start()
            )

        else:

            end_pos = len(text)

        content = text[
            start_pos:end_pos
        ].strip()

        if current_topic:

            topics.append(
                current_topic
            )

        current_topic = {

            "topic_number": topic_number,

            "topic": topic_title,

            "page_start": page_no,

            "page_end": page_no,

            "text": content
        }

# =====================================
# SAVE LAST TOPIC
# =====================================

if current_topic:

    topics.append(
        current_topic
    )
# =====================================
# KEEP ONLY LARGEST VERSION
# =====================================

best_topics = {}

for topic in topics:

    key = topic["topic_number"]

    if key not in best_topics:

        best_topics[key] = topic

    else:

        if len(topic["text"]) > len(
            best_topics[key]["text"]
        ):

            best_topics[key] = topic

topics = sorted(
    best_topics.values(),
    key=lambda x: (
        float(x["topic_number"])
    )
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
        topics,
        f,
        indent=2,
        ensure_ascii=False
    )

print()
print("=" * 50)
print(f"Topics extracted : {len(topics)}")
print(f"Saved : {OUTPUT_FILE}")
print("=" * 50)