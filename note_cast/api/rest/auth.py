from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from note_cast.app import manager as login_manager
from note_cast.db.crud.user import load_user
from note_cast.db.models import User

router = APIRouter()


@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    if not (user := load_user(email)):
        raise InvalidCredentialsException

    elif not user.verify_password(password):
        raise InvalidCredentialsException

    access_token = login_manager.create_access_token(data={"sub": email})
    return {"token": access_token}


@router.post("/register")
def register(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    if (user := load_user(email)) is not None:
        # TODO api error msg schema
        return {"err_msg": "user with this email already exists"}

    try:
        new_user: User = User(username=email, email=email, password=password).save()

    except Exception as ex:
        print(ex)
        return {"exp": "ex"}

    return {"msg": "success"}
