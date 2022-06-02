from typing import List, Optional
from fastapi import APIRouter, Body, Depends, Path, Query, status
from note_cast.api.errors import BOOKMARK_QUOTE_404, CustomHTTPException
from note_cast.db.crud import UserQuery, QuoteNode, QuoteQuery
from note_cast.schemas import (
    ApiBaseResponse,
    ApiErrorResponse,
    QuoteMetadata,
    Annotation,
)
from note_cast.schemas.user import BaseUserPydantic
from note_cast.security.login_manager import manager
from note_cast.utils import DataBaseUtils, DataUtils
from note_cast.utils.dependencies.core import pagination_params
from note_cast.utils.dependencies.podcasts import podcast_query_params
from note_cast.utils.dependencies.episodes import episode_query_params


router = APIRouter(prefix="/bookmarks")


@router.get("/", description="read all the quotes which are bookmarked")
def read_bookmarks(
    user=Depends(manager),
    pagination_params: dict = Depends(pagination_params),
    podcast_q_params: dict = Depends(podcast_query_params),
    episode_q_params: dict = Depends(episode_query_params),
    q_id: Optional[str] = Query(None),
):
    bookmarks: List[QuoteNode] = UserQuery.get_user_bookmarks(
        user=user, **pagination_params
    )

    results: List[QuoteMetadata] = []
    if bookmarks is not None:

        for quote in bookmarks:
            parent_episode, parent_podcast = DataBaseUtils.check_get_quote_parents(
                quote=quote
            )

            result: QuoteMetadata = DataUtils.compose_quote_metadata_pydantic(
                quote=quote,
                parent_episode=parent_episode,
                parent_podcast=parent_podcast,
            )

            results.append(result)

    return ApiBaseResponse(
        message="List of bookmarks retrived successfully", data=results
    )


@router.delete(
    "/{q_id}",
    description="delete a bookmarked quote",
    responses={
        200: {"model": ApiBaseResponse},
        404: {"model": ApiErrorResponse},
    },
    response_model_exclude_unset=True,
)
def delete_bookmark(q_id: str = Path(...), user=Depends(manager)):
    if (deleted_bookmark := UserQuery.delete_bookmark(q_id=q_id, user=user)) is None:
        raise CustomHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            category=BOOKMARK_QUOTE_404,
            detail="bookmarked quote does not exist",
        )
    (
        deleted_quote_episode,
        deleted_quote_podcast,
    ) = DataBaseUtils.check_get_quote_parents(quote=deleted_bookmark)

    result: QuoteMetadata = DataUtils.compose_quote_metadata_pydantic(
        quote=deleted_bookmark,
        parent_episode=deleted_quote_episode,
        parent_podcast=deleted_quote_podcast,
    )

    response = ApiBaseResponse(message="Quote was deleted successfully", data=result)

    return response


@router.post(
    "/",
    description="bookmark an existing quote",
    responses={
        201: {"model": ApiBaseResponse},
        404: {"model": ApiErrorResponse},
    },
    response_model=ApiBaseResponse,
    response_model_exclude_unset=True,
)
def create_bookmark(
    q_id: str = Body(..., description="quote to be bookmarked"), user=Depends(manager)
):
    if (quote := QuoteQuery.get_quote_by_id(q_id=q_id)) is not None:
        UserQuery.add_bookmark(user=user, quote=quote)

    author_pydantic = BaseUserPydantic(**user.to_dict())
    quote_pydantic = QuoteMetadata(**quote.to_dict())
    result = Annotation(author=author_pydantic, quote=quote_pydantic, bookmark=True)

    return ApiBaseResponse(message="Quote was bookmarked successfully", data=result)
