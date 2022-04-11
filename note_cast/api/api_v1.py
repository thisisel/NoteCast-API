from fastapi import APIRouter

from .rest import auth, callback, profile, podcasts, quotes, episodes, users

rest_api_router = APIRouter(prefix="/rest")

rest_api_router.include_router(auth.router)
rest_api_router.include_router(callback.router)
rest_api_router.include_router(profile.router)
rest_api_router.include_router(users.router)
rest_api_router.include_router(podcasts.router)
rest_api_router.include_router(quotes.router)
rest_api_router.include_router(episodes.router)
