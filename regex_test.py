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
        self.assertEqual(enfa.final_states, {"ab"})

        expected_transition_function = {
                ("aa", EPS): {"ab"}
        }

        self.assertEqual(enfa.transition_function, expected_transition_function)

    def test_thomsons_construction_single_symbol_regex(self):
        enfa = thomsons_construction("0")

        self.assertEqual(enfa.starting_state, "aa")
        self.assertEqual(enfa.final_states, {"ab"})

        expected_transition_function = {
                ("aa", "0"): {"ab"}
        }

        self.assertEqual(enfa.transition_function, expected_transition_function)

    def test_thomsons_construction_single_union_regex(self):
        enfa = thomsons_construction("01+")

        self.assertEqual(enfa.starting_state, "ae")
        self.assertEqual(enfa.final_states, {"af"})

        self.assertEqual(len(enfa.transition_function), 5)
        self.assertEqual(enfa.transition_function[("aa", "0")], {"ab"})
        self.assertEqual(enfa.transition_function[("ac", "1")], {"ad"})
        self.assertEqual(enfa.transition_function[("ae", EPS)], {"aa", "ac"})
        self.assertEqual(enfa.transition_function[("ab", EPS)], {"af"})
        self.assertEqual(enfa.transition_function[("ad", EPS)], {"af"})

    def test_thomsons_construction_single_concatenation_regex(self):
        enfa = thomsons_construction("01.")

        self.assertEqual(enfa.starting_state, "aa")
        self.assertEqual(enfa.final_states, {"ad"})

        self.assertEqual(len(enfa.transition_function), 2)
        self.assertEqual(enfa.transition_function[("aa", "0")], {"ae"})
        self.assertEqual(enfa.transition_function[("ae", "1")], {"ad"})

    def test_thomsons_construction_single_kleene_star_regex(self):
        enfa = thomsons_construction("0*")

        self.assertEqual(enfa.starting_state, "ac")
        self.assertEqual(enfa.final_states, {"ad"})

        self.assertEqual(len(enfa.transition_function), 3)
        self.assertEqual(enfa.transition_function[("ac", EPS)], {"aa", "ad"})
        self.assertEqual(enfa.transition_function[("aa", "0")], {"ab"})
        self.assertEqual(enfa.transition_function[("ab", EPS)], {"aa", "ad"})

    def test_thomsons_construction_double_concatenation_regex(self):
        enfa = thomsons_construction("01.0.")

        self.assertEqual(enfa.starting_state, "aa")
        self.assertEqual(enfa.final_states, {"ag"})

        self.assertEqual(len(enfa.transition_function), 3)
        self.assertEqual(enfa.transition_function[("aa", "0")], {"ae"})
        self.assertEqual(enfa.transition_function[("ae", "1")], {"ah"})
        self.assertEqual(enfa.transition_function[("ah", "0")], {"ag"})

    def test_thomsons_construction_union_and_concatenation_regex(self):
        enfa = thomsons_construction("01+0.")

        self.assertEqual(enfa.starting_state, "ae")
        self.assertEqual(enfa.final_states, {"ah"})

        self.assertEqual(len(enfa.transition_function), 6)
        self.assertEqual(enfa.transition_function[("aa", "0")], {"ab"})
        self.assertEqual(enfa.transition_function[("ac", "1")], {"ad"})
        self.assertEqual(enfa.transition_function[("ae", EPS)], {"aa", "ac"})
        self.assertEqual(enfa.transition_function[("ab", EPS)], {"ai"})
        self.assertEqual(enfa.transition_function[("ad", EPS)], {"ai"})
        self.assertEqual(enfa.transition_function[("ai", "0")], {"ah"})

    def test_thomsons_construction_1(self):
        enfa = thomsons_construction("001+*.1.")

        self.assertEqual(enfa.starting_state, "aa")
        self.assertEqual(enfa.final_states, {"am"})

        self.assertEqual(len(enfa.transition_function), 9)
        self.assertEqual(enfa.transition_function[('aa', '0')], {'ak'})
        self.assertEqual(enfa.transition_function[('ah', 'ε')], {'ag', 'aj'})
        self.assertEqual(enfa.transition_function[('ag', 'ε')], {'ae', 'ac'})
        self.assertEqual(enfa.transition_function[('ad', 'ε')], {'ah'})
        self.assertEqual(enfa.transition_function[('af', 'ε')], {'ah'})
        self.assertEqual(enfa.transition_function[('ac', '0')], {'ad'})
        self.assertEqual(enfa.transition_function[('ae', '1')], {'af'})
        self.assertEqual(enfa.transition_function[('ak', 'ε')], {'ag', 'aj'})
        self.assertEqual(enfa.transition_function[('an', '1')], {'am'})
