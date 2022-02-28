import os

import redis
from rq import Worker, Queue, Connection
# from note_cast.core.settings import settings

listen = ['transcript', 'default']

# redis_conn = redis.from_url(settings.REDIS_URL)
redis_conn = redis.from_url('redis://localhost:6379')

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen))
        worker.work(with_scheduler=True)
