import sys

sys.path.append("..")

from rq import Queue, get_current_job
from rq.decorators import job
from rq.registry import ScheduledJobRegistry

from worker import redis_conn

network_queue = Queue(name="network", connection=redis_conn)
cpu_queue = Queue(name="cpu", connection=redis_conn)
hybrid_queue = Queue(name="hybrid", connection=redis_conn)

network_registry = ScheduledJobRegistry(queue=network_queue)


def get_first_dependent_result(origin_queue, current_job):
    first_job = current_job.dependency
    first_job_result = origin_queue.fetch_job(first_job.id).result

    return first_job_result
