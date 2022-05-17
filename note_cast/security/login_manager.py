from functools import lru_cache

from fastapi_login import LoginManager
from note_cast.core.settings import settings
from note_cast.api.errors import InvalidCredentialsExc


@lru_cache()
def get_login_manager():
    manager = LoginManager(
        secret=str(settings.SECRET_KEY),
        token_url="/api/rest/login",
        custom_exception=InvalidCredentialsExc,
    )
    return manager


manager = get_login_manager()
