from email.quoprimime import quote
from fastapi import APIRouter, Request, Response, status
from requests import get
from pprint import pprint
from note_cast.services.cloudinary_api.resource import CloudinaryResource
from note_cast.db.crud.quote import QuoteQuery
from interface import cancel_scheduled_job

router = APIRouter(prefix="/callback")


@router.post("/cloudinary/upload/")
async def cloudinary_upload_callback(request: Request):

    upload_resp = await request.json()

    if upload_resp.get('info_kind') == 'google_speech':
        try:
            public_id : str = upload_resp["public_id"]
            job_id = public_id.split("/")[-1]
            cancel_scheduled_job(job_id=job_id)
            
            raw_public_id = public_id + ".transcript"
            
            transcript = CloudinaryResource.download_raw_resource(public_id=raw_public_id)
            quote = QuoteQuery.update_transcript(q_id=job_id, transcript=transcript)
        
        except Exception as ex:
            print(ex)

    return Response(status_code=status.HTTP_200_OK)