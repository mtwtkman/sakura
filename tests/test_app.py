from io import BytesIO
import json
from unittest import TestCase, mock, skip

from sakura import App, resource, scope, get


start_response_mock = mock.Mock()


class TestRequestHandlerCall(TestCase):
    """totally tests"""
    def setUp(self):
        def get_handler(request):
            x = json.dumps(request.body) if request.body else 'no param'
            return f'GET: {x}'

        def post_handler(request):
            x = json.dumps(request.body) if request.body else 'no param'
            return f'POST: {x}'

        def get_json_handler(request):
            return {'x': 1, y: 'x'}

        @get('/decorated')
        def decorated_handler(request):
            return 'GET: decorated'

        def scoped_handler(request):
            return 'GET: scoped'

        scoped = scope('/nest1').service(resource('/scoped').get(scoped_handler))

        self.dummy_app = App() \
            .service(resource('/get').get(get_handler)) \
            .service(resource('/post').post(post_handler)) \
            .service(decorated_handler) \
            .service(scoped)

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

    def test_404(self):
        result = self.call_app(self.build_environ('/not_found', 'get'))
        self.assertEqual(result, [b'404 NotFound'])

    def test_405(self):
        result = self.call_app(self.build_environ('/get', 'post'))
        self.assertEqual(result, [b'405 MethodNotAllowed'])

    def test_get_without_params(self):
        result = self.call_app(self.build_environ('/get', 'get'))
        self.assertEqual(result, [b'GET: no param'])

    def test_get_with_params(self):
        result = self.call_app(self.build_environ('/get', 'get', 'x=1&y=2'))
        self.assertEqual(result, [b'GET: {"x": ["1"], "y": ["2"]}'])

    def test_post_without_payload(self):
        result = self.call_app(self.build_environ('/post', 'post'))
        self.assertEqual(result, [b'POST: no param'])

    def test_post_with_payload(self):
        result = self.call_app(self.build_environ('/post', 'post', payload='x=1&y=2'))
        self.assertEqual(result, [b'POST: {"x": ["1"], "y": ["2"]}'])

    def test_decorated(self):
        result = self.call_app(self.build_environ('/decorated', 'get'))
        self.assertEqual(result, [b'GET: decorated'])

    def test_scoped(self):
        result = self.call_app(self.build_environ('/nest1/scoped', 'get'))
        self.assertEqual(result, [b'GET: scoped'])


class TestResourcePathMap(TestCase):
    def setUp(self):
        self.solo_path = '/solo'
        self.solo_handler = lambda: 1
        self.multiple_path = '/multi/index.html'
        self.multiple_handler = lambda: 10
        self.scoped_parent_path = '/nested'
        self.scoped_child_path = '/scoped'
        self.scoped_handler = lambda: 2

        self.solo_service = resource(self.solo_path).get(self.solo_handler)
        self.multiple_service = resource(self.multiple_path).get(self.multiple_handler)
        self.scoped_service = resource(self.scoped_child_path).get(self.scoped_handler)
        self.app = App() \
            .service(self.solo_service) \
            .service(scope(self.scoped_parent_path).service(self.scoped_service)) \
            .service(self.multiple_service)

    def _callFUT(self):
        return self.app.resource_path_map

    def test_ok(self):
        result = self._callFUT()
        expected = {
            self.solo_path: self.solo_service,
            self.multiple_path: self.multiple_service,
            f'{self.scoped_parent_path}{self.scoped_child_path}': self.scoped_service,
        }
        self.assertEqual(result, expected)
