import json
import fitz
import pytesseract
from pathlib import Path
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PDF_PATH = (
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

pdf = fitz.open(PDF_PATH)

pages = []

for i in range(len(pdf)):

    page = pdf[i]

    pix = page.get_pixmap(
        matrix=fitz.Matrix(4, 4)
    )

    img = Image.fromarray(
        __import__("numpy").frombuffer(
            pix.samples,
            dtype="uint8"
        ).reshape(
            pix.height,
            pix.width,
            pix.n
        )
    )

    text = pytesseract.image_to_string(
    img,
    lang="eng"
)

    pages.append(
        {
            "page": i + 1,
            "text": text
        }
    )

    print(
        f"Done page {i+1}/{len(pdf)}"
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
print(f"Saved: {OUTPUT_FILE}")
print(f"Pages: {len(pages)}")
print(text[:1000])