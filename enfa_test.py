import unittest

from enfa import ENfa, EPS

class ENfaTest(unittest.TestCase):
    def test_enfa_1(self):
        states = {"A", "B", "C", "D", "E"}
        input_symbols = {"0", "1", EPS}
        transition_function = {
            ("A", "1"): {"B"},
            ("B", "1"): {"A"},
            ("A", EPS): {"C"},
            ("C", "0"): {"D"},
            ("D", "0"): {"C"},
            ("C", "1"): {"E"},
            ("E", "0"): {"C"},
        }
        starting_state = "A"
        final_states = {"C"}

        e_nfa = ENfa(states, input_symbols, transition_function, starting_state, final_states)

        nfa = e_nfa.convert_to_nfa()

        expected_nfa_tranisition_function = {
            ('A', '0'): {'D'},
            ('A', '1'): {'B', 'E'},
            ('B', '1'): {'A'},
            ('C', '0'): {'D'},
            ('C', '1'): {'E'},
            ('D', '0'): {'C'},
            ('E', '0'): {'C'},
        }

        self.assertDictEqual(nfa.transition_function, expected_nfa_tranisition_function)
