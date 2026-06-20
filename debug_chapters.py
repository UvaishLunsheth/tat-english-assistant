import json

# Load the raw pages
with open("data/pedagogy/pedagogy_2_raw_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)
    
for page in pages:

    text = page["text"]

    if "It is one of the best method in teaching English" in text:

        print("\nFOUND PAGE:", page["page"])
        print(text[:1500])