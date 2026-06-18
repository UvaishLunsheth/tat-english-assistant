from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from models.metadata_schema import ReadMetadata

load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

structured_llm = llm.with_structured_output(
    ReadMetadata
)


def extract_metadata(
    read_block: str
) -> ReadMetadata:

    prompt = f"""
You are extracting metadata from a school textbook lesson.

Extract:

1. Lesson title
2. Author name (if present)

Return only structured data.

TEXT:

{read_block[:4000]}
"""

    return structured_llm.invoke(
        prompt
    )