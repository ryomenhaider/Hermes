import typer
from pathlib import Path
from hermes.api.data import profile


app = typer.Typer(
    name="hermes",
    help="Foundational intelligence data platform.",
    no_args_is_help=True,
)


@app.command()
def version():
    typer.echo(f"Hermes v0.2.16")


@app.command()
def info():
    typer.echo(f"Hermes v0.2.16")
    typer.echo("Foundational intelligence data platform")

@app.command()
def profile_data(
    path: Path = typer.Argument(
        help="Path to the dataset.",
        exists=True,
        readable=True,
        resolve_path=True,
    ),
):

    report = profile(path=path)
    typer.echo(report)

if __name__ == "__main__":
    app()