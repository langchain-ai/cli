"""
Development Scripts for Hub Packages
"""

from fastapi import FastAPI
from langserve.packages import add_package_route
from langc.utils.packages import get_package_root


def start_demo_server(*, port: int = 8000, host: str = "0.0.0.0"):
    """
    Starts a demo server for the current hub package.
    """
    app = FastAPI()
    package_root = get_package_root()
    add_package_route(app, package_root, "")
    import uvicorn

    # cast port as an int in case it comes as a string argument
    # from poe
    uvicorn.run(
        app,
        host=host,
        port=int(port),
        reload=True,
        reload_dirs=[str(package_root.resolve())],
    )
