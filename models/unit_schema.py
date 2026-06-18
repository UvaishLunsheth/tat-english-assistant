from pydantic import BaseModel
from typing import Optional


class ReadSection(BaseModel):
    title: str
    author: Optional[str] = None

    content: str
    glossary: str
    comprehension: str


class UnitSchema(BaseModel):
    unit_number: int

    pre_task: Optional[str] = None

    read_1: ReadSection

    read_2: Optional[ReadSection] = None

    vocabulary: Optional[str] = None

    functions: Optional[str] = None

    writing: Optional[str] = None

    activities: Optional[str] = None

    project: Optional[str] = None