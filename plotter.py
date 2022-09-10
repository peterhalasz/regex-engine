import graphviz

START_NODE = "Start"

def plot_automaton(transition_function, starting_state, final_states):
    g = graphviz.Digraph('G', format='png', directory='./out')

    g.attr('node', shape='doublecircle')
    for final_state in final_states:
        g.node(final_state)

    g.attr('node', shape='circle', style='invisible')
    g.node(START_NODE)

    g.attr('node', shape='circle', style='solid')
    g.edge(START_NODE, starting_state)

    for key, next_state in transition_function.items():
        current_state, input_symbol = key
        
        g.edge(current_state, next_state, label=input_symbol)

    g.view()
