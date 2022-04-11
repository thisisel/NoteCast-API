from note_cast.core.settings import settings
from note_cast.utils.http import httpx_client_factory, raise_on_4xx_5xx


headers = {"Authorization": "Bearer " + settings.PODCHASER_TOKEN, "Content-Type" : "application/json"}
base_url = settings.PODCHASER_BASE_URL
base_graphql_path = base_url + "graphql"
