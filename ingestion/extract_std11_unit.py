import json
import sys
import time
from pathlib import Path


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from ingestion.load_std11_unit import (
    load_std11_unit
)

from ingestion.std11_section_splitter import (
    split_read_block
)

from utils.std11_read_finder import (
    find_read_positions
)

from services.std11_metadata_extractor import (
    extract_std11_metadata
)

from models.std11_unit_schema import (
    Std11UnitSchema,
    ReadSection
)

from config.std11_unit_structure import (
    STD11_UNIT_STRUCTURE
)

from config.section_markers import (
    SECTION_MARKERS
)

from utils.text_cleaner import (
    clean_pre_task,
    clean_content,
    clean_glossary,
    clean_comprehension,
    clean_author,
    clean_text
)

# Position Helpers
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

# Extract Functions
def extract_std11_unit(
    unit_number: int
):

    print(
        f"\n📖 Extracting Unit {unit_number}"
    )

    structure = (
        STD11_UNIT_STRUCTURE[
            unit_number
        ]
    )

    has_project = structure[
        "has_project"
    ]

    unit_text = load_std11_unit(
        unit_number
    )


# Find Read Functions
    read_positions = (
        find_read_positions(
            unit_text
        )
    )

    read_count = len(
        read_positions
    )

    print(
        f"Reads found : {read_count}"
    )


# Find main sections
    vocabulary_pos = find_required(
        unit_text,
        "Vocabulary"
    )

    functions_pos = unit_text.find(
        "Function",
        vocabulary_pos
    )

    if functions_pos == -1:
        functions_pos = None

    writing_pos = find_required(
        unit_text,
        "Writing"
    )

    activity_pos = find_optional(
        unit_text,
        SECTION_MARKERS["activities"]
    )

    project_pos = find_optional(
        unit_text,
        SECTION_MARKERS["project"]
    )


 # Pre-task

    pre_task = unit_text[
        :read_positions[0]
    ]


# Dynamic Read Blocks                   

    read_blocks = []

    for idx in range(read_count):

        start = read_positions[idx]

        if idx < read_count - 1:

            end = read_positions[
                idx + 1
            ]

        else:

            end = vocabulary_pos

        read_blocks.append(

            unit_text[
                start:end
            ]
        )


 # Other section

    vocab_end = (
        functions_pos
        if functions_pos
        else writing_pos
    )

    vocabulary = unit_text[
        vocabulary_pos:vocab_end
    ]

    functions = ""

    if functions_pos:

        functions = unit_text[
            functions_pos:writing_pos
        ]       


# Writing/Activity/Project

    if has_project:

        writing_end = (
            activity_pos
            if activity_pos
            else project_pos
        )

        writing = unit_text[
            writing_pos:writing_end
        ]

        activities = ""

        if activity_pos:

            activities = unit_text[
                activity_pos:
                project_pos
            ]

        project = None

        if project_pos:

            project = unit_text[
                project_pos:
            ]

    else:

        writing_end = (
            activity_pos
            if activity_pos
            else len(unit_text)
        )

        writing = unit_text[
            writing_pos:
            writing_end
        ]

        activities = ""

        if activity_pos:

            activities = unit_text[
                activity_pos:
            ]

        project = None



# Build Reads

    reads = []

    for i, read_block in enumerate(read_blocks):

        # Add a small delay between read blocks to avoid LLM rate limit
        if i > 0:
            print("   ⏳ Pausing 2 seconds for LLM...")
            time.sleep(2)

        parts = split_read_block(
            read_block
        )

        meta = (
            extract_std11_metadata(
                read_block[:1000]
            )
        )

        reads.append(

            ReadSection(

                title=meta.title,

                author=clean_author(
                    meta.author
                ),

                content=clean_content(
                    parts["content"]
                ),

                glossary=clean_glossary(
                    parts["glossary"]
                ),

                comprehension=clean_comprehension(
                    parts["comprehension"]
                )
            )
        )

# Build Schema

    unit = Std11UnitSchema(

        unit_number=unit_number,

        pre_task=clean_pre_task(
            pre_task
        ),

        reads=reads,

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


# Save

    output_dir = (
        PROJECT_ROOT
        / "data"
        / "std11_units"
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

    return unit


if __name__ == "__main__":

    units_to_extract = [6, 7, 8, 9, 10]

    for idx, unit_num in enumerate(units_to_extract):
        
        extract_std11_unit(unit_num)

        