from fastapi import APIRouter, Depends
from note_cast.schemas import ApiBaseResponse, ApiErrorResponse, BaseEpisode
from note_cast.utils.dependencies.query_params import (
    episode_query_params,
    podcast_query_params,
)
from note_cast.services.podchaser_api import (
    PodchaserPodcastGQueries,
    PodchaserEpisodeGQueries,
)

router = APIRouter(prefix="/episodes", tags=["episodes"])


@router.get(
    "/",
    response_model=ApiBaseResponse,
    response_model_exclude_none=True,
)
def search_episode(
    podcast_q_params: dict = Depends(podcast_query_params),
    episode_q_params: dict = Depends(episode_query_params),
):

    if (p_id := podcast_q_params.get("p_id")) is not None:
        (
            podcast,
            episodes,
            paginator_info,
        ) = PodchaserPodcastGQueries.fetch_podcast_related_episodes(
            p_id=p_id,
            episode_search_term=episode_q_params.get("e_title"),
            from_air_date=episode_q_params.get("from_Air_date"),
            to_air_date=episode_q_params.get("to_air_date"),
        )
        result = dict(podcast=podcast, episodes=episodes, paginator_info=paginator_info)

    elif (e_id := episode_q_params.get("e_id")) is not None:
        result: BaseEpisode = PodchaserEpisodeGQueries.fetch_single_episode(e_id=e_id)

    elif (e_title := episode_q_params.get("e_title")) is not None:
        result: BaseEpisode = PodchaserEpisodeGQueries.search_episode(term=e_title)

    return ApiBaseResponse(
        message="Search episode query completed successfully", data=result
    )


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
    result: BaseEpisode = PodchaserEpisodeGQueries.fetch_single_episode(e_id=e_id)

    return ApiBaseResponse(
        message="Episode retrived successfully", data=result
    )


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
