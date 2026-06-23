from pydantic import BaseModel
from typing import Optional


class ReadPreview(BaseModel):

    title: str

    author: Optional[str] = None

    content: str

    glossary: Optional[str] = None

    comprehension: Optional[str] = None


class Std11UnitPreview(BaseModel):

    unit_number: int

    pre_task: str

    reads: list[ReadPreview]

    vocabulary: str

    functions: str

    writing: str

    activities: str

    project: Optional[str] = None