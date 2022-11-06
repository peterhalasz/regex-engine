def validate_symbols(input_symbols, input_string):
    for input_symbol in input_string:
        if input_symbol not in input_symbols:
            return False
    return True


def validate_states(states, starting_state, final_states):
    if starting_state not in states:
        return False
    for final_state in final_states:
        if final_state not in states:
            return False
    return True


def validate_transitions(states, input_symbols, transition_function):
    for key, next_state in transition_function.items():
        current_state, input_symbol = key
        if current_state not in states:
            return False
        if input_symbol not in input_symbols:
            return False
        if next_state not in states:
            return False
    return True


def validate_automaton(
    input_symbols, states, starting_state, final_states, transition_function
):
    return validate_states(
        states, starting_state, final_states
    ) and validate_transitions(states, input_symbols, transition_function)
