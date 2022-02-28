from turtle import st
from . import QuoteMetadata, EpisodeTimestamp
def quote_timestamp_to_mentionrel(data : QuoteMetadata):
    
    start : EpisodeTimestamp = data.start_timestamp
    end : EpisodeTimestamp = data.end_timestamp

    return {
        'start_offset_h' : start.hour,
        'start_offset_m' : start.minute,
        'start_offset_s' : start.seconds,
        'end_offset_h' : end.hour,
        'end_offset_m' : end.minute,
        'end_offset_s' : end.seconds,
    }