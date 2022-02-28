from typing import List, Optional

from fastapi import APIRouter, Query, Depends

from note_cast.api.rest import notes

from . import notes
from note_cast.schemas.notes import Note



router = APIRouter(prefix="/my")
router.include_router(notes.router, tags=["notes"])

