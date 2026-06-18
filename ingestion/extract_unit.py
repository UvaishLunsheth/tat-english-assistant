import json
import sys
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ingestion.load_unit import load_unit
from ingestion.section_splitter import split_read_block

from services.metadata_extractor import extract_metadata

from models.unit_schema import (
UnitSchema,
ReadSection
)

from config.unit_structure import UNIT_STRUCTURE
from config.section_markers import SECTION_MARKERS

from utils.text_cleaner import (
clean_pre_task,
clean_content,
clean_glossary,
clean_comprehension,
clean_author,
clean_text
)

# ==================================================

# HELPERS

# ==================================================

def find_required(
text: str,
keyword: str
):
    pos = text.find(keyword)

    if pos == -1:
      raise ValueError(
        f"{keyword} not found"
    )

    return pos


def find_optional(
text: str,
keywords: list[str]
):
   
   positions = []

   for keyword in keywords:

    pos = text.find(keyword)

    if pos != -1:
        positions.append(pos)

   if not positions:
       return None

   return min(positions)


# ==================================================

# EXTRACTION

# ==================================================

def extract_unit(unit_number: int):
    
    print(f"\n📖 Extracting Unit {unit_number}")
    
    structure = UNIT_STRUCTURE[unit_number]

    read_count = structure["read_count"]

    has_project = structure["has_project"]

    unit_text = load_unit(unit_number)

    # ----------------------------------
    # FIND POSITIONS
    # ----------------------------------

    read_1_pos = find_required(
        unit_text,
        "Read 1"
    )

    vocabulary_pos = find_required(
    unit_text,
    "Vocabulary"
   )

# Find Function AFTER Vocabulary
    functions_pos = unit_text.find(
    "Function",
    vocabulary_pos
   )

    if functions_pos == -1:
       functions_pos = None

# Find Writing AFTER Function
    writing_pos = unit_text.find(
    "Writing",
    functions_pos if functions_pos else vocabulary_pos
)

    if writing_pos == -1:

       raise ValueError("Writing not found")    
    

    if unit_number == 3:
        print("\n===== DEBUG UNIT 3 =====")
        print("vocabulary_pos =", vocabulary_pos)
        print("functions_pos =", functions_pos)
        print("writing_pos =", writing_pos)

    print(
        unit_text[
            vocabulary_pos:
            writing_pos
        ][:4000]
    )

    activity_pos = find_optional(
        unit_text,
        SECTION_MARKERS["activities"]
    )

    project_pos = find_optional(
        unit_text,
        SECTION_MARKERS["project"]
    )

    
    read_2_pos = None

    if read_count == 2:

        read_2_pos = find_required(
            unit_text,
            "Read 2"
        )

    # ----------------------------------
    # PRE TASK
    # ----------------------------------

    pre_task = unit_text[
        :read_1_pos
    ]

    # ----------------------------------
    # READ BLOCKS
    # ----------------------------------

    if read_count == 2:

        read_1_block = unit_text[
            read_1_pos:read_2_pos
        ]

        read_2_block = unit_text[
            read_2_pos:vocabulary_pos
        ]

    else:

        read_1_block = unit_text[
            read_1_pos:vocabulary_pos
        ]

        read_2_block = None

    # ----------------------------------
    # OTHER SECTIONS
    # ----------------------------------

    vocab_end = functions_pos if functions_pos is not None else writing_pos
    vocabulary = unit_text[
        vocabulary_pos:vocab_end
    ]

    functions = unit_text[
        functions_pos:writing_pos
    ] if functions_pos is not None else ""

    if has_project:

        writing_end = activity_pos if activity_pos is not None else project_pos
        writing = unit_text[
            writing_pos:writing_end
        ]

        if activity_pos is not None:
            activities = unit_text[
                activity_pos:project_pos
            ]
        else:
            activities = ""

        project = unit_text[
            project_pos:
        ] if project_pos is not None else None

    else:

        writing_end = activity_pos if activity_pos is not None else len(unit_text)
        writing = unit_text[
            writing_pos:writing_end
        ]

        if activity_pos is not None:
            activities = unit_text[
                activity_pos:
            ]
        else:
            activities = ""

        project = None

    # ----------------------------------
    # READ 1
    # ----------------------------------

    read_1_parts = split_read_block(
        read_1_block
    )

    # RESOLVED ISSUE: Pass only the top snippet to protect against timeouts
    read_1_meta = extract_metadata(
        read_1_block[:1000]
    )

    # ----------------------------------
    # READ 2
    # ----------------------------------

    read_2_parts = None
    read_2_meta = None

    if read_count == 2:

        read_2_parts = split_read_block(
            read_2_block
        )

        # RESOLVED ISSUE: Pass only the top snippet to protect against timeouts
        read_2_meta = extract_metadata(
            read_2_block[:1000]
        )

    # ----------------------------------
    # BUILD SCHEMA
    # ----------------------------------

    unit = UnitSchema(

        unit_number=unit_number,

        pre_task=clean_pre_task(
            pre_task
        ),

        read_1=ReadSection(

            title=read_1_meta.title,

            author=clean_author(
                read_1_meta.author
            ),

            content=clean_content(
                read_1_parts["content"]
            ),

            glossary=clean_glossary(
                read_1_parts["glossary"]
            ),

            comprehension=clean_comprehension(
                read_1_parts["comprehension"]
            )
        ),

        read_2=(

            ReadSection(

                title=read_2_meta.title,

                author=clean_author(
                    read_2_meta.author
                ),

                content=clean_content(
                    read_2_parts["content"]
                ),

                glossary=clean_glossary(
                    read_2_parts["glossary"]
                ),

                comprehension=clean_comprehension(
                    read_2_parts["comprehension"]
                )
            )

            if read_count == 2

            else None
        ),

        vocabulary=clean_text(
            vocabulary
        ),

        functions=clean_text(
            functions
        ),

        writing=clean_text(
            writing
        ),

        activities=clean_text(
            activities
        ),

        project=(
            clean_text(project)
            if project
            else None
        )
    )

    # ----------------------------------
    # SAVE
    # ----------------------------------

    output_dir = (
        PROJECT_ROOT
        / "data"
        / "units"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = (
        output_dir
        / f"unit_{unit_number}.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            unit.model_dump(),
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"✅ Unit {unit_number} saved"
    )

    print(
        f"📁 {output_path}"
    )

    return unit


# ==================================================

# TEST

# ==================================================

if __name__ == "__main__":
    extract_unit(3)