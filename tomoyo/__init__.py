import sys


class PythonVersionError(Exception):
    pass


if sys.version_info[:2] < (3, 7):
    raise PythonVersionError("tomoyo supports python3.7+.")


from .resource import resource, get, post, put, delete
from .server import Server
from .app import App, scope
