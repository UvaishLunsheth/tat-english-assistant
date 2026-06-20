import json
import re
from pathlib import Path

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "pedagogy_2_chunks.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "pedagogy_2_chunks_small.json"
)

# =====================================
# CLEANER
# =====================================

def clean_text(text):

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()

# =====================================
# LOAD
# =====================================

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    chunks = json.load(f)

# =====================================
# SPLITTER
# =====================================

splitter = RecursiveCharacterTextSplitter(

    chunk_size=1000,
    chunk_overlap=150,

    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)

# =====================================
# SPLIT
# =====================================

small_chunks = []

for chunk in chunks:

    pieces = splitter.split_text(
        chunk["text"]
    )

    chunk_id = 1

    for piece in pieces:

        piece = clean_text(piece)

        if len(piece) < 50:
            continue

        small_chunks.append({

            "source": chunk["source"],

            "unit": chunk["unit"],

            "topic_number": chunk["topic_number"],

            "topic": chunk["topic"],

            "page_start": chunk["page_start"],

            "page_end": chunk["page_end"],

            "chunk_id": chunk_id,

            "char_count": len(piece),

            "text": piece
        })

        chunk_id += 1

# =====================================
# SAVE
# =====================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        small_chunks,
        f,
        indent=2,
        ensure_ascii=False
    )

print()
print(f"Original topics : {len(chunks)}")
print(f"Small chunks    : {len(small_chunks)}")

avg_size = sum(
    x["char_count"]
    for x in small_chunks
) // len(small_chunks)

print(f"Average size    : {avg_size}")
print()
print(f"Saved : {OUTPUT_FILE}")
print(len(small_chunks))
print(small_chunks[0])