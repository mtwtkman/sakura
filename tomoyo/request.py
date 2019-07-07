from urllib.parse import parse_qs


class Request:
    def __init__(self, environ, method, body):
        self.environ = environ
        self.method = method
        self.body = parse_qs(body) or {}
