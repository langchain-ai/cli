import typer
import subprocess
from typing import Annotated, Optional

from langc.namespaces import hub
from langc.namespaces import serve

app = typer.Typer(no_args_is_help=True, add_completion=False)
app.add_typer(hub.hub, name="hub", help=hub.__doc__)
app.add_typer(serve.serve, name="serve", help=serve.__doc__)


@app.command()
def start(
    *,
    port: Annotated[
        Optional[int], typer.Option(help="The port to run the server on")
    ] = None,
    host: Annotated[
        Optional[str], typer.Option(help="The host to run the server on")
    ] = None,
) -> None:
    cmd = ["poetry", "run", "poe", "start"]
    if port is not None:
        cmd += ["--port", str(port)]
    if host is not None:
        cmd += ["--host", host]
    subprocess.run(cmd)


if __name__ == "__main__":
    app()
