from pydantic import BaseModel
from typing import Optional


class ReadMetadata(BaseModel):
    title: str
    author: Optional[str] = None