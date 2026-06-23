from pathlib import Path
import json
import re

# ==================================================
# PATHS
# ==================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "ocr"
    / "11_english_raw_pages.json"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "std11_units"
)

OUTPUT_DIR.mkdir(
    exist_ok=True
)

# ==================================================
# LOAD OCR PAGES
# ==================================================
with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:
    pages = json.load(f)

# ==================================================
# DETECT UNIT STARTS
# ==================================================
unit_starts = []

pattern = re.compile(
    r"\bUNIT\s+(\d+)\b",
    re.IGNORECASE
)

for page in pages:
    text = page.get(
        "text",
        ""
    )

    match = pattern.search(
        text
    )

    if match:
        unit_no = int(
            match.group(1)
        )

        unit_starts.append(
            (
                unit_no,
                page["page"]
            )
        )

# ==================================================
# SORT
# ==================================================
unit_starts.sort(
    key=lambda x: x[0]
)

print()
print("=" * 70)
print("UNIT STARTS")
print("=" * 70)

for unit_no, page_no in unit_starts:
    print(
        f"Unit {unit_no} -> Page {page_no}"
    )

# ==================================================
# BUILD UNITS
# ==================================================
for idx, (unit_no, start_page) in enumerate(unit_starts):

    if idx < len(unit_starts) - 1:
        end_page = (
            unit_starts[idx + 1][1] - 1
        )
    else:
        end_page = len(
            pages
        )

    unit_pages = [
        p
        for p in pages
        if start_page <= p["page"] <= end_page
    ]

    full_text = "\n\n".join(
        p["text"] for p in unit_pages
    )

    # ==============================================
    # TITLE
    # ==============================================
    title = ""

    lines = [
        line.strip()
        for line in full_text.splitlines()
        if line.strip()
    ]

    for i, line in enumerate(lines):
        if line.upper().startswith("READ 1"):
            if i + 1 < len(lines):
                title = lines[i + 1]
            break

    # fallback
    if not title:
        title = f"Unit {unit_no}"

    # ==============================================
    # SAVE
    # ==============================================
    data = {
        "unit": unit_no,
        "title": title,
        "start_page": start_page,
        "end_page": end_page,
        "text": full_text
    }

    output_file = (
        OUTPUT_DIR
        / f"unit_{unit_no}.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Created : {output_file.name}"
    )

# ==================================================
# DONE
# ==================================================
print()
print("=" * 70)
print("STD 11 UNIT EXTRACTION COMPLETE")
print("=" * 70)
print(f"Units created : {len(unit_starts)}")
print(f"Saved in      : {OUTPUT_DIR}")
print("=" * 70)