# Custom Logger Using Loguru
from functools import lru_cache

import logging

from pathlib import Path
from loguru import logger
from note_cast.core.settings import loguru_conf


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "NOTSET",
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id="app")
        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class CustomizeLogger:
    @classmethod
    def make_logger(cls):

        logger = cls.customize_logging(
            Path(loguru_conf.PATH).joinpath(loguru_conf.FILENAME),
            level=loguru_conf.LEVEL,
            retention=loguru_conf.RETENTION,
            rotation=loguru_conf.ROTATION,
            format=loguru_conf.FORMAT,
        )

        return logger

    @classmethod
    def customize_logging(
        cls, filepath: Path, level: str, rotation: str, retention: str, format: str
    ):

        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ["uvicorn", "uvicorn.error", "fastapi"]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        logger.remove()

        logger.add(
            str(filepath),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format,
        )

        return logger.bind(request_id=None, method=None)


@lru_cache()
def get_logger():
    return CustomizeLogger.make_logger()


loguru_logger = get_logger()
