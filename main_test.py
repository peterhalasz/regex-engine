import unittest

from dfa import Dfa
from nfa import Nfa

from main import compile_and_test_dfa, compile_and_test_nfa

class MainTest(unittest.TestCase):
    def test_main_dfa_1(self):
        transition_function = {
            ("A", "0"): "A", ("A", "1"): "B",
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

        self.assertTrue(compile_and_test_dfa(dfa, "011001"))
        self.assertTrue(compile_and_test_dfa(dfa, "0000011001"))
        self.assertTrue(compile_and_test_dfa(dfa, "011001"))

        self.assertFalse(compile_and_test_dfa(dfa, ""))
        self.assertFalse(compile_and_test_dfa(dfa, "1"))
        self.assertFalse(compile_and_test_dfa(dfa, "1011001"))

    def test_main_nfa_1(self):
        transition_function = {
            ("A", "0"): {"A", "B"},
            ("A", "1"): {"A"},
            ("B", "1"): {"C"},
        }
        starting_state = "A"
        final_states = {"C"}

        nfa = Nfa(transition_function, starting_state, final_states)

        self.assertTrue(compile_and_test_nfa(nfa, "011001"))
        self.assertTrue(compile_and_test_nfa(nfa, "0000011001"))
        self.assertTrue(compile_and_test_nfa(nfa, "011001"))

        self.assertFalse(compile_and_test_nfa(nfa, ""))
        self.assertFalse(compile_and_test_nfa(nfa, "1"))
        self.assertFalse(compile_and_test_nfa(nfa, "1011011"))
