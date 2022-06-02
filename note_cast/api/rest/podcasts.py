from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import RedirectResponse
from note_cast.schemas import ApiBaseResponse, ApiErrorResponse, BasePodcast
from note_cast.services.podchaser_api import PodchaserPodcastGQueries
from note_cast.utils.dependencies.query_params import (
    episode_query_params,
    paginator_info,
)


router = APIRouter(prefix="/podcasts", tags=["podcast"])


@router.get(
    "/",
    response_model=ApiBaseResponse,
    response_model_exclude_none=True,
    description="search for a podcast based on title",
)
def search_podcast(term: str):

    podcasts, pagination_info = PodchaserPodcastGQueries.search_podcast_term(term=term)
    results: dict = dict(podcasts=podcasts, paginationInfo=pagination_info)

    return ApiBaseResponse(
        message="Search podcast query completed successfully", data=results
    )


@router.get(
    "/{p_id}/",
    responses={
        200: {"model": ApiBaseResponse},
        404: {"model": ApiErrorResponse},
    },
    response_model=ApiBaseResponse,
    response_model_exclude_none=True,
    description="read a particular podcast with {p_id}",
)
def read_single_podcast(p_id: str):

    result: BasePodcast = PodchaserPodcastGQueries.fetch_single_podcast(p_id=p_id)

    return ApiBaseResponse(message="Podcast retrieved successfully", data=result)


@router.get(
    "/{p_id}/episodes/",
    description="Read a list of podcast episodes",
    response_class=RedirectResponse,
    status_code=status.HTTP_302_FOUND,
)
def read_podcast_episodes_collection(
    p_id: str,
    request: Request,
    episode_q_params: dict = Depends(episode_query_params),
    paginator: dict = Depends(paginator_info),
):

    next_endpoint = request.url_for("search_episode")
    query_params = f"?p_id={p_id}"

    if (e_title := episode_q_params.get('e_title')):
        query_params += f'&e_title={e_title}'
    if (from_air_date := episode_q_params.get('from_air_date')):
        query_params += f'&from_air_date={from_air_date}'
    if (to_air_date := episode_q_params.get('to_air_date')):
        query_params += f'&to_air_date={to_air_date}'

    next_url = next_endpoint + query_params

    return next_url


@router.get(
    "/{p_id}/quotes/",
    description="Read a list of quotes mentioned on the podcast",
    response_class=RedirectResponse,
    status_code=status.HTTP_302_FOUND,
)
def read_podcast_quotes_collection(p_id: str, request: Request):
    # TODO redirect to /api/rest/quotes?p_id=p_id
    next_endpoint = request.url_for("search_quotes")
    query_params = f"?p_id={p_id}"
    next_url = next_endpoint + query_params

    return next_url


@router.get(
    "/{p_id}/notes/",
    description="Read a list of notes related to the podcast",
    response_class=RedirectResponse,
    status_code=status.HTTP_302_FOUND,
)
def read_podcast_notes_collection(p_id: str, request: Request):
    # TODO redirect to /api/rest/notes?p_id=p_id
    next_endpoint = request.url_for("search_notes")
    query_params = f"?p_id={p_id}"
    next_url = next_endpoint + query_params

    return next_url
