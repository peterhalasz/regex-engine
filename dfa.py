from plotter import plot_automaton
from printer import print_automaton

""" Deterministic Finite Automaton."""


class Dfa:
    def __init__(self, transition_function, starting_state, final_states):
        # Here implemented as a tuple to string dict.
        # (state, input symbol) -> next state
        self.transition_function = transition_function

        self.starting_state = starting_state

        # A finite set of accepting / final states.
        self.final_states = final_states

    def plot(self):
        plot_automaton(self.transition_function, self.starting_state, self.final_states)

    def print(self):
        print_automaton(
            self.transition_function, self.starting_state, self.final_states
        )

    def is_string_accepted(self, input_string):
        """Check if the string is accepted by the DFA.

        Args:
            input_string: the input to check.

        Returns:
            True if the automaton accepts the string, False otherwise.
        """
        current_state = self.starting_state
        for input_symbol in input_string:

            if (current_state, input_symbol) not in self.transition_function:
                # The automaton does not terminate
                return False

            current_state = self.transition_function[(current_state, input_symbol)]

        if current_state in self.final_states:
            return True
        else:
            # The automaton terminates in a non-final state
            return False
