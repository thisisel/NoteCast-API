import os
import secrets
from functools import lru_cache
from typing import Union

from dotenv import load_dotenv
from pydantic import BaseSettings, HttpUrl
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

config = Config(".env")


class Settings(BaseSettings):
    PROJECT_NAME: str = "Note Cast API"
    VERSION: str = "0.0.1"
    API_ROOT_PREFIX: str = "/api"

    SECRET_KEY: Secret = config(
        "SECRET_KEY", cast=Secret, default=secrets.token_urlsafe(32)
    )

    FASTAPI_ENV: str = config("FASTAPI_ENV")

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    ALLOWED_HOSTS: Union[CommaSeparatedStrings, str] = config(
        "ALLOWED_HOSTS",
        cast=CommaSeparatedStrings,
        default="",
    )

    NEO4J_USERNAME: str = config("NEO4J_USERNAME")
    NEO4J_PASSWORD: str = config("NEO4J_PASSWORD")

    REDIS_URL: str = config("REDIS_URL", default="redis://localhost:6379")

    CLOUDINARY_CLOUD_NAME : str = config("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY : str = config("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET : str = config("CLOUDINARY_API_SECRET")
    LOCALHOST_PUBLIC_IP : HttpUrl = config("LOCALHOST_PUBLIC_IP")
    CLOUDINARY_NOTIFICATION_URL : HttpUrl = f"{LOCALHOST_PUBLIC_IP}/api/rest/callback/cloudinary/upload/"

    if FASTAPI_ENV == "development":
        debug: bool = True
        DB_URI: str = f"bolt://{NEO4J_USERNAME}:{NEO4J_PASSWORD}@localhost:7687"

    elif FASTAPI_ENV == "testing":
        debug: bool = True
        # DB_URI

    elif FASTAPI_ENV == "production":
        debug: bool = False
        DB_URI: str = config("AURORA_URI")
    else:
        # TODO raise error
        print(f"Invalid FASTAPI_ENV {FASTAPI_ENV}")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
