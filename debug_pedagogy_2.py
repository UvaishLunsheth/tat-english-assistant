import json

with open(
    "data/pedagogy_2_topics.json",
    "r",
    encoding="utf-8"
) as f:
    topics = json.load(f)

for topic in topics:

    if topic["topic"] == "Direct Method":

        print(topic["text"][:3000])
        break