import sys

from .app import App, scope
from .resource import delete, get, post, put, resource
from .server import Server


class PythonVersionError(Exception):
    pass


if sys.version_info[:2] < (3, 7):
    raise PythonVersionError("tomoyo supports python3.7+.")
