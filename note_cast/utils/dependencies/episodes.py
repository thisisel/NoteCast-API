from typing import Optional
from datetime import datetime


def episode_query_params(
    e_id: Optional[str] = None,
    e_title: Optional[str] = None,
    from_air_date: Optional[datetime] = None,
    to_air_date: Optional[datetime] = None,
):
    return {
        "e_id": e_id,
        "e_title": e_title,
        "from_air_date": from_air_date.strftime("%Y-%m-%d %H:%M:%S"),
        "to_air_date": to_air_date.strftime("%Y-%m-%d %H:%M:%S"),
    }
