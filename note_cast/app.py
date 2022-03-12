import logging

logger = logging.getLogger(__name__)

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from note_cast.security.login_manager import manager

from .api.api_v1 import graphql_router, rest_api_router
from .core.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME, debug=settings.debug, version=settings.VERSION
    )

    import note_cast.db

    manager.useRequest(app)

    app.include_router(rest_api_router, prefix=settings.API_ROOT_PREFIX)
    app.include_router(
        graphql_router, prefix=settings.API_ROOT_PREFIX + "/graphql", tags=["graphql"]
    )

    app.add_api_route(
        path="/",
        endpoint=lambda: dict(status=True, project=settings.PROJECT_NAME, version=settings.VERSION),
        status_code=200,
        methods=["get"],
        include_in_schema=False,
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