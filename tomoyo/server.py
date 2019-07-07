from wsgiref.simple_server import make_server


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
