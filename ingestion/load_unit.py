import json
from pathlib import Path

from config.unit_ranges import UNIT_RANGES


RAW_PAGES_PATH = Path("data/raw_pages.json")


def load_unit(unit_number: int) -> str:

    start_page, end_page = UNIT_RANGES[unit_number]

    with open(
        RAW_PAGES_PATH,
        "r",
        encoding="utf-8"
    ) as f:
        pages = json.load(f)

    texts = []

    for page in pages:

        if start_page <= page["page"] <= end_page:
            texts.append(page["text"])

    return "\n".join(texts)