from unittest import TestCase

import wolfeutils

class TestJoke(TestCase):
    def test_is_string(self):
        s = wolfeutils.joke()
        self.assertTrue(isinstance(s, basestring))
