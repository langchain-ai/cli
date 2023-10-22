from pathlib import Path
from typing import Set


def get_package_root() -> Path:
    # traverse path for routes to host (any directory holding a pyproject.toml file)
    package_root = Path.cwd()
    visited: Set[Path] = set()
    while True:
        pyproject_path = package_root / "pyproject.toml"
        if pyproject_path.exists():
            return package_root
        if package_root.parent == package_root:
            raise FileNotFoundError("No pyproject.toml found")
        package_root = package_root.parent
