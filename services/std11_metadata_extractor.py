import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the main project folder to Python's path so it can find 'models'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# NEW: Import from langchain_openai instead of google
from langchain_openai import ChatOpenAI

from models.metadata_schema import (
    ReadMetadata
)

load_dotenv()

# NEW: Initialize OpenAI's gpt-4o-mini model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

structured_llm = (
    llm.with_structured_output(
        ReadMetadata
    )
)

def extract_std11_metadata(
    read_block: str
) -> ReadMetadata:

    prompt = f"""
You are extracting metadata from a Gujarat Board
Std 11 English textbook lesson.

Extract:

1. Lesson title
2. Author name (if present)

Rules:

- Ignore "Read 1", "Read 2", "Read 3"
- Ignore "Glossary"
- Ignore "Comprehension"
- Author may be absent
- Return only structured output

TEXT:

{read_block[:4000]}
"""

    return structured_llm.invoke(
        prompt
    )