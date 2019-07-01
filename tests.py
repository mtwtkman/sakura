from io import BytesIO
import json
from unittest import TestCase, mock

from sakura import App, resource


start_response_mock = mock.Mock()


class TestApp(TestCase):
    def setUp(self):
        def get_handler(request):
            x = json.dumps(request.body) if request.body else 'no param'
            return f'GET: {x}'

        def post_handler(request):
            x = json.dumps(request.body) if request.body else 'no param'
            return f'POST: {x}'

        def get_json_handler(request):
            return {'x': 1, y: 'x'}

        self.dummy_app = App() \
            .service(resource('/get').get(get_handler)) \
            .service(resource('/post').post(post_handler))

    def call_app(self, environ):
        return self.dummy_app(environ, start_response_mock)

    def build_environ(self, path, method, qs=None, payload=''):
        environ = {
            'PATH_INFO': path,
            'REQUEST_METHOD': method.upper(),
            'QUERY_STRING': qs
        }
        if method == 'post':
            b = payload.encode()
            environ['wsgi.input'] = BytesIO(b)
            environ['CONTENT_LENGTH'] = len(b)
        return environ

    def test_get_without_params(self):
        result = self.call_app(self.build_environ('/get', 'get'))
        assert result == [b'GET: no param']

    def test_get_with_params(self):
        result = self.call_app(self.build_environ('/get', 'get', 'x=1&y=2'))
        assert result == [b'GET: {"x": ["1"], "y": ["2"]}']

    def test_post_without_payload(self):
        result = self.call_app(self.build_environ('/post', 'post'))
        assert result == [b'POST: no param']

    def test_post_with_payload(self):
        result = self.call_app(self.build_environ('/post', 'post', payload='x=1&y=2'))
        assert result == [b'POST: {"x": ["1"], "y": ["2"]}']
