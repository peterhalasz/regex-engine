import printer
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

    def _remove_inaccessable_nodes(self, transition_function, starting_state):
        result_transition_function = {}

        transition_end_nodes = [node for nodes in transition_function.values() for node in nodes]

        for transition in transition_function:
            if transition[0] == starting_state or transition[0] in transition_end_nodes:
                result_transition_function[transition] = transition_function[transition]

        return result_transition_function

    def _remove_eps_transitions(self, transition_function):
        eps_transitions = {k:v for k,v in transition_function.items() if k[1] == EPS}
        nfa_transition_function = {k:v for k,v in transition_function.items() if k[1] != EPS}

        for eps_transition in eps_transitions:
            transitions_from_eps_end_state = {k:v for k,v in transition_function.items() if k[0] in transition_function[eps_transition]}
            
            for eps_end_transition in transitions_from_eps_end_state:
                print(f"Deleting et {eps_transition}->{eps_transitions[eps_transition]}, adding {(eps_transition[0], eps_end_transition[1])} -> {transitions_from_eps_end_state[eps_end_transition]}")

                #if transitions_from_eps_end_state[eps_end_transition].intersection(self.final_states):
                    #print("FINAL: ", transitions_from_eps_end_state[eps_end_transition], "adding ", eps_transition[0])
                #    self.final_states = self.final_states.union({eps_transition[0]})

                if (eps_transition[0], eps_end_transition[1]) in nfa_transition_function.keys():
                    nfa_transition_function[(eps_transition[0], eps_end_transition[1])] = nfa_transition_function[(eps_transition[0], eps_end_transition[1])].union(transitions_from_eps_end_state[eps_end_transition])
                else:
                    nfa_transition_function[(eps_transition[0], eps_end_transition[1])] = transitions_from_eps_end_state[eps_end_transition] 
        
        return nfa_transition_function

    def convert_to_nfa_2(self):
        nfa_starting_state = self.starting_state
        nfa_final_states = self.final_states

        nfa_transition_function = {k:v for k,v in self.transition_function.items() }

        while True:
            nfa_transition_function = self._remove_eps_transitions(nfa_transition_function)

            e = {k:v for k,v in nfa_transition_function.items() if k[1] == EPS}
            if not e:
                break


        nfa_transition_function = self._remove_inaccessable_nodes(nfa_transition_function, nfa_starting_state)

        nfa = Nfa(
            self.states,
            self.input_symbols,
            nfa_transition_function,
            nfa_starting_state,
            self.final_states,
        )

        print(self.final_states)

        return nfa

    def convert_to_nfa(self):
        nfa_starting_states = {self.starting_state}
        nfa_final_states = self.final_states

        eps_transitions = {}
        # Step 1 - Find eps transitions (v1 - v2)
        for state, symbol in self.transition_function:
            if symbol == EPS:
                eps_transitions[(state, symbol)] = self.transition_function[(state, symbol)]

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

                    # Step 3 - If v1 is a starting state v2 is also a starting state
                    if state in self.starting_state:
                        nfa_starting_states = nfa_starting_states.union({k[0]})
                    # Step 4 - If v2 is a final state, v1 is also a final state
                    if k[0] in self.final_states:
                        nfa_final_states = nfa_final_states.union({state})
            else:
                if (state, symbol) in nfa_transition_function.keys():
                    old = nfa_transition_function[(state, symbol)]
                    nfa_transition_function[(state, symbol)] = old.union(nfa_transition_function[(state, symbol)])
                else:
                    nfa_transition_function[(state, symbol)] = self.transition_function[(state, symbol)]

        nfa = Nfa(
            self.states,
            self.input_symbols,
            nfa_transition_function,
            nfa_starting_states,
            nfa_final_states,
        )

        return nfa

if __name__ == "__main__":
    states = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J"}
    input_symbols = {"0", "1", EPS}
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

    e_nfa = ENfa(states, input_symbols, transition_function, starting_state, final_states)
    #e_nfa.plot()

    nfa = e_nfa.convert_to_nfa_2()
    print(nfa.transition_function)
    #nfa.plot()
    for k,v in nfa.transition_function.items():
        print(k, v)

    #printer.print_automaton(e_nfa.transition_function, e_nfa.starting_state, e_nfa.final_states, e_nfa.input_symbols)

