import typer
from typing import Annotated, Optional
from pathlib import Path

import shutil
import re
import subprocess

from langc.namespaces.hub import hub
from langc.namespaces.serve import serve

app = typer.Typer(no_args_is_help=True, add_completion=False)
app.add_typer(hub, name="hub")
app.add_typer(serve, name="serve")


def _git_get_root(destination_dir: Optional[Path]) -> Optional[Path]:
    """Get the root of the git repository."""
    try:
        path_out = (
            subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                cwd=None
                if destination_dir is None
                else str(destination_dir.absolute()),
            )
            .stdout.decode()
            .strip()
        )
        if path_out:
            return Path(path_out)

    except Exception:
        pass

    return None


@app.command()
def new(name: Annotated[str, typer.Argument(help="The name of the folder to create")]):
    # copy over template from ../project_template
    project_template_dir = Path(__file__).parent.parent / "project_template"
    destination_dir = Path.cwd() / name if name != "." else Path.cwd()
    shutil.copytree(project_template_dir, destination_dir, dirs_exist_ok=name == ".")


if __name__ == "__main__":
    app()
