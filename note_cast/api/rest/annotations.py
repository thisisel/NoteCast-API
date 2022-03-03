from typing import List, Optional
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from note_cast.core.dependencies import fetch_quote
from note_cast.db.crud import QuoteNode
from note_cast.schemas import QuoteMetadata, QuotePydantic
from note_cast.schemas.response import ApiBaseResponse
from note_cast.security.login_manager import manager


router = APIRouter(prefix="/annotations")

@router.get("/")
def read_notes(n_id : Optional[str], user = Depends(manager)):
    ...


@router.post("/")
def create_note(quote_node : QuoteNode = Depends(fetch_quote)):
    detail = QuotePydantic(q_id=quote_node.q_id, transcript=quote_node.transcript, visible=quote_node.visible)
    content = ApiBaseResponse(status=True, message="Quote was fetched", detail=detail)
    return JSONResponse(status_code=201, content=jsonable_encoder(content.dict()))
    


@router.put("/")
def update_note(user = Depends(manager)):
    ...