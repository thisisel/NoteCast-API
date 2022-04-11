from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, Field

from .user import BaseUserPydantic
if TYPE_CHECKING:
    from .quote import QuoteMetadata


class CreateNote(BaseModel):
    text: str = Field(..., min_length=50, max_length=450)
    is_public: bool = True


class CreateAnnotation(BaseModel):
    note: Optional[CreateNote] = None
    bookmark: Optional[bool] = False


class BaseNote(CreateNote):
    n_id: str
    author: Optional[BaseUserPydantic] = None
    quote: Optional[BaseModel] = None


class SingleNote(BaseNote):
    author: Optional[BaseUserPydantic]


class NoteCollection(BaseModel):
    author: BaseUserPydantic
    notes: List[BaseNote]


class Annotation(BaseModel):
    author: BaseUserPydantic
    quote: BaseModel
    note: Optional[BaseModel] = None
    bookmark: Optional[bool] = False

