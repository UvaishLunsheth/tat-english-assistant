from pydantic import BaseModel
from typing import Optional


class ReadSection(BaseModel):

    title: str

    author: Optional[str] = None

    content: str

    glossary: str

    comprehension: str


class Std11UnitSchema(BaseModel):

    unit_number: int

    pre_task: Optional[str] = None

    reads: list[ReadSection]

    vocabulary: Optional[str] = None

    functions: Optional[str] = None

    writing: Optional[str] = None

    activities: Optional[str] = None

    project: Optional[str] = None