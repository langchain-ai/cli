"""
Manage LangServe application projects.
"""

import typer
from typing import Annotated, Optional, List
from pathlib import Path
import shutil
import re
from langc.utils.git import copy_repo, update_repo
from langc.utils.packages import get_package_root
from langserve.packages import list_packages, get_langserve_export

serve = typer.Typer(no_args_is_help=True, add_completion=False)


@serve.command()
def new(
    name: Annotated[str, typer.Argument(help="The name of the folder to create")],
    packages: Annotated[
        Optional[List[str]], typer.Option(help="Packages to seed the project with")
    ],
):
    """
    Create a new LangServe application.
    """
    # copy over template from ../project_template
    project_template_dir = Path(__file__).parent.parent / "project_template"
    destination_dir = Path.cwd() / name if name != "." else Path.cwd()
    shutil.copytree(project_template_dir, destination_dir, dirs_exist_ok=name == ".")

    # add packages if specified
    if packages is not None:
        add(packages)


@serve.command()
def add(
    dependencies: Annotated[List[str], typer.Argument(help="The dependency to add")],
):
    """
    Adds the specified package to the current LangServe instance.
    """
    package_dir = Path.cwd() / "packages"
    for dependency in dependencies:
        # update repo
        typer.echo(f"Adding {dependency}...")
        source_path = update_repo(dependency)
        pyproject_path = source_path / "pyproject.toml"
        langserve_export = get_langserve_export(pyproject_path)

        destination_path = package_dir / langserve_export.package_name
        if destination_path.exists():
            typer.echo(
                f"Endpoint {langserve_export.package_name} already exists. Skipping...",
            )
            continue
        copy_repo(source_path, destination_path)


@serve.command()
def remove(name: str):
    """
    Removes the specified package from the current LangServe instance.
    """
    pass


@serve.command()
def list():
    """
    Lists all packages in the current LangServe instance.
    """
    package_root = get_package_root() / "packages"
    for package_path in list_packages(package_root):
        relative = package_path.relative_to(package_root)
        pyproject_path = package_path / "pyproject.toml"
        langserve_export = get_langserve_export(pyproject_path)
        typer.echo(
            f"{relative}: ({langserve_export['module']}.{langserve_export['attr']})"
        )
