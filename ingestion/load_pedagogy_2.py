import json
from pathlib import Path

from pypdf import PdfReader

# ==================================================
# PATHS
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "references"
    / "pedagogy_2.pdf"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "pedagogy"
    / "pedagogy_2_raw_pages.json"
)

# ==================================================
# LOAD PDF
# ==================================================

reader = PdfReader(INPUT_FILE)

print(
    f"Pages found : {len(reader.pages)}"
)

# ==================================================
# EXTRACT PAGES
# ==================================================

pages = []

for i, page in enumerate(reader.pages):

    text = page.extract_text()

    if text is None:
        text = ""

    text = text.strip()

    pages.append(
        {
            "page": i + 1,
            "text": text
        }
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
        pages,
        f,
        indent=2,
        ensure_ascii=False
    )

print()
print(
    f"Pages extracted : {len(pages)}"
)

print(
    f"Saved : {OUTPUT_FILE}"
)

print()
print("Sample page:")
print("-" * 50)

print(
    pages[10]["text"][:500]
)