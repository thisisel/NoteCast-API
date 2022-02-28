import logging

logger = logging.getLogger(__name__)

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from neomodel import config as n4j_conf
from starlette.middleware.cors import CORSMiddleware

from note_cast.security.login_manager import manager

from .api.api_v1 import graphql_router, rest_api_router
from .core.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME, debug=settings.debug, version=settings.VERSION
    )

    # n4j_conf.DATABASE_URL = settings.DB_URI
    import note_cast.db

    manager.useRequest(app)

    app.include_router(rest_api_router, prefix=settings.API_ROOT_PREFIX)
    app.include_router(
        graphql_router, prefix=settings.API_ROOT_PREFIX + "/graphql", tags=["graphql"]
    )

    return app


app = create_app()

# TODO add middleware allowed hosts
def _add_middleware(app: FastAPI) -> None:

    # TODO add catch permission middleware
    from .core.middlewares import catch_Permissionerror_middleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# TODO customize excpetions
# def _add_exception_handler(app: FastAPI):
# app.add_exception_handler(NotFound, notfound_error_handler)
# app.add_exception_handler(HTTPException, http_error_handler)
# app.add_exception_handler(InternalError, internal_error_handler)
# app.add_exception_handler(RequestValidationError, http422_error_handler)
# app.add_exception_handler(Forbidden, forbidden_error_handler)
# app.add_exception_handler(NotAllowed, notallowed_error_handler)
# app.add_exception_handler(UnAuthorized, unauthorized_error_handler)


# def _get_index_page(debug: bool):
