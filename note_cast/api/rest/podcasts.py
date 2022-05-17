from typing import List, Tuple

from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from note_cast.schemas import ApiBaseResponse, ApiErrorResponse, BasePodcast
from note_cast.services.podchaser_api import PodchaserPodcastGQueries


router = APIRouter(prefix="/podcasts", tags=["podcast"])


@router.get(
    "/",
    description="search for a podcast based on title",
    response_model=ApiBaseResponse,
    response_model_exclude_unset=True,
)
def search_podcast(term: str):

    # results: List[BasePodcast] = PodchaserPodcast.search_podcast_term(term=term)
    results, pagination_info = PodchaserPodcastGQueries.search_podcast_term(term=term)
    return ApiBaseResponse(
        message="Search podcast query completed successfully", data=results
    )


@router.get(
    "/{p_id}/",
    responses={
        200: {"model": ApiBaseResponse},
        404: {"model": ApiErrorResponse},
    },
    description=" read a particular podcast with {p_id}",
)
def read_single_podcast(p_id: str):

    result: BasePodcast = PodchaserPodcast.get_single_podcast(p_id=p_id)
    # podcast = PodcastQuery.search_podcasts(p_id=p_id)
    # if len(podcast) == 0:
    #     raise CustomHTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         category=PODCAST_404,
    #         detail=f"podcast with p_id = {p_id} does not exist",
    #     )

    # result: BasePodcast = BasePodcast(**podcast[0].to_dict())
    return ApiBaseResponse(message="Podcast retrieved successfully", data=result)


@router.get(
    "/{p_id}/episodes/",
    description="Read a list of podcast episodes",
    response_class=RedirectResponse,
    status_code=status.HTTP_302_FOUND,
)
def read_podcast_episodes_collection(p_id: str, request: Request):

    # TODO redirect to /api/rest/episodes?p_id=p_id
    next_endpoint = request.url_for("search_episode")
    query_params = f"?p_id={p_id}"
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
