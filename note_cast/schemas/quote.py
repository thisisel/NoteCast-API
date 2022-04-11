from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional

from .user import BaseUserPydantic

if TYPE_CHECKING:
    from .annotation import BaseNote
    from .episode import BaseEpisode

from pydantic import BaseModel, Field, HttpUrl


class Quote(BaseModel):
    q_id: str
    transcript: Optional[str]
    visible: bool = True


class EpisodeTimestamp(BaseModel):
    hour: int = Field(0, ge=0, le=4)
    minute: int = Field(0, ge=0, le=60)
    seconds: int = Field(0, ge=0, le=60)


class NewQuoteMetadata(BaseModel):

    start_timestamp: EpisodeTimestamp
    end_timestamp: EpisodeTimestamp

    audio_url: HttpUrl
    e_id: str
    e_title: str
    length_s: int

    p_id: str
    p_title: str


class BaseQuote(BaseModel):
    q_id: str
    transcript: str


class QuoteMetadata(BaseQuote):
    episode: Optional[BaseModel] = None
    attachments: Optional[List[BaseModel]] = None
    bookmarkers: Optional[List[BaseUserPydantic]] = None


class MentionRel(BaseModel):
    start_offset_h: int = Field(0, ge=0, le=4)
    start_offset_m: int = Field(0, ge=0, le=60)
    start_offset_s: int = Field(0, ge=0, le=60)

    end_offset_h: int = Field(0, ge=0, le=4)
    end_offset_m: int = Field(0, ge=0, le=60)
    end_offset_s: int = Field(0, ge=0, le=60)
