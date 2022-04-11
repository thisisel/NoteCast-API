from fastapi import APIRouter, Depends, Query
from note_cast.schemas import ApiBaseResponse, ApiErrorResponse, BaseEpisode
from  note_cast.utils.dependencies.query_params import episode_query_params, podcast_query_params

router = APIRouter(prefix="/episodes",  tags=["episodes"])


@router.get("/")
def search_episode(
    podcast_q_params: dict = Depends(podcast_query_params),
    episode_q_params: dict = Depends(episode_query_params),
):
    results = [
        {
            "e_id": "47443",
            "e_title": "The Benefits of Mixed Emotions",
            "e_listennotes_url": "https://melodic-erosion.net",
        },
    ]
    # if p_id -> retrive podcast episodes or 404 if podcast does not exist
    # if e_id -> retrive single episode otr nothing
    return ApiBaseResponse(message="Search episode query completed successfully", data=results)


@router.get(
    "/{e_id}/",
    responses={
        200: {"model": ApiBaseResponse},
        404: {"model": ApiErrorResponse},
    },
    description=" read a particular episode with {e_id}",
)
def read_single_episode(e_id: str):
    result: BaseEpisode = BaseEpisode()
    response = ApiBaseResponse(
        message="episode retrieved successfully", data=result.dict()
    )
    ...


@router.get(
    "/{e_id}/quotes",
    description="Read a list of quotes mentioned on an specific episode",
)
def read_episode_quotes_collection(e_id: str):
    # TODO redirect to /api/rest/quotes?e_id=e_id
    ...


@router.get(
    "/{e_id}/quotes",
    description="Read a list of notes on an specific episode",
)
def read_episode_notes_collection(e_id: str):
    # TODO redirect to /api/rest/notes?e_id=e_id
    ...
