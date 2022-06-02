import typer
from db_manage import db_cli_app


cli_app = typer.Typer()
cli_app.add_typer(db_cli_app, name="db")


@cli_app.command()
def run(host: str = None, port: int = None, reload: bool = True):
    import uvicorn
    from note_cast.app import settings

    if host is None:
        host = settings.HOST

    if port is None:
        port = settings.PORT

    uvicorn.run("note_cast.app:app", host=host, port=port, reload=reload)


@cli_app.command()
def worker(queue_name: str):
    import redis
    from rq import Connection, Queue, Worker
    from note_cast.app import settings

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

    typer.echo("Worker redis connection closed!")


if __name__ == "__main__":
    cli_app()
