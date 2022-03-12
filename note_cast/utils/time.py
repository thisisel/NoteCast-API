class TimeUtils:

    from note_cast.schemas.podcast import EpisodeTimestamp

    @staticmethod
    def timestamp_to_millies(ep_timestamp: EpisodeTimestamp) -> int:
        h_millies = ep_timestamp.hour * 3600000
        m_millies = ep_timestamp.minute * 60000
        s_millies = ep_timestamp.seconds * 1000

        return h_millies + m_millies + s_millies

    @staticmethod
    def timestamp_to_seconds(ep_timestamp: EpisodeTimestamp) -> int:
        h_seconds = ep_timestamp.hour * 3600
        m_seconds = ep_timestamp.minute * 60

        return h_seconds + m_seconds + ep_timestamp.seconds

    @staticmethod
    def seconds_to_millies(seconds: int) -> int:
        return seconds * 1000