from typing import List, Optional

from fastapi import APIRouter, Depends
from note_cast.api.rest.profile import notes
from note_cast.security.login_manager import manager

from . import bookmarks, notes

router = APIRouter(prefix="/profile")
router.include_router(notes.router, tags=["notes"])
router.include_router(bookmarks.router, tags=["bookmarks"])

@router.get("/", description="read profile info", tags=["profile"])
def read_profile(user = Depends(manager)):
    ...

@router.put("/", description="update profile info", tags=["profile"])
def update_profile(user = Depends(manager)):
    ...