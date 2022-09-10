def main():
    # A finite set of states. Usually denoted by Q.
    states = {'A', 'B', 'C'}
    # A finite set of input symbols. Usually denoted by epsilon.
    input_symbols = {'0', '1'}
    # Transition function. Usually denoted by delta.
    # Here implemented as a tuple to string dict.
    # (state, input symbol) -> next state
    transition_function = {
        ('A', '0'): 'A',
        ('A', '1'): 'B',
        ('B', '0'): 'C',
    }
    # Start state. Usually denoted by q0.
    starting_state = 'A'
    # A finite set of accepting / final states. Usually denoted by F.
    # F has to be a subset of Q.
    final_states = {'C'}

    test_input_string = '0000010'

    current_state = starting_state
    for input_symbol in test_input_string:
        print(current_state, input_symbol)

        if (current_state, input_symbol) not in transition_function:
            print("FAILED")
            return

        next_state = transition_function[(current_state, input_symbol)]
        current_state = next_state

        if current_state in final_states:
            print("ACCEPTED")
            return 


if __name__ == "__main__":
    main()
