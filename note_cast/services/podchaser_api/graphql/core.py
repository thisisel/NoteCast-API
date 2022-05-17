from note_cast.api.errors.podchaser_exception import PodchaserException
from note_cast.log.custom_logging import loguru_app_logger
from note_cast.core.settings import PodchaserConfig
from note_cast.schemas import PaginatorInfo
from python_graphql_client import GraphqlClient


class PodchaserCoreUtils:

    client = GraphqlClient(
        endpoint=PodchaserConfig.BASE_GQ_PATH, headers=PodchaserConfig.HEADERS
    )

    @classmethod
    def execute_query(cls, query: str):

        response = cls.client.execute(query=query)

        if (errors := response.get("errors", None)) is not None:
            loguru_app_logger.error(errors)
            raise PodchaserException(error=errors)

        if (data := response.get("data")) is None:
            error: str = f"KeyError while getting 'data' field in Podchaser response \n{response}"
            loguru_app_logger.exception(error)
            raise PodchaserException(error=error)

        return data

    @classmethod
    def make_pagination_info(cls, pagination_response: dict):
        paginator_info = PaginatorInfo(
            currentPage=pagination_response.get("currentPage"),
            hasMorePages=pagination_response.get("hasMorePages"),
            total=pagination_response.get("total"),
        )
        return paginator_info
