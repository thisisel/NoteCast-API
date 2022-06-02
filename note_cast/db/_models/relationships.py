from datetime import datetime
from typing import Union
from neomodel import (
    DateTimeProperty,
    IntegerProperty,
    StructuredRel,
)
from note_cast.log.custom_logging import loguru_app_logger


class PublishRel(StructuredRel):
    air_date_db = DateTimeProperty(default_now=True)

    @property
    def air_date(self):
        return self.air_date_db

    @air_date.setter
    def air_date(self, a_date: Union[str, datetime]):
        try:
            self.air_date_db = (
                datetime.strptime(a_date, "%Y-%m-%d %H:%M:%S")
                if type(a_date) is str
                else a_date
            )
        except ValueError:
            loguru_app_logger.error(
                f"While inserting PublishRel , {a_date} format does not match with pattern"
            )
            raise ValueError


class MentionRel(StructuredRel):
    start_offset_h = IntegerProperty(required=True)
    start_offset_m = IntegerProperty(required=True)
    start_offset_s = IntegerProperty(required=True)
    end_offset_h = IntegerProperty(required=True)
    end_offset_m = IntegerProperty(required=True)
    end_offset_s = IntegerProperty(required=True)

    def to_dict(self) -> dict:
        return {
            "start_offset_h": self.start_offset_h,
            "start_offset_m": self.start_offset_m,
            "start_offset_s": self.start_offset_s,
            "end_offset_h": self.end_offset_h,
            "end_offset_m": self.end_offset_m,
            "end_offset_s": self.end_offset_s,
        }


class BaseNoteActionRel(StructuredRel):
    date = DateTimeProperty(default_now=True)


class LikeRel(BaseNoteActionRel):
    pass


class SaveRel(BaseNoteActionRel):
    pass


class CommentRel(BaseNoteActionRel):
    pass


class ReplyRel(BaseNoteActionRel):
    pass


class AnnotateRel(BaseNoteActionRel):
    date_created = DateTimeProperty(default_now=True)
    ...
