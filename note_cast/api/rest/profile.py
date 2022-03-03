from typing import List, Optional

from fastapi import APIRouter, Query, Depends

from note_cast.api.rest import annotations

from . import annotations
from note_cast.schemas.notes import Note



router = APIRouter(prefix="/profile")
router.include_router(annotations.router, tags=["annotations"])

