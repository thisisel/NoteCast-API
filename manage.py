import redis
import typer
import uvicorn
from rq import Connection, Queue, Worker

from note_cast.app import app, settings

cli_app = typer.Typer()


@cli_app.command()
def run(host: str = settings.HOST, port: int = settings.PORT, reload: bool = True):
    uvicorn.run("manage:app", host=host, port=port, reload=reload)


@cli_app.command()
def worker(queue_name: str):
    listen = listen = settings.REDIS_LISTEN
    redis_conn = redis.from_url(settings.REDIS_URL)

    if queue_name in listen:
        with Connection(redis_conn):
            worker = Worker(map(Queue, [queue_name]))
            worker.work(with_scheduler=True)
            # worker.clean_registries()
    else:
        typer.echo(f"An invalid argument passed for queue name = {queue_name}")
        typer.echo(f"Valid queue names include: {listen}")

    typer.echo('Worker redis connection closed!')


if __name__ == "__main__":
    cli_app()
