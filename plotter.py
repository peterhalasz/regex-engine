import graphviz

START_NODE = "Start"

def plot_automaton(transition_function, starting_state, final_states):
    g = graphviz.Digraph('G', format='png', directory='./out')

    g.attr('node', shape='doublecircle')
    g.graph_attr['rankdir'] = 'LR'

    for final_state in final_states:
        g.node(final_state)

    g.attr('node', shape='circle', style='invisible')
    g.node(START_NODE)

    g.attr('node', shape='circle', style='solid')
    if isinstance(starting_state, str):
        g.edge(START_NODE, starting_state)
    elif isinstance(starting_state, set):
        for state in starting_state:
            g.edge(START_NODE, state)

    for key, next_state in transition_function.items():
        current_state, input_symbol = key
        
        if isinstance(next_state, str):
            g.edge(current_state, next_state, label=input_symbol)
        elif isinstance(next_state, set):
            for elt in next_state:
                g.edge(current_state, elt, label=input_symbol)

    g.view()
