from tabulate import tabulate


def print_automaton(
    transition_function, starting_state, final_states, is_epsilon=False
):
    input_symbols = ["0", "1"]

    if is_epsilon:
        input_symbols.append("ε")

    states = set()
    for state, _ in transition_function:
        states.add(state)

    table = []
    for state in sorted(states):
        table_row = ["", state]

        for input_symbol in input_symbols:
            if (state, input_symbol) in transition_function:
                if len(state) == 1 and starting_state in state:
                    table_row[0] = "->"

                if state in final_states:
                    table_row[0] = "*"

                table_row.append(transition_function[(state, input_symbol)])
            else:
                table_row.append("-")
        table.append(table_row)

    headers = ["State", *[i for i in input_symbols]]

    print(tabulate(table, headers=headers))
