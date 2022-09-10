from plotter import plot_automaton
from utils import validate_automaton

def main():
    # A finite set of states. Usually denoted by Q.
    states = {"A", "B", "C", "D", "E", "F", "G"}
    # A finite set of input symbols. Usually denoted by epsilon.
    input_symbols = {"0", "1"}
    # Transition function. Usually denoted by delta.
    # Here implemented as a tuple to string dict.
    # (state, input symbol) -> next state
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
    # Start state. Usually denoted by q0.
    starting_state = "A"
    # A finite set of accepting / final states. Usually denoted by F.
    # F has to be a subset of Q.
    final_states = {"G"}

    plot_automaton(transition_function, starting_state, final_states)

    test_input_string = "0000011001"

    if not validate_automaton(input_symbols, test_input_string, states, starting_state,
            final_states, transition_function):
        print("Incorrect automaton")
        return

    current_state = starting_state
    for input_symbol in test_input_string:
        print(current_state, input_symbol)

        if (current_state, input_symbol) not in transition_function:
            print("FAILED")
            return

        current_state = transition_function[(current_state, input_symbol)]

        if current_state in final_states:
            print("ACCEPTED")
            return 


    print("FAILED")
    return

if __name__ == "__main__":
    main()

