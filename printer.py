from tabulate import tabulate

def print_automaton(transition_function, starting_state, final_states, input_symbols):
    # NOTE: the amount of sorting happening here is a crime and should be seriously punished
    states = set()
    for state, _ in transition_function:
        states.add(state)
    
    table = []
    sorted_input_symbols = sorted(input_symbols)
    for state in sorted(states):
        table_row = ["", state]

        for input_symbol in sorted_input_symbols:
            if (state, input_symbol) in transition_function:
                if len(state) == 1 and starting_state in state:
                    table_row[0] = "->"

                if state in final_states:
                    table_row[0] = "*"

                table_row.append(transition_function[(state, input_symbol)])
        table.append(table_row)

    headers = ['State', *[i for i in sorted_input_symbols]]

    print(tabulate(table, headers=headers))
