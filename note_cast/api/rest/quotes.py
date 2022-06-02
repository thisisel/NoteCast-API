from typing import Tuple, Union, List

from fastapi import APIRouter, Body, Depends, Path, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from note_cast.db.crud import (
    NoteQuery,
    QuoteQuery,
    UserQuery,
    EpisodeQuery,
    EpisodeNode,
    NoteNode,
    QuoteNode,
    PodcastNode,
    User,
    PodcastQuery
)


from note_cast.schemas import (
    Annotation,
    ApiBaseResponse,
    BaseEpisode,
    BaseNote,
    BasePodcast,
    BaseUserPydantic,
    CreateAnnotation,
    QuoteMetadata,
)
from note_cast.security.login_manager import manager
from note_cast.utils.dependencies.query_params import (
    episode_query_params,
    podcast_query_params,
    quote_query_params,
    pagination_params,
)
from note_cast.utils.dependencies.quotes import submit_quote
from note_cast.api.errors import (
    CustomHTTPException,
    QUOTE_404,
    PODCAST_404,
    EPISODE_404,
)


router = APIRouter(prefix="/quotes", tags=["quotes"])


@router.get(
    "/",
    description="read all quotes or search",
)
def search_quotes(
    quote_q_params: dict = Depends(quote_query_params),
    podcast_q_params: dict = Depends(podcast_query_params),
    episode_q_params: dict = Depends(episode_query_params),
    pagination_q_params: dict = Depends(pagination_params),
):

    skip: int = pagination_q_params.get("skip", 0)
    limit: int = pagination_q_params.get("limit", 20)

    if q_id := quote_q_params.get("q_id"):

        if quote := QuoteQuery.get_quote_by_id(q_id=q_id):
            result = quote.to_dict()
        else:
            raise CustomHTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                category=QUOTE_404,
                detail="requested quote does not exist",
            )
    elif p_id := podcast_q_params.get("p_id"):

        if podcast := PodcastQuery.get_podcast(p_id=p_id):
            result: List[dict] = podcast.quotes_list(
                to_dict=True, skip=skip, limit=limit
            )
        else:
            raise CustomHTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                category=PODCAST_404,
                detail="requested podcast does not exist",
            )

    elif e_id := episode_q_params.get("e_id"):
        if episode := EpisodeQuery.find_episode(e_id=e_id):
            result: List[dict] = episode.quotes_list(
                to_dict=True, skip=skip, limit=limit
            )
        else:
            raise CustomHTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                category=EPISODE_404,
                detail="requested episode is not registered",
            )
    else:
        result: List[dict] = QuoteQuery.get_most_annotated_quotes(
            to_dict=True, skip=skip, limit=limit
        )


    return result


# TODO rewrite dependency:submit quote for testing
@router.post(
    "/",
    description="Submit a new quote, Optionally bookmark or annotate it",
    tags=["bookmarks", "notes"],
)
def create_quote(
    quote_result: Union[Tuple[QuoteNode, EpisodeNode, PodcastNode], None] = Depends(
        submit_quote
    ),
    user: User = Depends(manager),
    annotation_data: CreateAnnotation = Body(...),
):

    if (note := annotation_data.note) is not None:
        new_note: NoteNode = NoteQuery.create_note_on_quote(
            **note.dict(), author=user, quote=quote_result[0]
        )
        new_note_pydantic: BaseNote = BaseNote(**new_note.to_dict())

    if annotation_data.bookmark:
        UserQuery.add_bookmark(user=user, quote=quote_result[0])

    author_pydantic = BaseUserPydantic(**user.to_dict())
    podcast_pydantic = BasePodcast(**quote_result[2].to_dict())
    episode_pydantic = BaseEpisode(
        **quote_result[1].to_dict(), podcast=podcast_pydantic
    )
    quote_pydantic = QuoteMetadata(
        **quote_result[0].to_dict(), episode=episode_pydantic
    )
    new_annotation_pydantic: Annotation = Annotation(
        quote=quote_pydantic,
        note=new_note_pydantic,
        bookmark=annotation_data.bookmark,
        author=author_pydantic,
    )

    result: ApiBaseResponse = ApiBaseResponse(
        message="New quote submitted successfully. Annotations attached.",
        data=new_annotation_pydantic.dict(),
    )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=jsonable_encoder(result)
    )


@router.get("/{q_id}", description="read a single quote")
def read_single_quote(
    q_id: str = Path(..., description="quote id of the requested notes")
):
    if (quote := QuoteQuery.get_quote_by_id(q_id=q_id)) is None:
        raise CustomHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            category=QUOTE_404,
            detail="requested quote does not exist",
        )
    result: ApiBaseResponse = ApiBaseResponse(
        message="Requested quote was retrieved successfully", data=quote.to_dict()
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(result)
    )




@router.get(
    "/{q_id}/notes",
    description="read all the notes about a particular quote",
    tags=["notes"],
)
def read_quote_notes_collection(
    q_id: str = Path(..., description="quote id of the requested notes"),
    author_username: str = Query(None),
):
    # TODO redirect to /api/rest/notes?q_id=q_id
    ...
