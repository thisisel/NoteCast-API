from fastapi import Query


def user_query_params(u_id: str = Query(None), username: str = Query(None)):
    return dict(u_id=u_id, username=username)
