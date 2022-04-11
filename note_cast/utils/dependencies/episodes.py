from typing import Optional
def episode_query_params(
    e_id: Optional[str] = None,
    e_title: Optional[str] = None,
):
    return {"e_id": e_id, "e_title": e_title}