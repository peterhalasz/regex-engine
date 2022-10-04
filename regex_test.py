import unittest

from regex import shunting_yard

class RegexTest(unittest.TestCase):

    def test_shuingting_yard(self):
        self.assertEqual(shunting_yard("0+1"), "01+")
