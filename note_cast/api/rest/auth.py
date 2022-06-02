from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from neomodel.exceptions import UniqueProperty
from note_cast.api.errors import CustomHTTPException
from note_cast.app import manager as login_manager
from note_cast.db.crud import User, load_user
from note_cast.log.custom_logging import loguru_app_logger
from note_cast.schemas import ApiBaseResponse, ApiErrorResponse, BaseUserPydantic, RestLoginSuccessResp, UserPydantic
router = APIRouter(tags=["auth"])


@router.post(
    "/login",
    responses={
        200: {"model": RestLoginSuccessResp},
        401: {"model": ApiErrorResponse},
    },
    response_model_exclude_unset=True,
)
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    if not (user := load_user(email)):
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong username",
            category="Invalid credentials",
        )

    elif not user.verify_password(password):
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password",
            category="Invalid credentials",
        )

    user_pydantic = BaseUserPydantic(
        u_id=user.u_id, username=user.username, email=email
    )
    access_token = login_manager.create_access_token(data={"sub": email})

    # TODO add no cache header
    result = RestLoginSuccessResp(
        status=True,
        message="Successful login",
        user=user_pydantic,
        access_token=access_token,
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(result)
    )


@router.post(
    "/register",
    responses={
        201: {"model": ApiBaseResponse},
        400: {"model": ApiErrorResponse},
    },
    response_model_exclude_unset=True,
)
def register(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    try:
        new_user: User = User(username=email, email=email, password=password).save()
        new_user_pydantic = UserPydantic(
            u_id=new_user.u_id,
            username=new_user.username,
            email=new_user.email,
            disabled=new_user.disabled,
            joined_date=new_user.joined_date,
        )

    except UniqueProperty as exc:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A user with {email} already exists!",
        )

    except Exception as ex:
        loguru_app_logger.exception(ex)
        raise CustomHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    result: ApiBaseResponse = ApiBaseResponse(
        message="Successful registration", data=new_user_pydantic.dict()
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=jsonable_encoder(result)
    )
