import cloudinary.api
from requests import get


class CloudinaryResource:
    @classmethod
    def download_raw_resource(cls, public_id: str):
        r_resp = cloudinary.api.resource(public_id=public_id, resource_type="raw")
        r = get(url=r_resp["url"])
        j = r.json()

        transcript = j[0].get("transcript")
        print(transcript)

        return transcript
