import logging
import uvicorn
import typer
import redis
from rq import Worker, Queue, Connection
from note_cast.app import settings, app
# from note_cast.log.custom_logging import loguru_worker_logger
from loguru import logger


cli_app = typer.Typer()

@cli_app.command()
def run(host : str = settings.HOST, port : int = settings.PORT, reload : bool = True):
    uvicorn.run("manage:app", host=host, port=port, reload=reload)

@cli_app.command()
def worker():
    listen = ['transcript', 'default']
    # redis_conn = redis.from_url(settings.REDIS_URL)
    redis_conn = redis.from_url('redis://localhost:6379')
    
    # typer.echo('Initiating connection...')
   
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen))
        worker.work(with_scheduler=True)
        logging.getLogger('rq.worker').propagate = True
        worker.log = logger
    
    # typer.echo('Worker redis connection closed!')

if __name__ == "__main__":
    cli_app()