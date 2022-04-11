from datetime import timedelta

from rq.exceptions import NoSuchJobError
from rq.job import Job


from tasks import redis_conn, network_queue, network_registry


def pull_transcript(p_id: str, e_id: str, q_id: str, transcript: str):
    from note_cast.db.crud.quote import QuoteQuery
    from note_cast.services.cloudinary_api import asset_folder_path
    from note_cast.services.cloudinary_api.resource import CloudinaryResource

    try:
        asset_path = asset_folder_path(p_id=p_id, e_id=e_id)
        transcript_public_id = f"{asset_path}{q_id}.transcript"

        # resource_info_response = CloudinaryResource.get_resource_info(public_id=raw_public_id, resource_type="raw")
        # resource_data = CloudinaryResource.download_resource(resource_info_response["url"])
        # resource_data_jsn = resource_data.json()
        # transcript = resource_data_jsn[0]["transcript"]

        transcript = CloudinaryResource.fetch_transcript(
            public_id=transcript_public_id, resource_type="raw"
        )

        # TODO make it either on_successful call back or dependency
        QuoteQuery.update_transcript(q_id=q_id, transcript=transcript)

    except Exception as x:
        print(x)


def schedule_pulling_transcription(seconds, *args, **kwargs):
    job = network_queue.enqueue_in(
        timedelta(seconds=seconds), pull_transcript, *args, **kwargs
    )
    return job

def cancel_scheduled_job(job_id):
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        network_registry.remove(job=job, delete_job=True)
    except NoSuchJobError as nse:
        # TODO log with worker logger
        print(nse)
