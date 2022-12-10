import unittest

from dfa import Dfa
from nfa import Nfa
from enfa import ENfa, EPS
from regex import Regex


def compile_and_test_dfa(dfa, input_string):
    return dfa.is_string_accepted(input_string)


def compile_and_test_nfa(nfa, input_string):
    dfa = nfa.convert_to_dfa()

    return dfa.is_string_accepted(input_string)


def compile_and_test_enfa(enfa, input_string):
    nfa = enfa.convert_to_nfa()
    dfa = nfa.convert_to_dfa()

    return dfa.is_string_accepted(input_string)


def compile_and_test_regex(regex, input_string):
    regex = Regex(regex)
    enfa = regex.create_enfa_from_regex()
    nfa = enfa.convert_to_nfa()
    dfa = nfa.convert_to_dfa()

    return dfa.is_string_accepted(input_string)


class MainTest(unittest.TestCase):
    def test_main_dfa_1(self):
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

    def test_main_enfa_1(self):
        transition_function = {
            ("A", "0"): {"H"},
            ("B", EPS): {"C", "I"},
            ("C", EPS): {"F", "G"},
            ("D", EPS): {"B"},
            ("E", EPS): {"B"},
            ("F", "0"): {"D"},
            ("G", "1"): {"E"},
            ("H", EPS): {"C", "I"},
            ("I", "1"): {"J"},
        }
        starting_state = "A"
        final_states = {"J"}

        enfa = ENfa(transition_function, starting_state, final_states)

        self.assertTrue(compile_and_test_enfa(enfa, "011001"))
        self.assertTrue(compile_and_test_enfa(enfa, "0000011001"))
        self.assertTrue(compile_and_test_enfa(enfa, "011001"))

        self.assertFalse(compile_and_test_enfa(enfa, ""))
        self.assertFalse(compile_and_test_enfa(enfa, "1"))
        self.assertFalse(compile_and_test_enfa(enfa, "1011011"))

    def test_main_regex(self):
        regex = "0(0+1)*1"
        self.assertTrue(compile_and_test_regex(regex, "011001"))
        self.assertTrue(compile_and_test_regex(regex, "0000011001"))
        self.assertTrue(compile_and_test_regex(regex, "011001"))

        self.assertFalse(compile_and_test_regex(regex, ""))
        self.assertFalse(compile_and_test_regex(regex, "1"))
        self.assertFalse(compile_and_test_regex(regex, "1011011"))
