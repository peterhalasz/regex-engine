from plotter import plot_automaton
from printer import print_automaton

""" Deterministic Finite Automaton.

A simple implementation of a dfa.
"""


class Dfa:
    def __init__(self, transition_function, starting_state, final_states):
        # Transition function. Usually denoted by delta.
        # Here implemented as a tuple to string dict.
        # (state, input symbol) -> next state
        self.transition_function = transition_function

        # Start state. Usually denoted by q0.
        self.starting_state = starting_state

        # A finite set of accepting / final states. Usually denoted by F.
        # F has to be a subset of Q.
        self.final_states = final_states

    def plot(self):
        plot_automaton(self.transition_function, self.starting_state, self.final_states)

    def print(self):
        print_automaton(
            self.transition_function, self.starting_state, self.final_states
        )

    def is_string_accepted(self, input_string):
        current_state = self.starting_state
        for input_symbol in input_string:

            if (current_state, input_symbol) not in self.transition_function:
                print("FAILED - Does not terminate")
                return False

            current_state = self.transition_function[(current_state, input_symbol)]

        if current_state in self.final_states:
            print("ACCEPTED")
            return True
        else:
            print("FAILED - Ended in a non-final state")
            return False
