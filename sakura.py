import re
import enum
from functools import wraps
import json
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs


class HttpMethod(enum.Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"


class Request:
    def __init__(self, environ, method, body):
        self.environ = environ
        self.method = method
        self.body = parse_qs(body) or {}


class Service:
    def __init__(self):
        self.resource_map = {}

    def service(self, resource):
        self.resource_map[resource.path] = resource
        return self


path_pattern = re.compile(r'(/[^/]+)')


class App(Service):
    def __init__(self):
        super().__init__()

    def resolve_path(self, raw):
        def loop(resource_map, head, tail, acc):
            x = resource_map.get(head)
            if not x:
                return
            if not tail:
                return x
            [h, *t] = tail
            if isinstance(x, scope):
                return loop(x.resource_map, h, t, None)
            return loop(resource_map, h, t, x)

        [head, *tail] = [x for x in path_pattern.split(raw) if x]
        return loop(self.resource_map, head, tail, None)

    def __call__(self, environ, start_response):
        path: str = environ["PATH_INFO"]
        method = getattr(HttpMethod, environ["REQUEST_METHOD"])
        if method == HttpMethod.GET:
            request_body = environ["QUERY_STRING"]
        elif method == HttpMethod.POST:
            try:
                request_body_size = int(environ.get("CONTENT_LENGTH", 0))
            except ValueError:
                request_body_size = 0
            request_body = environ["wsgi.input"].read(request_body_size).decode()

        resource = self.resolve_path(path)
        content_type = "text/plain"
        if not resource:
            status = "404 NotFound"
            response = status
        elif resource.method != method:
            status = "405 MethodNotAllowed"
            response = status
        else:
            response = resource.handler(Request(environ, method, request_body))
            if isinstance(response, dict):
                response = json.dumps(response)
                content_type = "application/json"
            status = "200 OK"
        response_headers = [
            ("Content-Type", content_type),
            ("Content-Length", str(len(response))),
        ]
        start_response(status, response_headers)
        return [response.encode()]


class Server:
    def __init__(self, app):
        self.app = app

    def bind(self, host, port):
        self.host = host
        self.port = port
        return self

    def run(self):
        with make_server(self.host, self.port, self.app) as httpd:
            print(f"Start server {self.host}:{self.port}")
            httpd.serve_forever()


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


class scope(Service):
    def __init__(self, path):
        super().__init__()
        self.path = path


def method_wrapper(method: HttpMethod):
    def _inner(path: str):
        def __inner(handler):
            @wraps(handler)
            def ___inner(request: Request):
                return handler(request)

            return getattr(resource(path), method.value)(___inner)

        return __inner

    return _inner


get = method_wrapper(HttpMethod.GET)
post = method_wrapper(HttpMethod.POST)
put = method_wrapper(HttpMethod.PUT)
delete = method_wrapper(HttpMethod.DELETE)
