import sys
import json
from pathlib import Path

# Add the main project folder to Python's path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.std11_unit_ranges import (
    STD11_UNIT_RANGES
)

# ==================================================
# PATHS
# ==================================================

RAW_PAGES_PATH = Path(
    "data/ocr/11_english_raw_pages.json"
)

# ==================================================
# LOAD UNIT
# ==================================================


def load_std11_unit(

    unit_number: int

) -> str:



    start_page, end_page = (

        STD11_UNIT_RANGES[unit_number]

    )



    with open(

        RAW_PAGES_PATH,

        "r",

        encoding="utf-8"

    ) as f:



        pages = json.load(f)



    texts = []



    for page in pages:



        if (

            start_page

            <= page["page"]

            <= end_page

        ):



            texts.append(

                page["text"]

            )



    return "\n".join(texts)