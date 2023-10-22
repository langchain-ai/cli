"""
Manage installable hub packages.
"""

import typer
from typing import Annotated, Optional
from pathlib import Path
import shutil
import re
from fastapi import FastAPI
from langserve.packages import add_package_route
from langc.utils.packages import get_package_root

hub = typer.Typer(no_args_is_help=True, add_completion=False)


@hub.command()
def new(name: Annotated[str, typer.Argument(help="The name of the folder to create")]):
    """
    Creates a new hub package.
    """
    computed_name = name if name != "." else Path.cwd().name
    destination_dir = Path.cwd() / name if name != "." else Path.cwd()

    # copy over template from ../package_template
    project_template_dir = Path(__file__).parent.parent.parent / "package_template"
    shutil.copytree(project_template_dir, destination_dir, dirs_exist_ok=name == ".")

    package_name_split = computed_name.split("/")
    package_name_last = (
        package_name_split[-2]
        if len(package_name_split) > 1 and package_name_split[-1] == ""
        else package_name_split[-1]
    )
    default_package_name = re.sub(
        r"[^a-zA-Z0-9_]",
        "_",
        package_name_last,
    )

    # replace template strings
    pyproject = destination_dir / "pyproject.toml"
    pyproject_contents = pyproject.read_text()
    pyproject.write_text(
        pyproject_contents.replace("__package_name__", default_package_name)
    )

    # move module folder
    package_dir = destination_dir / default_package_name
    shutil.move(destination_dir / "package_template", package_dir)

    # replace readme
    readme = destination_dir / "README.md"
    readme_contents = readme.read_text()
    readme.write_text(
        readme_contents.replace("__package_name_last__", package_name_last)
    )


@hub.command()
def start(
    *,
    port: Annotated[int, typer.Option(help="The port to run the server on")] = 8000,
    host: Annotated[str, typer.Option(help="The host to run the server on")] = "0.0.0.0"
):
    """
    Starts a demo server for the current hub package.
    """
    app = FastAPI()
    package_root = get_package_root()
    add_package_route(app, package_root, "/")
    typer.echo("Starting server...")
    import uvicorn

    uvicorn.run(app, host=host, port=port)
