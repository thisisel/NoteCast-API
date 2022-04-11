from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from note_cast.db.models import Quote, Episode, Podcast

from fastapi import status
from note_cast.api.errors import EPISODE_404, PODCAST_404, CustomHTTPException
from note_cast.schemas import NewQuoteMetadata


class DataBaseUtils:
    @classmethod
    def get_or_create_submitting_quote_parents(
        cls, data: NewQuoteMetadata, asset_public_id: str
    ):

        from note_cast.db.crud import EpisodeQuery, PodcastQuery, QuoteQuery

        from .data import DataUtils

        if (podcast := PodcastQuery.get_podcast(p_id=data.p_id)) is None:
            podcast: Podcast = PodcastQuery.create_podcast(**data.dict())

        if (
            episode := PodcastQuery.get_related_episode(podcast=podcast, e_id=data.e_id)
        ) is None:
            episode: Episode = EpisodeQuery.create_episode(**data.dict())
            episode.published_for.connect(podcast)

        quote: Quote = QuoteQuery.create_premature_quote(q_id=asset_public_id)
        quote.mentioned_on.connect(
            episode, DataUtils.compose_mentionrel_data_from_timestamp(data=data)
        )

        return quote, episode, podcast

    @classmethod
    def check_get_quote_parents(cls, quote: Quote):
        from note_cast.db.crud import EpisodeQuery, QuoteQuery

        if (
            parent_episode := QuoteQuery.get_quote_episode_or_none(quote=quote)
        ) is None:
            raise CustomHTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                category=EPISODE_404,
                detail="requested quote is orphan, episode-wise",
            )

        if (
            parent_podcast := EpisodeQuery.get_source_podcast_or_none(
                episode=parent_episode
            )
        ) is None:
            raise CustomHTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                category=PODCAST_404,
                detail="requested quote is orphan, podcast-wise",
            )

        return parent_episode, parent_podcast
