from pathlib import Path
import json

import easyocr
import numpy as np

from pdf2image import convert_from_path
from tqdm import tqdm

PDF_PATH = Path("data/11-English.pdf")

OUTPUT_DIR = Path("data/ocr")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "11_english_raw_pages.json"


def pdf_to_images(pdf_path):

    print("Converting PDF...")

    images = convert_from_path(
        pdf_path,
        dpi=200
    )

    print(f"Total pages : {len(images)}")

    return images


def extract_text(reader, image):

    image_np = np.array(image)

    result = reader.readtext(
        image_np,
        detail=0,
        paragraph=True
    )

    return "\n".join(result)


def main():

    reader = easyocr.Reader(
        ["en"],
        gpu=False
    )

    images = pdf_to_images(PDF_PATH)

    pages = []

    for page_no, image in enumerate(
        tqdm(images),
        start=1
    ):

        text = extract_text(
            reader,
            image
        )

        pages.append(
            {
                "page": page_no,
                "chars": len(text),
                "text": text
            }
        )

        if page_no % 10 == 0:

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
    print("=" * 50)
    print("OCR COMPLETE")
    print("=" * 50)
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()