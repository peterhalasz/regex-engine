from plotter import plot_automaton
from utils import validate_automaton, validate_symbols
from tabulate import tabulate

""" Deterministic Finite Automaton.

A simple implementation of a dfa.
"""
class Dfa():
    def __init__(self, states, input_symbols, transition_function, starting_state, final_states):
        # A finite set of states. Usually denoted by Q.
        self.states = states

        # A finite set of input symbols. Usually denoted by epsilon.
        self.input_symbols = input_symbols

        # Transition function. Usually denoted by delta.
        # Here implemented as a tuple to string dict.
        # (state, input symbol) -> next state
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

    def print(self):
        # NOTE: the amount of sorting happening here is a crime and should be seriously punished
        dfa_states = set()
        for dfa_state, _ in self.transition_function:
            dfa_states.add(dfa_state)
        
        table = []
        sorted_input_symbols = sorted(self.input_symbols)
        for dfa_state in dfa_states:
            table_row = ["", dfa_state]

            for input_symbol in sorted_input_symbols:
                if (dfa_state, input_symbol) in self.transition_function:
                    if len(dfa_state) == 1 and self.starting_state in dfa_state:
                        table_row[0] = "->"

                    print(self.final_states, dfa_state)

                    if dfa_state in self.final_states:
                        table_row[0] = "*"

                    table_row.append(self.transition_function[(dfa_state, input_symbol)])
            table.append(table_row)

        headers = ['State', *[i for i in sorted_input_symbols]]

        print(tabulate(table, headers=headers))

    def is_string_accepted(self, input_string):
        if not validate_symbols(self.input_symbols, input_string):
            print("Input string is not part of the input symbols")
            return False

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

if __name__ == "__main__":
    states = {"A", "B", "C", "D", "E", "F", "G"}
    input_symbols = {"0", "1"}
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

    # The string the dfa will process.
    test_input_string = "0000011001"

    dfa = Dfa(states, input_symbols, transition_function, starting_state, final_states)

    dfa.is_string_accepted(test_input_string)
    dfa.plot()
