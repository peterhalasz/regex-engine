import unittest

from enfa import ENfa, EPS

class ENfaTest(unittest.TestCase):
    def test_enfa_1(self):
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

        e_nfa = ENfa(transition_function, starting_state, final_states)

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

    def test_enfa_2(self):
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

        e_nfa = ENfa(transition_function, starting_state, final_states)

        nfa = e_nfa.convert_to_nfa()

        expected_nfa_tranisition_function = {
            ('A', '0'): {'H'},
            ('H', '1'): {'J', 'E'},
            ('D', '1'): {'J', 'E'},
            ('D', '0'): {'D'},
            ('E', '1'): {'J', 'E'},
            ('E', '0') :{'D'},
            ('H', '0'): {'D'},
        }

        self.assertDictEqual(nfa.transition_function, expected_nfa_tranisition_function)

    def test_enfa_3(self):
        transition_function = {
            ("A", "1"): {"B"},
            ("B", "0"): {"C"},
        }
        starting_state = "A"
        final_states = {"C"}

        e_nfa = ENfa(transition_function, starting_state, final_states)

        nfa = e_nfa.convert_to_nfa()

        expected_nfa_tranisition_function = {
            ("A", "1"): {"B"},
            ("B", "0"): {"C"},
        }

        self.assertDictEqual(nfa.transition_function, expected_nfa_tranisition_function)

    def test_enfa_4(self):
        transition_function = {
            ("A", "1"): {"B"},
            ("B", EPS): {"C"},
        }
        starting_state = "A"
        final_states = {"C"}

        e_nfa = ENfa(transition_function, starting_state, final_states)

        nfa = e_nfa.convert_to_nfa()

        expected_nfa_tranisition_function = {
            ("A", "1"): {"B"},
        }

        self.assertDictEqual(nfa.transition_function, expected_nfa_tranisition_function)

    def test_enfa_5(self):
        transition_function = {
            ("A", "1"): {"B"},
            ("B", EPS): {"C"},
            ("C", EPS): {"D"},
        }
        starting_state = "A"
        final_states = {"D"}

        e_nfa = ENfa(transition_function, starting_state, final_states)

        nfa = e_nfa.convert_to_nfa()

        expected_nfa_tranisition_function = {
            ("A", "1"): {"B"},
        }

        self.assertDictEqual(nfa.transition_function, expected_nfa_tranisition_function)

    def test_enfa_6(self):
        transition_function = {
            ("A", "1"): {"B"},
            ("B", EPS): {"C"},
            ("C", EPS): {"D"},
            ("D", "1"): {"E"},
        }
        starting_state = "A"
        final_states = {"E"}

        e_nfa = ENfa(transition_function, starting_state, final_states)

        nfa = e_nfa.convert_to_nfa()

        expected_nfa_tranisition_function = {
            ("A", "1"): {"B"},
            ("B", "1"): {"E"},
        }

        self.assertDictEqual(nfa.transition_function, expected_nfa_tranisition_function)
