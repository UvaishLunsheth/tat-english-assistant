import json

with open(
    "data/pedagogy/pedagogy_2_raw_pages.json",
    "r",
    encoding="utf-8"
) as f:
    pages = json.load(f)

print(pages[4]["text"])   # page 5
print()
print("=" * 80)
print()
print(pages[5]["text"])   # page 6