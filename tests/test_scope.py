from unittest import TestCase

from tomoyo import resource


class TestScope(TestCase):
    def _makeOne(self, path):
        from tomoyo import scope
        return scope(path)

    def test_simple(self):
        path = '/hoge'
        one = self._makeOne(path)
        child = resource('/x').get(lambda req: 'x')
        one.service(child)
        self.assertEqual(one.path, path)
        self.assertTrue(child.path in one.resource_map)
        self.assertTrue(one.resource_map[child.path] is child)

    def test_nested(self):
        path = '/hoge'
        one = self._makeOne(path)
        child_path = '/fuga'
        child_one = self._makeOne(child_path)
        child_resource = resource('/x').get(lambda req: 'x')
        child_one.service(child_resource)
        one.service(child_one)
        self.assertEqual(one.path, path)
        self.assertTrue(child_one.path in one.resource_map)
        self.assertTrue(one.resource_map[child_one.path] is child_one)
