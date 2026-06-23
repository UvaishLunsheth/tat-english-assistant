import json
from pathlib import Path

import easyocr
import numpy as np  
from pdf2image import convert_from_path
from tqdm import tqdm

PDF_PATH = Path("data/12-English.pdf")
OUTPUT_PATH = Path("data/raw_pages.json")

def pdf_to_images(pdf_path):
    # 2. Fixed indentation for the whole file
    print("Converting PDF to images...")
    images = convert_from_path(pdf_path)
    print(f"Total pages: {len(images)}")
    return images

def extract_text(reader, image):
    # <-- 3. Converted PIL image to NumPy array so EasyOCR can read it
    image_np = np.array(image)
    
    result = reader.readtext(
        image_np, 
        detail=0, 
        paragraph=True
    )
    return "\n".join(result)

def main():
    reader = easyocr.Reader(["en"])
    images = pdf_to_images(PDF_PATH)
    pages = []

    for page_no, image in enumerate(tqdm(images), start=1):
        text = extract_text(reader, image)
        
        pages.append({
            "page": page_no,
            "text": text
        })

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(
            pages,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"\nSaved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()