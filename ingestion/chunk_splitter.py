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
    / "chunks.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "chunks_small.json"
)


# ==================================================
# CLEANER
# ==================================================

def clean_text(text: str) -> str:

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ==================================================
# LOAD CHUNKS
# ==================================================

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    chunks = json.load(f)


# ==================================================
# SPLITTER
# ==================================================

splitter = RecursiveCharacterTextSplitter(

    chunk_size=700,

    chunk_overlap=100,

    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)


# ==================================================
# SPLIT
# ==================================================

small_chunks = []

for chunk in chunks:

    text = chunk["text"]

    pieces = splitter.split_text(
        text
    )

    chunk_id = 1

    for piece in pieces:

        piece = clean_text(
            piece
        )

        if len(piece) < 50:
            continue

        small_chunks.append({

            "unit": chunk["unit"],

            "section": chunk["section"],

            "title": chunk["title"],

            "author": chunk.get("author"),

            "chunk_id": chunk_id,

            "char_count": len(piece),

            "text": piece
        })

        chunk_id += 1


# ==================================================
# SAVE
# ==================================================

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


# ==================================================
# STATS
# ==================================================

avg_size = sum(
    len(chunk["text"])
    for chunk in small_chunks
) // len(small_chunks)

print()

print(
    f"Original chunks : {len(chunks)}"
)

print(
    f"Small chunks    : {len(small_chunks)}"
)

print(
    f"Average size    : {avg_size} chars"
)

print()

print(
    f"✅ Saved: {OUTPUT_FILE}"
)