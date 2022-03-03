from note_cast.db.models import Quote
from note_cast.services.cloudinary_api import asset_folder_path
from note_cast.services.cloudinary_api.resource import CloudinaryResource
from note_cast.db.crud.quote import QuoteQuery


def pull_transcript(p_id : str, e_id: str, q_id: str, transcript: str):

    try:
        asset_path = asset_folder_path(p_id=p_id, e_id=e_id)
        raw_public_id = f"{asset_path}{q_id}.transcript"
        CloudinaryResource.download_raw_resource(public_id=raw_public_id)
        QuoteQuery.update_transcript(q_id=q_id, transcript=transcript)
   
    except Exception as x:
        print(x)
        print(x.with_traceback())
    