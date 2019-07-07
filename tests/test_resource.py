from unittest import TestCase

from tomoyo import HttpMethod


class TestResourceNew(TestCase):
    def _callFUT(self):
        from tomoyo import resource
        return resource.__new__(resource)

    def test_generate_methods_named_http_method(self):
        one = self._callFUT()
        self.assertTrue(hasattr(one, 'get'))
        self.assertTrue(hasattr(one, 'post'))
        self.assertTrue(hasattr(one, 'put'))
        self.assertTrue(hasattr(one, 'delete'))


class TestResourceTo(TestCase):
    def _callFUT(self, handler, method):
        from tomoyo import resource
        return resource('')._to(handler, method)

    def test_return_self(self):
        handler = lambda req: 1
        method = HttpMethod.GET
        one = self._callFUT(handler, method)
        self.assertEqual(one.handler, handler)
        self.assertEqual(one.method, method)
