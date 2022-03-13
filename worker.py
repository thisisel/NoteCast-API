import sys

import redis
from rq import Connection, Queue, Worker

from note_cast.core.settings import settings

redis_conn = redis.from_url(settings.REDIS_URL)
listen = settings.REDIS_LISTEN


if __name__ == "__main__":

    queue_name = sys.argv[1]

    if queue_name in listen:
        with Connection(redis_conn):
            worker = Worker(map(Queue, [queue_name]))
            worker.work(with_scheduler=True)
    else:
        print("invalid queue name passed")
