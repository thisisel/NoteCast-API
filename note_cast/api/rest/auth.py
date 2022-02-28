from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from note_cast.app import manager as login_manager
from note_cast.db.crud.user import load_user
from note_cast.db.models import User
from note_cast.schemas.response import (
    RestRegisterSuccessResp,
    RestLoginSuccessResp,
    UserPydantic,
    BaseUserPydantic,
    ApiErrorResponse,
)

router = APIRouter()


@router.post("/login", 
    responses={
        201: {"model": RestLoginSuccessResp},
        400: {"model": ApiErrorResponse},
    },
    )
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    if not (user := load_user(email)):
        raise InvalidCredentialsException

    elif not user.verify_password(password):
        raise InvalidCredentialsException

    user_pydantic = BaseUserPydantic(id=user.u_id, username=user.username, email=email)
    access_token = login_manager.create_access_token(data={"sub": email})

    return RestLoginSuccessResp(
        status=True, message="Successful login", user=user_pydantic, token=access_token
    )


@router.post("/register",     
    responses={
        200: {"model": RestRegisterSuccessResp},
        400: {"model": ApiErrorResponse},
    },)
def register(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    if (user := load_user(email)) is not None:
        return ApiErrorResponse(
            category="user_exists", message=f"A user with {email} already exists!"
        )

    try:
        new_user: User = User(username=email, email=email, password=password).save()
        new_user_pydantic = UserPydantic(
            id=new_user.u_id,
            username=new_user.username,
            email=new_user.email,
            disabled=new_user.disabled,
            joined_date=new_user.joined_date,
        )

    except Exception as ex:
        print(ex)
        return {"exp": "ex"}

    return RestRegisterSuccessResp(
        status=True, message="Successful Registration", user=new_user_pydantic
    )
