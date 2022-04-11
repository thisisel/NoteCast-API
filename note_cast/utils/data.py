from note_cast.schemas import (
    EpisodeTimestamp,
    NewQuoteMetadata,
    QuoteMetadata,
    BaseEpisode,
    BasePodcast,
)


class DataUtils:
    @classmethod
    def compose_mentionrel_data_from_timestamp(cls, data: NewQuoteMetadata):

        start: EpisodeTimestamp = data.start_timestamp
        end: EpisodeTimestamp = data.end_timestamp

        return {
            "start_offset_h": start.hour,
            "start_offset_m": start.minute,
            "start_offset_s": start.seconds,
            "end_offset_h": end.hour,
            "end_offset_m": end.minute,
            "end_offset_s": end.seconds,
        }

    @classmethod
    def compose_quote_metadata_pydantic(cls, quote, parent_episode, parent_podcast)-> QuoteMetadata:

        podcast_pydantic = BasePodcast(**parent_podcast.to_dict())
        episode_pydantic = BaseEpisode(**parent_episode.to_dict(), podcast=podcast_pydantic)
       
        result = QuoteMetadata(
            **quote.to_dict(), episode=episode_pydantic
        )

        return result
