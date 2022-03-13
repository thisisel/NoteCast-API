# Custom Logger Using Loguru
import logging
import os
from functools import lru_cache
from pathlib import Path

from loguru import logger
from note_cast.core.settings import loguru_conf

base_dir = os.path.abspath(os.path.dirname(__file__))


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
    def make_logger(cls, logger_name: dict = dict(app_logger="uvicorn.access")):

        logger = cls.customize_logging(
            filepath=Path(base_dir).joinpath(loguru_conf.FILENAME),
            level=loguru_conf.LEVEL,
            retention=loguru_conf.RETENTION,
            rotation=loguru_conf.ROTATION,
            format=loguru_conf.FORMAT,
            logger_name=logger_name,
        )

        return logger

    @classmethod
    def customize_logging(
        cls,
        filepath: Path,
        level: str,
        rotation: str,
        retention: str,
        format: str,
        logger_name: dict,
    ):

        logging.basicConfig(handlers=[InterceptHandler()], level=0)

        # for name in logging.root.manager.loggerDict.keys():
        #     print(name)

        if name := logger_name.get("app_logger", None):

            logging.getLogger(name).handlers = [InterceptHandler()]

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
        else:
            try:
                # logging.getLogger(name).handlers = []
                # logging.getLogger(logger_name['rq.worker']).handlers = [InterceptHandler()]
                logging.getLogger(logger_name["rq.worker"]).propagate = True

            except KeyError as exc:
                raise exc


@lru_cache
def get_logger():
    return CustomizeLogger.make_logger()


@lru_cache
def get_worker_logger():
    return CustomizeLogger.make_logger(logger_name={"rq.worker": "rq.worker"})


loguru_app_logger = get_logger()
loguru_worker_logger = get_worker_logger()
