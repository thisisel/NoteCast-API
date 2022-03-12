from fastapi import APIRouter, Depends, Path
from note_cast.core.dependencies import podcast_query_params, user_query_params

router = APIRouter(prefix="/users")


@router.get("/", description="search for users", tags=["users"])
def read_users(user=Depends(user_query_params)):
    ...


@router.get(
    "/{username}", description="read information about a single user", tags=["users"]
)
def read_user(username: str = Path(...)):
    ...


@router.put(
    "/{username}",
    description="update with a ['follow'] reaction towards a user",
    tags=["users"],
)
def update_follow_user(username: str = Path(...)):
    ...


@router.get(
    "/{username}/notes",
    description="read all the notes written by the user with {'username'}",
    tags=["notes"],
)
def read_user(
    username: str = Path(...), podcast_q_params: dict = Depends(podcast_query_params)
):
    ...
