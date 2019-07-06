from unittest import TestCase

from sakura import memoise


class TestMemoise(TestCase):
    def test_wrap_property(self):
        class C:
            def __init__(self, a):
                self.a = a

            def _do_something(self, x):
                self.a = x

            @property
            @memoise
            def under_test(self):
                return self._do_something(10)

            @property
            @memoise
            def never_changed(self):
                return self._do_something(100)

        c = C(1)
        self.assertFalse(hasattr(c, '_under_test'))
        c.under_test
        c.never_changed
        self.assertNotEqual(c.a, c.under_test)
        self.assertNotEqual(c.a, c.never_changed)
