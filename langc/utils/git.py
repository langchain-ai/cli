import typer
from typing import Annotated, Optional, TypedDict
from pathlib import Path

import shutil
import re
import subprocess
from langc.constants import DEFAULT_GIT_REPO, DEFAULT_GIT_BRANCH
from langc.utils.packages import get_langserve_export
import hashlib
from git import Repo


class DependencySource(TypedDict):
    git: str
    ref: str
    subdirectory: Optional[str]


LANGCHAIN_DIRECTORY = Path.home() / ".langchain"
REPO_DIRECTORY = LANGCHAIN_DIRECTORY / "git_repos"


# use poetry dependency string format
def _parse_dependency_string(package_string: str) -> DependencySource:
    if package_string.startswith("git+"):
        # remove git+
        remaining = package_string[4:]
        # split main string from params
        gitstring, *params = remaining.split("#")
        # parse params
        params_dict = {}
        for param in params:
            if not param:
                # ignore empty entries
                continue
            if "=" in param:
                key, value = param.split("=")
                if key in params_dict:
                    raise ValueError(
                        f"Duplicate parameter {key} in dependency string {package_string}"
                    )
                params_dict[key] = value
            else:
                if "ref" in params_dict:
                    raise ValueError(
                        f"Duplicate parameter ref in dependency string {package_string}"
                    )
                params_dict["ref"] = param
        return DependencySource(
            git=gitstring,
            ref=params_dict.get("ref", DEFAULT_GIT_BRANCH),
            subdirectory=params_dict.get("subdirectory"),
        )

    elif package_string.startswith("https://"):
        raise NotImplementedError("url dependencies are not supported yet")
    else:
        # it's a default git repo dependency
        gitstring = DEFAULT_GIT_REPO
        branch = DEFAULT_GIT_BRANCH
        subdirectory = package_string
        return DependencySource(git=gitstring, ref=branch, subdirectory=subdirectory)


def _get_repo_path(dependency: DependencySource) -> Path:
    # only based on git for now
    gitstring = dependency["git"]
    hashed = hashlib.sha256(gitstring.encode("utf-8")).hexdigest()[:8]

    removed_protocol = gitstring.split("://")[-1]
    removed_basename = re.split(r"[/:]", removed_protocol, 1)[-1]
    removed_extras = removed_basename.split("#")[0]
    foldername = re.sub(r"[^a-zA-Z0-9_]", "_", removed_extras)

    directory_name = f"{foldername}_{hashed}"
    return REPO_DIRECTORY / directory_name


def update_repo(gitpath: str) -> Path:
    # see if path already saved
    dependency = _parse_dependency_string(gitpath)
    repo_path = _get_repo_path(dependency)
    if not repo_path.exists():
        repo = Repo.clone_from(dependency["git"], repo_path)
    else:
        repo = Repo(repo_path)

    # pull it
    repo.git.checkout(dependency["ref"])

    repo.git.pull()

    return (
        repo_path
        if dependency["subdirectory"] is None
        else repo_path / dependency["subdirectory"]
    )


def copy_repo(
    source: Path,
    destination: Path,
) -> None:
    ignore_func = lambda _, files: [f for f in files if f == ".git"]
    shutil.copytree(source, destination, ignore=ignore_func)
