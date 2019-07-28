import re

from .net import HttpMethod
from .request import Request
from .response import (
    NotFound,
    MethodNotAllowed,
    build_ok_response,
)
from .service import Service


class InvalidHttpMethod(Exception):
    pass


class App(Service):
    @property
    def resource_path_map(self):
        if not hasattr(self, "_resource_path_map"):

            def loop(path, value, tail, acc):
                if isinstance(value, scope):
                    [(p, v), *t] = value.resource_map.items()
                    loop(f"{path}{p}", v, t, acc)
                else:
                    acc[path] = value
                if not tail:
                    return acc
                [(p, v), *t] = tail
                return loop(p, v, t, acc)

            [(path, value), *tail] = self.resource_map.items()
            self._resource_path_map = loop(path, value, tail, {})
        return self._resource_path_map

    @property
    def resource_paths(self):
        return self.resource_path_map.keys()

    def _from_query_string(self, environ):
        return environ["QUERY_STRING"]

    def _from_stream(self, environ):
        try:
            request_body_size = int(environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            request_body_size = 0
        return environ["wsgi.input"].read(request_body_size).decode()

    def _abort(self, e, *args, **kwargs):
        raise e(*args, **kwargs)

    def _build_request_body(self, method, environ):
        return {
            HttpMethod.GET: self._from_query_string,
            HttpMethod.POST: self._from_stream,
        }.get(method, lambda _: self._abort(InvalidHttpMethod, method))(environ)

    def _find_matched_path(self, path):
        filterd = [
            x
            for x in [(p, re.match(fr"^{p}$", path)) for p in self.resource_paths]
            if x[1]
        ]
        if filterd:
            return {"name": filterd[0][0], "matched_object": filterd[0][1]}
        return

    def __call__(self, environ, start_response):
        path: str = environ["PATH_INFO"]
        method = getattr(HttpMethod, environ["REQUEST_METHOD"])
        request_body = self._build_request_body(method, environ)
        matched_path = self._find_matched_path(path)

        if not matched_path:
            response = NotFound()
        else:
            resource = self.resource_path_map[matched_path["name"]]
            if not resource.is_allowed_method(method):
                response = MethodNotAllowed()
            else:
                response_body = resource.handler(
                    Request(environ, resource.method, request_body),
                    **matched_path["matched_object"].groupdict(),
                )
                response = build_ok_response(response_body)
        start_response(
            str(response.status_code_message), response.headers.as_key_value_pairs()
        )
        return [response.body.encode()]


class scope(Service):
    def __init__(self, path):
        super().__init__()
        self.path = path
