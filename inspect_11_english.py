import json
from pathlib import Path

# ==========================================
# PATHS
# ==========================================
INPUT_FILE = Path("data/ocr/11_english_raw_pages.json")

# Make sure the file actually exists before trying to read it
if not INPUT_FILE.exists():
    print(f"File not found: {INPUT_FILE}")
    raise SystemExit

# ==========================================
# LOAD DATA
# ==========================================
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    pages = json.load(f)

print(f"Successfully loaded {len(pages)} pages.")

for page in pages:

    text = page["text"]

    if "UNIT " in text.upper():

        print()
        print("=" * 80)
        print(page["page"])
        print("=" * 80)

        print(text[:500])