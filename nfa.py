from tabulate import tabulate
from plotter import plot_automaton
from utils import validate_automaton, validate_symbols

""" Non-deterministic Finite Automaton.

A simple implementation of an nfa.
"""
class Nfa():
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

    def convert_to_dfa(self):
        dfa_input_symbols = self.input_symbols
        dfa_starting_state = {self.starting_state}
        dfa_accepting_states = set()

        # A dict of a tuple of a set of states and an input symbol to a set of states
        dfa_transition_function = {}

        reachable_states = []
        for key, next_states in self.transition_function.items():
            current_state, input_symbol = key
            dfa_transition_function[(frozenset(current_state), input_symbol)] = next_states
            
            reachable_states.append(next_states)
        
        for next_states in reachable_states:
            for input_symbol in self.input_symbols:

                combined_next_states = set()
                for state in next_states:
                    if (state, input_symbol) in self.transition_function:
                        n = self.transition_function[(state, input_symbol)]
                        for x in n:
                            combined_next_states.add(x)

                if combined_next_states:
                    dfa_transition_function[(frozenset(next_states), input_symbol)] = combined_next_states

                    if next_states.intersection(self.final_states):
                        dfa_accepting_states.add(frozenset(next_states))

                    if combined_next_states != next_states and combined_next_states not in reachable_states:
                        reachable_states.append(combined_next_states)


        # Printing the dfa as a table
        # NOTE: the amount of sorting happening here is a crime and should be seriously punished
        dfa_states = set()
        for dfa_state, _ in dfa_transition_function:
            dfa_states.add(dfa_state)

        table = []
        for dfa_state in dfa_states:
            table_row = ["", sorted(list(dfa_state))]
            for input_symbol in sorted(self.input_symbols):
                if (dfa_state, input_symbol) in dfa_transition_function:
                    if len(dfa_state) == 1 and self.starting_state in dfa_state:
                        table_row[0] = "->"

                    if set(dfa_state) in dfa_accepting_states:
                        table_row[0] = "*"

                    table_row.append(sorted(dfa_transition_function[(dfa_state, input_symbol)]))
            table.append(table_row)

        headers = ['State', *[i for i in sorted(self.input_symbols)]]
        print(tabulate(sorted(table), headers=headers))

    def is_string_accepted(self, input_string):
        if not validate_symbols(self.input_symbols, input_string):
            print("Input string is not part of the input symbols")
            return False
        print("Not implemented")
        return False

if __name__ == "__main__":
    states = {"A", "B", "C", "D"}
    input_symbols = {"0", "1"}
    transition_function = {
        ("A", "0"): {"A", "B"},
        ("A", "1"): {"B"},
        ("B", "0"): {"C"},
        ("B", "1"): {"A", "C"},
        ("C", "1"): {"D"},
    }
    starting_state = "A"
    final_states = {"D"}

    # The string the dfa will process.
    test_input_string = "0000011001"

    nfa = Nfa(states, input_symbols, transition_function, starting_state, final_states)

    #nfa.plot()
    nfa.convert_to_dfa()
