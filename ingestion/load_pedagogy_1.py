import json
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

# ==========================================
# PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PDF_PATH = (
    PROJECT_ROOT
    / "data"
    / "references"
    / "pedagogy_1.pdf"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "pedagogy"
    / "pedagogy_1_raw_pages.json"
)

# ==========================================
# LOAD PDF
# ==========================================

loader = PyPDFLoader(str(PDF_PATH))

documents = loader.load()

print(f"Total Pages: {len(documents)}")

# ==========================================
# CONVERT TO JSON
# ==========================================

pages = []

for i, doc in enumerate(documents):

    pages.append({
        "page": i + 1,
        "text": doc.page_content
    })

# ==========================================
# SAVE
# ==========================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

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
print("✅ Saved")
print(OUTPUT_FILE)