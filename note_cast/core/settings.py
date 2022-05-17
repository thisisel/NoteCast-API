import os
import secrets
from functools import lru_cache
from typing import Any, List, Union

from dotenv import load_dotenv
from pydantic import BaseModel, BaseSettings, HttpUrl
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

config = Config(".env")


class CloudinaryConfig:
    CLOUD_NAME: str = config("CLOUDINARY_CLOUD_NAME")
    API_KEY: str = config("CLOUDINARY_API_KEY")
    API_SECRET: str = config("CLOUDINARY_API_SECRET")
    LOCALHOST_PUBLIC_IP: HttpUrl = config("LOCALHOST_PUBLIC_IP")
    NOTIFICATION_URL: HttpUrl = (
        f"{LOCALHOST_PUBLIC_IP}/api/rest/callback/cloudinary/upload/"
    )
    FOLDER: str = config("CLOUDINARY_FOLDER", default="listennotes_segments")
    RAW_CONVERT: bool = config("CLOUDINARY_RAW_CONVERT", default=False)
    ASYNC_UPLOAD: bool = config("CLOUDINARY_ASYNC_UPLOAD", default=True)

class PodchaserConfig:
    TOKEN : str = config("PODCHASER_TOKEN")
    BASE_URL : HttpUrl = config("PODCHASER_BASE_URL")
    HEADERS : dict = {
        "Authorization": "Bearer " + TOKEN,
        "Content-Type" : "application/json"
    }
    BASE_GQ_PATH : HttpUrl = BASE_URL + "graphql"

    FASTAPI_ENV: str = config("FASTAPI_ENV")
    
    if FASTAPI_ENV == "development":
        PODCHASER_SECRET : Secret = config("PODCHASER_DEV_SECRET", cast=Secret)
        PODCHASER_KEY : str = config("PODCHASER_DEV_KEY")

    elif FASTAPI_ENV == "testing":
        raise EnvironmentError

    elif FASTAPI_ENV == "production":
        PODCHASER_SECRET : Secret = config("PODCHASER_PRO_SECRET", cast=Secret)
        PODCHASER_KEY : str = config("PODCHASER_PRO_KEY")
    else:
        raise Exception(f"Invalid FASTAPI_ENV")


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
    REDIS_LISTEN: List[str] = ["cpu", "network", "hybrid"]

    #TODO create CloudinarySettings
    CLOUDINARY_CLOUD_NAME: str = config("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY: str = config("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET: str = config("CLOUDINARY_API_SECRET")
    LOCALHOST_PUBLIC_IP: HttpUrl = config("LOCALHOST_PUBLIC_IP")
    CLOUDINARY_NOTIFICATION_URL: HttpUrl = (
        f"{LOCALHOST_PUBLIC_IP}/api/rest/callback/cloudinary/upload/"
    )
    CLOUDINARY_FOLDER: str = config("CLOUDINARY_FOLDER", default="listennotes_segments")
    CLOUDINARY_RAW_CONVERT: bool = config("CLOUDINARY_RAW_CONVERT", default=False)
    CLOUDINARY_ASYNC_UPLOAD: bool = config("CLOUDINARY_ASYNC_UPLOAD", default=True)

    PODCHASER_TOKEN : str = config("PODCHASER_TOKEN")
    PODCHASER_BASE_URL : HttpUrl = config("PODCHASER_BASE_URL")

    if FASTAPI_ENV == "development":
        debug: bool = True
        DB_URI: str = f"bolt://{NEO4J_USERNAME}:{NEO4J_PASSWORD}@localhost:7687"
        PODCHASER_SECRET : Secret = config("PODCHASER_DEV_SECRET", cast=Secret)
        PODCHASER_KEY : str = config("PODCHASER_DEV_KEY")

    elif FASTAPI_ENV == "testing":
        debug: bool = True
        # DB_URI

    elif FASTAPI_ENV == "production":
        debug: bool = False
        DB_URI: str = config("AURORA_URI")
        PODCHASER_SECRET : Secret = config("PODCHASER_PRO_SECRET", cast=Secret)
        PODCHASER_KEY : str = config("PODCHASER_PRO_KEY")
    else:
        raise Exception(f"Invalid FASTAPI_ENV {FASTAPI_ENV}")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class LoguruConfig(BaseModel):
    """Loguru configuration to be set for the server"""

    PATH: str = "./"
    FILENAME: str = "dev.log"
    LEVEL: str = "debug"
    ROTATION: str = "20 days"
    RETENTION: str = "1 months"
    FORMAT: str = "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> request id: {extra[request_id]} - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"

    def __init__(__pydantic_self__, for_worker_log:bool=False,**data: Any) -> None:
        super().__init__(**data)
        
        if for_worker_log:
            __pydantic_self__.FILENAME = "worker.log"


@lru_cache()
def get_loguru_conf():
    return LoguruConfig()


loguru_conf = get_loguru_conf()


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
