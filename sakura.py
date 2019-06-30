from abc import ABC, abstractmethod
import json
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs


class Request:
    def __init__(self, environ, method, body):
        self.environ = environ
        self.method = method
        self.body = parse_qs(body.decode()) or {}


class App:
    def __init__(self):
        self.resource_map = {}

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']
        if method == 'GET':
            request_body = environ['QUERY_STRING']
        elif method == 'POST':
            try:
                request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            except ValueError:
                request_body_size = 0
            request_body = environ['wsgi.input'].read(request_body_size)
        resource = self.resource_map.get(path, None)
        content_type = 'text/plain'
        if not resource:
            status = '404 NotFound'
            response = status
        elif resource.method != method:
            status = '405 Method Not Allowed'
            response = status
        else:
            response = resource.handler(Request(environ, method, request_body))
            if isinstance(response, dict):
                response = json.dumps(response)
                content_type = 'application/json'
            status = '200 OK'
        response_headers = [
            ('Content-Type', content_type),
            ('Content-Length', str(len(response))),
        ]
        start_response(status, response_headers)
        return [response.encode()]

    def service(self, service):
        self.resource_map[service.path] = service
        return self


class Server:
    def __init__(self, app):
        self.app = app

    def bind(self, host, port):
        self.host = host
        self.port = port
        return self

    def run(self):
        with make_server(self.host, self.port, self.app) as httpd:
            print(f'Start server {self.host}:{self.port}')
            httpd.serve_forever()


class resource:
    def __init__(self, path):
        self.path = path

    def _to(self, handler, method):
        self.handler = handler
        self.method = method
        return self

    def get(self, handler):
        return self._to(handler, 'GET')

    def post(self, handler):
        return self._to(handler, 'POST')


if __name__ == '__main__':
    def handle_get(request):
        data = ','.join(f'{k.upper()}: {v}' for k, v in request.body.items())
        return data or 'no params'

    def j(request):
        return request.body or {'sakura': 'kinomoto', 'tomoyo': 'daidouji'}

    def handle_post(request):
        return dict(result=True, **request.body)

    app = App() \
        .service(resource('/').get(handle_get)) \
        .service(resource('/json').get(j)) \
        .service(resource('/post').post(handle_post))
    Server(app=app).bind('0.0.0.0', 8000).run()
