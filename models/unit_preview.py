from pydantic import BaseModel
from typing import Optional


class ReadSectionPreview(BaseModel):
    title: str
    author: Optional[str] = None

    content: str

    glossary: Optional[str] = None

    comprehension: Optional[str] = None


class UnitPreview(BaseModel):

    unit_number: int

    pre_task: str

    read_1: ReadSectionPreview

    read_2: ReadSectionPreview

    vocabulary: str

    functions: str

    writing: str

    activities: str

    project: str