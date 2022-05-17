import typer


cli_app = typer.Typer()
db_cli_app = typer.Typer()
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


@db_cli_app.command()
def init():
    from neomodel import install_all_labels
    from note_cast.db import models

    install_all_labels()


@db_cli_app.command()
def remove(
    confirmed: bool = typer.Option(
        ..., prompt="Are you sure you want to drop all indexes and constraints?"
    )
):
    from neomodel import remove_all_labels
    import note_cast.db

    if confirmed:
        remove_all_labels()
    else:
        typer.echo("canceled")


@db_cli_app.command()
def clear(
    confirmed: bool = typer.Option(
        ..., prompt="Are you sure you want to clear database?"
    )
):
    from neomodel import clear_neo4j_database
    import note_cast.db

    if confirmed:
        clear_neo4j_database()
    else:
        typer.echo("canceled")


if __name__ == "__main__":
    cli_app()
