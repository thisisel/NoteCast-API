from rq import Queue
from rq.exceptions import NoSuchJobError
from rq.job import Job
from rq.registry import ScheduledJobRegistry

from worker import redis_conn
from tasks import pull_transcript
from datetime import timedelta

transcript_queue = Queue(name="transcript", connection=redis_conn)
registry = ScheduledJobRegistry(queue=transcript_queue)


def schedule_transcript_job(seconds, *args, **kwargs):
    job = transcript_queue.enqueue_in(timedelta(seconds=seconds), pull_transcript, *args, **kwargs)
    return job


fetch_job_by_id = lambda job_id: Job.fetch(job_id, connection=redis_conn)


def get_job_status(job_id):
    job = Job.fetch(job_id, connection=redis_conn)
    status = {
        "queued": job.is_queued,
        "finished": job.is_finished,
        "started": job.is_started,
        "failed": job.is_failed,
    }
    return status


def job_in_registry(job_id):
    try:
        job = Job.fetch(job_id, connection=redis_conn)

    except NoSuchJobError:
        return None

    return job in registry


def cancel_scheduled_job(job_id):
    job = Job.fetch(job_id, connection=redis_conn)
    registry.remove(job=job, delete_job=True)
