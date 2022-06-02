import typer

db_cli_app = typer.Typer()


@db_cli_app.command()
def init():
    from neomodel import install_all_labels
    from note_cast.db import models

    install_all_labels()


@db_cli_app.command()
def remove():
    from neomodel import remove_all_labels
    import note_cast.db

    _ = typer.confirm("Are you sure you want to drop all indexes and constraints?", abort=True)
    remove_all_labels()



@db_cli_app.command()
def clear(
    indexes: bool = typer.Option(
        default=False,
        prompt="Are you sure you want to drop all indexes?",
    ),
    constraints: bool = typer.Option(
        default=False, prompt="Are sure you want to drop all constraints?"
    ),

):
    from neomodel import clear_neo4j_database, db
    import note_cast.db

    _ = typer.confirm("Are sure you want to clear all data?", abort=True)
    extra_clean = dict(clear_constraints=constraints, clear_indexes=indexes)

    clear_neo4j_database(db, **extra_clean)



@db_cli_app.command()
def drop(
    indexes: bool = typer.Option(
        default=False,
        prompt="Are you sure you want to drop all indexes and constraints?",
    ),
    constraints: bool = typer.Option(
        default=False, prompt="Are sure you want to clear all data?"
    ),
):

    from neomodel import clear_neo4j_database, drop_indexes, drop_constraints
    import note_cast.db


    if indexes:
        confirmed = typer.confirm("Are you sure you want to drop all indexes?")
        if confirmed:
            drop_indexes()

        else:
            typer.echo("Not deleting")
    
    elif constraints:
        confirmed = typer.confirm("Are you sure you want to drop all constraints?")
        if confirmed:
            drop_constraints()

        else:
            typer.echo("Not deleting")

