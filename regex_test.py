import unittest

from enfa import EPS
from regex import shunting_yard, thomsons_construction

class RegexTest(unittest.TestCase):

    def test_shunting_yard(self):
        self.assertEqual(shunting_yard("0"), "0")
        self.assertEqual(shunting_yard("01"), "01.")
        self.assertEqual(shunting_yard("0+1"), "01+")
        self.assertEqual(shunting_yard("(0+1)*0+11"), "01+*0.11.+")
        self.assertEqual(shunting_yard("0(0+1)*1"), "001+*.1.")

    def test_thomsons_construction_empty_regex(self):
        enfa = thomsons_construction("")

        self.assertEqual(enfa.starting_state, "aa")
        self.assertEqual(enfa.final_states, "ab")

        expected_transition_function = {
                ("aa", EPS): "ab"
        }

        self.assertEqual(enfa.transition_function, expected_transition_function)

    def test_thomsons_construction_single_symbol_regex(self):
        enfa = thomsons_construction("0")

        self.assertEqual(enfa.starting_state, "aa")
        self.assertEqual(enfa.final_states, "ab")

        expected_transition_function = {
                ("aa", "0"): "ab"
        }

        self.assertEqual(enfa.transition_function, expected_transition_function)
