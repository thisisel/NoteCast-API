from typing import List, Optional

from fastapi import APIRouter, Depends
from note_cast.api.rest import annotations
from note_cast.security.login_manager import manager

from . import annotations, bookmarks

router = APIRouter(prefix="/profile")
router.include_router(annotations.router, tags=["annotations"])
router.include_router(bookmarks.router, tags=["bookmarks"])

@router.get("/", description="read profile info", tags=["profile"])
def read_profile(user = Depends(manager)):
    ...

@router.put("/", description="update profile info", tags=["profile"])
def update_profile(user = Depends(manager)):
    ...