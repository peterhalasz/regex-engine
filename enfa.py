from nfa import Nfa
from plotter import plot_automaton
from utils import validate_automaton, validate_symbols

""" Epsilon Non-deterministic Finite Automaton.

A simple implementation of an e-nfa.
"""

EPS = "ε"

class ENfa():
    def __init__(self, states, input_symbols, transition_function, starting_state, final_states):
        # A finite set of states. Usually denoted by Q.
        self.states = states

        # A finite set of input symbols. Usually denoted by epsilon.
        self.input_symbols = input_symbols

        # Transition function. Usually denoted by delta.
        # Here implemented as a tuple to set of strings dict.
        # (state, input symbol) -> next states
        self.transition_function = transition_function

        # Start state. Usually denoted by q0.
        self.starting_state = starting_state

        # A finite set of accepting / final states. Usually denoted by F.
        # F has to be a subset of Q.
        self.final_states = final_states

    def validate_automaton(self):
        if not validate_automaton(self.input_symbols, self.states, self.starting_state, self.final_states, self.transition_function):
            print("Incorrect automaton")
            return False
        return True

    def plot(self):
        plot_automaton(self.transition_function, self.starting_state, self.final_states)

    def is_string_accepted(self, input_string):
        if not validate_symbols(self.input_symbols, input_string):
            print("Input string is not part of the input symbols")
            return False
        print("Not implemented")
        return False

    def convert_to_nfa(self):
        for k, v in self.transition_function.items():
            print(k, v)

        eps_transitions = {}
        # Step 1 - Find eps transitions (v1 - v2)
        for state, symbol in self.transition_function:
            if symbol == EPS:
                eps_transitions[(state, symbol)] = self.transition_function[(state, symbol)]


        print("====")
        for k, v in eps_transitions.items():
            print(k, v)

        print("====")

        # Step 2
        # Find all moves that start from the end state (v2) of the eps transition
        # Duplicate those with the same input (v1 - v2) and the end state from the v2-n
        # transition.
        # Remove the eps transitions.
        nfa_transition_function = {}

        for state, symbol in self.transition_function:
            if (state, symbol) in eps_transitions:
                end_states = eps_transitions[(state, symbol)]

                transitions_from_eps_end_state = {k:v for k,v in self.transition_function.items() if k[0] in end_states}

                for k, v in transitions_from_eps_end_state.items():
                    if (state, k[1]) in nfa_transition_function.keys():
                        nfa_transition_function[(state, k[1])] = v.union(nfa_transition_function[(state, k[1])])
                    else:
                        nfa_transition_function[(state, k[1])] = v

            else:
                if (state, symbol) in nfa_transition_function.keys():
                    old = nfa_transition_function[(state, symbol)]
                    nfa_transition_function[(state, symbol)] = old.union(nfa_transition_function[(state, symbol)])
                else:
                    nfa_transition_function[(state, symbol)] = self.transition_function[(state, symbol)]
                

        # Step 3 - If v1 is a starting state v2 is also a starting state

        # Step 4 - If v2 is a final state, v1 is also a final state

        nfa = Nfa(
            None,
            None,
            nfa_transition_function,
            None,
            None,
        )

        return nfa



if __name__ == "__main__":
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

    # The string the e-nfa will process.
    test_input_string = "0000011001"

    e_nfa = ENfa(states, input_symbols, transition_function, starting_state, final_states)

    e_nfa.convert_to_nfa()

    #e_nfa.plot()
