
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# ==================================================
# PROJECT ROOT
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==================================================
# IMPORTS
# ==================================================

from ingestion.load_unit import load_unit
from models.unit_preview import UnitPreview

# ==================================================
# ENV
# ==================================================

load_dotenv()

# ==================================================
# LLM
# ==================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

structured_llm = llm.with_structured_output(
    UnitPreview
)

# ==================================================
# LOAD UNIT
# ==================================================

UNIT_NUMBER = 1

unit_text = load_unit(
    UNIT_NUMBER
)

print("=" * 80)

for keyword in [
    "Glossary",
    "Comprehension",
    "Vocabulary",
    "Revision of functions"
]:
    print(
        keyword,
        ":",
        unit_text.find(keyword)
    )

print("=" * 80)

read_1_block = unit_text[
    unit_text.find("Read 1"):
    unit_text.find("Read 2")
]

print("\n")
print("=" * 80)
print(read_1_block[:5000])
print("=" * 80)
# ==================================================
# PROMPT
# ==================================================

prompt = f"""
You are extracting information from a school textbook unit.

Extract the following:

1. Unit number
2. Pre-task section

3. Read 1:
   - title

4. Read 2:
   - title
   - author (if available)

5. Vocabulary section

6. Functions section

7. Writing section

8. Activities section

9. Project section

Important:
- Return only the requested sections.
- Do not summarize.
- Preserve the original wording as much as possible.
- If a section is missing, return an empty string.

TEXT:

{unit_text}
"""

# ==================================================
# EXTRACT
# ==================================================

result = structured_llm.invoke(
    prompt
)

# ==================================================
# OUTPUT
# ==================================================

print("\n===== PYDANTIC OBJECT =====\n")

print(result)

print("\n===== JSON OUTPUT =====\n")

with open("preview_output.json", "w", encoding="utf-8") as f:
    f.write(
        result.model_dump_json(
            indent=2
        )
    )

