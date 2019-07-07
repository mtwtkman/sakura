from functools import wraps

from .net import HttpMethod
from .request import Request


class resource:
    def __new__(cls, *args, **kwargs):
        for method in list(HttpMethod):

            def _(m: HttpMethod):
                def __(self, handler):
                    return self._to(handler, m)

                return __

            setattr(cls, method.value, _(method))
        return super().__new__(cls)

    def __init__(self, path: str):
        self.path = path

    def _to(self, handler, method: HttpMethod) -> "resource":
        self.handler = handler
        self.method = method
        return self

    def is_allowed_method(self, method):
        return self.method == method


def _resource_handler(method: HttpMethod):
    def _inner(path: str):
        def __inner(handler):
            @wraps(handler)
            def ___inner(request: Request, *args, **kwargs):
                return handler(request, *args, **kwargs)

            return getattr(resource(path), method.value)(___inner)

        return __inner

    return _inner


get = _resource_handler(HttpMethod.GET)
post = _resource_handler(HttpMethod.POST)
put = _resource_handler(HttpMethod.PUT)
delete = _resource_handler(HttpMethod.DELETE)
