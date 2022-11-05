import unittest

from dfa import Dfa

class DfaTest(unittest.TestCase):
    def test_dfa_1(self):
        transition_function = {
            ("A", "0"): "A",
            ("A", "1"): "B",
            ("B", "0"): "C",
            ("B", "1"): "D",
            ("C", "1"): "E",
            ("D", "0"): "E",
            ("E", "0"): "F",
            ("F", "1"): "G",
        }
        starting_state = "A"
        final_states = {"G"}
        dfa = Dfa(transition_function, starting_state, final_states)

        self.assertTrue(dfa.is_string_accepted("0000011001"))
        self.assertTrue(dfa.is_string_accepted("011001"))

        self.assertFalse(dfa.is_string_accepted(""))
        self.assertFalse(dfa.is_string_accepted("1"))
        self.assertFalse(dfa.is_string_accepted("1011001"))


    def test_dfa_2(self):
        transition_function = {
            ("A", "0"): "B",
        }
        starting_state = "A"
        final_states = {"B"}
        dfa = Dfa(transition_function, starting_state, final_states)

        self.assertTrue(dfa.is_string_accepted("0"))

        self.assertFalse(dfa.is_string_accepted(""))
        self.assertFalse(dfa.is_string_accepted("1"))
        self.assertFalse(dfa.is_string_accepted("01"))
