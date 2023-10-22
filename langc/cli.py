import typer

from langc.namespaces import hub
from langc.namespaces import serve

app = typer.Typer(no_args_is_help=True, add_completion=False)
app.add_typer(hub.hub, name="hub", help=hub.__doc__)
app.add_typer(serve.serve, name="serve", help=serve.__doc__)


@app.command()
def start():
    """
    Start the hub or serve server, depending which directory you are in.
    """
    pass


if __name__ == "__main__":
    app()
