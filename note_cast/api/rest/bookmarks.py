from typing import Union

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from note_cast.core.dependencies import fetch_quote
from note_cast.security.login_manager import manager
from note_cast.db.crud import QuoteNode
from note_cast.schemas import ApiBaseResponse, QuotePydantic

router = APIRouter(prefix="/bookmarks")


@router.get("/", description="read all the quotes which are bookmarked")
def read_bookmarks(user=Depends(manager)):
    ...


@router.post("/", description="create a new bookmark on a quote")
def create_bookmark(
    result: Union[QuoteNode, ApiBaseResponse, None] = Depends(fetch_quote),
    # user=Depends(manager),
):

    if isinstance(result, QuoteNode):

        detail = QuotePydantic(
            q_id=result.q_id,
            transcript=result.transcript,
            visible=result.visible,
        )
        status_code = status.HTTP_200_OK
        content = ApiBaseResponse(
            status=True, message="Quote was fetched", detail=detail
        )

    elif isinstance(result, ApiBaseResponse) and result.status:

        status_code = status.HTTP_202_ACCEPTED
        content = ApiBaseResponse(status=True, message=result.message)

    else:

        status_code = status.HTTP_404_NOT_FOUND
        content = ApiBaseResponse(status=False, message="invalid q_id")

    return JSONResponse(
        status_code=status_code, content=jsonable_encoder(content.dict())
    )


@router.delete("/", description="delete a bookmark")
def delete_bookmark(user=Depends(manager)):
    ...
