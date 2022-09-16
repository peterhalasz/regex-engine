from dfa import Dfa
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
        dfa_accepting_states = set()

        # A dict of a tuple of a set of states and an input symbol to a set of states
        dfa_transition_function = {}

        # Add the nfa transitions to the dfa's transition function
        # Create a list states that are reachable
        reachable_states = []
        for key, next_states in self.transition_function.items():
            current_state, input_symbol = key
            dfa_transition_function[(frozenset(current_state), input_symbol)] = next_states
            
            reachable_states.append(next_states)
        
        # Constructing the nfa transition function lazily
        for next_states in reachable_states:
            for input_symbol in self.input_symbols:

                combined_next_states = set()

                # Iterate over all states of the nfa
                # Collect all nfa reachable states from that state
                # This nfa state can include multiple dfa states
                for state in next_states:
                    if (state, input_symbol) in self.transition_function:
                        nfa_next_states = self.transition_function[(state, input_symbol)]
                        for nfa_next_state in nfa_next_states:
                            combined_next_states.add(nfa_next_state)


                if combined_next_states:
                    dfa_transition_function[(frozenset(next_states), input_symbol)] = combined_next_states

                    if combined_next_states != next_states and combined_next_states not in reachable_states:
                        reachable_states.append(combined_next_states)

        # Delete entires that are not reaching a state and unreachable states
        entries_to_delete = []
        for key, next_states in dfa_transition_function.items():
            state, input_symbol = key

            if state not in dfa_transition_function.values():
                for symbol in self.input_symbols:
                    if (state, symbol) in dfa_transition_function:
                        entries_to_delete.append((state, symbol))

            all_end_states_from_other_states = [v if k[0] != state else None for k,v in dfa_transition_function.items()]
            if state not in all_end_states_from_other_states and ",".join(state) != self.starting_state:
                for symbol in self.input_symbols:
                    if (state, symbol) in dfa_transition_function:
                        entries_to_delete.append((state, symbol))

        for entry in entries_to_delete:
            if entry in dfa_transition_function:
                del dfa_transition_function[entry]

        # Creating the dfa's accepting states
        for state, _ in dfa_transition_function:
            if state.intersection(self.final_states):
                dfa_accepting_states.add(state)

        # Create the dfa
        dfa_transition_function_2 = {}
        for key, next_states in dfa_transition_function.items():
            dfa_state, input_symbol = key
            dfa_transition_function_2[",".join(sorted(dfa_state)), input_symbol] = ",".join(sorted(next_states))

        
        dfa_accepting_states_2 = [",".join(sorted(s)) for s in dfa_accepting_states]

        dfa = Dfa(
            states=self.states,
            input_symbols=self.input_symbols,
            transition_function=dfa_transition_function_2,
            starting_state=self.starting_state,
            final_states=dfa_accepting_states_2,
        )

        return dfa

    def is_string_accepted(self, input_string):
        if not validate_symbols(self.input_symbols, input_string):
            print("Input string is not part of the input symbols")
            return False
        print("Not implemented")
        return False


if __name__ == "__main__":
    states = {"A", "B", "C"}
    input_symbols = {"0", "1"}
    transition_function = {
        ("A", "0"): {"A"},
        ("A", "1"): {"B"},
        ("B", "0"): {"B", "C"},
        ("B", "1"): {"B"},
        ("C", "0"): {"C"},
        ("C", "1"): {"B", "C"},
    }
    starting_state = "A"
    final_states = {"C"}

    nfa = Nfa(states, input_symbols, transition_function, starting_state, final_states)
    dfa = nfa.convert_to_dfa()
    dfa.print()
