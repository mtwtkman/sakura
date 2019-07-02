from unittest import TestCase

from sakura import HttpMethod


class TestResourceTo(TestCase):
    def _callFUT(self, handler, method):
        from sakura import resource
        return resource('')._to(handler, method)

    def test_return_self(self):
        handler = lambda req: 1
        method = HttpMethod.GET
        one = self._callFUT(handler, method)
        self.assertEqual(one.handler, handler)
        self.assertEqual(one.method, method)
