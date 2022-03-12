import sys

import redis
from rq import Worker, Queue, Connection


redis_conn = redis.from_url('redis://localhost:6379')
listen = ['cpu', 'network', 'hybrid']


if __name__ == '__main__':

    queue_name = sys.argv[1]
   
    if queue_name in listen:
        with Connection(redis_conn):  
            worker = Worker(map(Queue, [queue_name]))
            worker.work(with_scheduler=True)
    else:
        print('invalid queue name passed')
