from unittest import TestCase

from tomoyo import resource
from tomoyo.service import Service, ReservedPathError


class TestService(TestCase):
    def setUp(self):
        self.service = Service()

    def _callFUT(self, resource):
        return self.service.service(resource)

    def test_ok(self):
        path = '/foo'
        actual = self._callFUT(resource(path).get(lambda: 1))
        self.assertTrue(path in actual.resource_map)

    def test_error(self):
        path = '/foo'
        self._callFUT(resource(path).get(lambda: 1))
        with self.assertRaises(ReservedPathError):
            self._callFUT(resource(path).get(lambda: 2))
