import json
from pathlib import Path

# Load the sections file
FILE_PATH = Path("data/pedagogy_2_sections.json")

with open(FILE_PATH, "r", encoding="utf-8") as f:
    sections = json.load(f)

print()
print("=" * 60)
print("SECTIONS PER UNIT")
print("=" * 60)

counts = {}

for section in sections:
    unit_no = section["unit"]
    counts[unit_no] = counts.get(unit_no, 0) + 1

for unit_no in sorted(counts):
    print(
        f"Unit {unit_no} -> {counts[unit_no]} sections"
    )