from unittest import TestCase


class TestResourceNew(TestCase):
    def _callFUT(self):
        from sakura import resource
        return resource.__new__(resource)

    def test_generate_methods_named_http_method(self):
        one = self._callFUT()
        self.assertTrue(hasattr(one, 'get'))
        self.assertTrue(hasattr(one, 'post'))
        self.assertTrue(hasattr(one, 'put'))
        self.assertTrue(hasattr(one, 'delete'))
