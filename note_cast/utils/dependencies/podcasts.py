from typing import Optional

def podcast_query_params(
    p_id: Optional[str] = None,
    p_title: Optional[str] = None,
):
    return {"p_id": p_id, "p_title": p_title}