from typing import List, Optional
from fastapi import APIRouter, Depends
from note_cast.security.login_manager import manager


router = APIRouter(prefix="/notes")

@router.get("/notes")
def read_notes(n_id : Optional[str], user = Depends(manager)):
    ...


@router.post("/notes")
def create_note(user = Depends(manager)):
    ...


@router.put("/notes")
def update_note(user = Depends(manager)):
    ...