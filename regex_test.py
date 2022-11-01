import unittest

from regex import shunting_yard

class RegexTest(unittest.TestCase):

    def test_shunting_yard(self):
        self.assertEqual(shunting_yard("0"), "0")
        self.assertEqual(shunting_yard("01"), "01.")
        self.assertEqual(shunting_yard("0+1"), "01+")
        self.assertEqual(shunting_yard("(0+1)*0+11"), "01+*0.11.+")
        self.assertEqual(shunting_yard("0(0+1)*1"), "001+*.1.")

    def test_thomsons_construction(self):
        pass
