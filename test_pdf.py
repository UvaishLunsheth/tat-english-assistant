# test_pdf.py

from pypdf import PdfReader

PDF_PATH = "data/references/pedagogy_2.PDF"

reader = PdfReader(PDF_PATH)

print(f"Pages: {len(reader.pages)}")

# 1 subtracted from each target page (144->143, 203->202, etc.)
for i in [143, 150, 170, 182, 202, 221, 244, 270]:

    page = reader.pages[i]

    text = page.extract_text()

    print()
    print("=" * 50)
    print(f"PAGE {i + 1}")
    print("=" * 50)

    print(text[:500])