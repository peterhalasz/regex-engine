from nfa import Nfa
from plotter import plot_automaton
from printer import print_automaton

""" Epsilon Non-deterministic Finite Automaton.

A simple implementation of an e-nfa.
"""

EPS = "ε"


class ENfa:
    def __init__(self, transition_function, starting_state, final_states):
        # Transition function. Usually denoted by delta.
        # Here implemented as a tuple to set of strings dict.
        # (state, input symbol) -> next states
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
            self.transition_function,
            self.starting_state,
            self.final_states,
            is_epsilon=True,
        )

    def _remove_inaccessable_nodes(self, transition_function, starting_state):
        result_transition_function = {}

        transition_end_nodes = [
            node for nodes in transition_function.values() for node in nodes
        ]

        for transition in transition_function:
            if transition[0] == starting_state or transition[0] in transition_end_nodes:
                result_transition_function[transition] = transition_function[transition]

        return result_transition_function

    def _remove_eps_transitions(self, transition_function):
        eps_transitions = {k: v for k, v in transition_function.items() if k[1] == EPS}
        nfa_transition_function = {
            k: v for k, v in transition_function.items() if k[1] != EPS
        }

        for eps_transition in eps_transitions:
            transitions_from_eps_end_state = {
                k: v
                for k, v in transition_function.items()
                if k[0] in transition_function[eps_transition]
            }

            # TODO: This is not nice. Extract instead of manipulating enfa.
            end_states = eps_transitions[eps_transition]
            if end_states.intersection(self.final_states):
                self.final_states.add(eps_transition[0])

            for eps_end_transition in transitions_from_eps_end_state:
                if (
                    eps_transition[0],
                    eps_end_transition[1],
                ) in nfa_transition_function.keys():
                    nfa_transition_function[
                        (eps_transition[0], eps_end_transition[1])
                    ] = nfa_transition_function[
                        (eps_transition[0], eps_end_transition[1])
                    ].union(
                        transitions_from_eps_end_state[eps_end_transition]
                    )
                else:
                    nfa_transition_function[
                        (eps_transition[0], eps_end_transition[1])
                    ] = transitions_from_eps_end_state[eps_end_transition]

        return nfa_transition_function

    def convert_to_nfa(self):
        nfa_starting_state = self.starting_state

        nfa_transition_function = {k: v for k, v in self.transition_function.items()}

        while True:
            nfa_transition_function = self._remove_eps_transitions(
                nfa_transition_function
            )

            eps_transitions = {
                k: v for k, v in nfa_transition_function.items() if k[1] == EPS
            }
            if not eps_transitions:
                break

        nfa_transition_function = self._remove_inaccessable_nodes(
            nfa_transition_function, nfa_starting_state
        )

        nfa = Nfa(
            nfa_transition_function,
            nfa_starting_state,
            self.final_states,
        )

        return nfa
