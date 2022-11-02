from enfa import ENfa, EPS

KLEENEE = ("*", 2)
CONCATENATION = (".", 1)
UNION = ("+", 0)

ALPHABET = {"0", "1"}
OPERATORS = {KLEENEE[0], CONCATENATION[0], UNION[0]}

def node_name_generator():
    for i in range(ord('a'),ord('z')+1):
        for j in range(ord('a'),ord('z')+1):
            yield chr(i)+chr(j)

def _get_operator(operator):
    if operator == "*":
        return KLEENEE
    elif operator == ".":
        return CONCATENATION
    else:
        return UNION

def _is_operator_higher_precedence(operator1, operator2):
    return _get_operator(operator1)[1] >= _get_operator(operator2)[1]

def _add_explicit_concatenation_symbols(regex):
    new_regex = ""

    prev = ""
    for c in regex:
        if (c in ALPHABET and (prev in ALPHABET or prev == ')' or prev == '*')) or (c == '(' and
                prev in ALPHABET):
            new_regex += "."

        new_regex += c
        prev = c

    return new_regex

def shunting_yard(regex):
    regex = _add_explicit_concatenation_symbols(regex)

    output = ""
    operator_stack = []

    for symbol in regex:
        if symbol in ALPHABET:
            output += symbol
        elif symbol in OPERATORS:
            if operator_stack:
                top_operator = operator_stack[-1]

                if top_operator != "(":
                    while _is_operator_higher_precedence(top_operator, symbol):
                        output += operator_stack.pop()
                        if operator_stack:
                            top_operator = operator_stack[-1]
                        else:
                            break

            operator_stack.append(symbol)
        elif symbol == "(":
           operator_stack.append("(")
        elif symbol == ")":
            while operator_stack and operator_stack[-1] != "(":
                output += operator_stack.pop()
            operator_stack.pop()

    while operator_stack:
        output += operator_stack.pop()

    return output

def _handle_empty_expression(node_gen):
    starting_state = node_gen.__next__()
    final_state = node_gen.__next__()

    enfa = ENfa(
        (starting_state, final_state),
        ("0", "1"),
        {
            (starting_state, EPS): {final_state},
        },
        starting_state,
        {final_state},
    )

    return enfa

def _handle_symbol(symbol, node_gen):
    starting_state = node_gen.__next__()
    final_state = node_gen.__next__()

    enfa = ENfa(
        (starting_state, final_state),
        ("0", "1"),
        {
            (starting_state, symbol): {final_state},
        },
        starting_state,
        {final_state},
    )

    return enfa

def _handle_union(enfa1, enfa2, node_gen):
    starting_state = node_gen.__next__()
    final_state = node_gen.__next__()
    
    enfa = ENfa(
        (starting_state, final_state),
        ("0", "1"),
        {
            (starting_state, EPS): {enfa1.starting_state, enfa2.starting_state},
            (list(enfa1.final_states)[0], EPS): {final_state},
            (list(enfa2.final_states)[0], EPS): {final_state},
        },
        starting_state,
        {final_state}
    )

    for k, v in enfa1.transition_function.items():
        enfa.transition_function[k] = v

    for k, v in enfa2.transition_function.items():
        enfa.transition_function[k] = v

    return enfa

def _handle_concatenation(enfa1, enfa2, node_gen):
    new_mid_state = node_gen.__next__()
    
    enfa = ENfa(
        # TODO: Compute states or remove field from enfa
        (),
        ("0", "1"),
        {},
        enfa1.starting_state,
        enfa2.final_states,
    )

    for k, v in enfa1.transition_function.items():
        enfa.transition_function[k] = v

    for k, v in enfa2.transition_function.items():
        enfa.transition_function[k] = v

    for k, v in enfa.transition_function.items():
        if v == enfa1.final_states:
            enfa.transition_function[k] = {new_mid_state}
            break

    for k, v in enfa.transition_function.items():
        if k[0] == enfa2.starting_state:
            enfa.transition_function[(new_mid_state, k[1])] = v
            del enfa.transition_function[k]
            break

    return enfa

def _handle_kleene_star(enfa1, node_gen):
    starting_state = node_gen.__next__()
    final_state = node_gen.__next__()
    
    enfa = ENfa(
        (starting_state, final_state),
        ("0", "1"),
        {
            (starting_state, EPS): {final_state, enfa1.starting_state},
            (list(enfa1.final_states)[0], EPS): {final_state, enfa1.starting_state},
        },
        starting_state,
        {final_state},
    )

    for k, v in enfa1.transition_function.items():
        enfa.transition_function[k] = v

    return enfa

def thomsons_construction(regex):
    node_gen = node_name_generator()

    if regex == '':
        return _handle_empty_expression(node_gen)

    if regex == '0':
        return _handle_symbol(regex, node_gen)

    if regex == '01+':
        enfa1 = _handle_symbol("0", node_gen)
        enfa2 = _handle_symbol("1", node_gen)

        return _handle_union(enfa1, enfa2, node_gen)

    if regex == '01.':
        enfa1 = _handle_symbol("0", node_gen)
        enfa2 = _handle_symbol("1", node_gen)

        return _handle_concatenation(enfa1, enfa2, node_gen)

    if regex == '0*':
        enfa1 = _handle_symbol("0", node_gen)

        return _handle_kleene_star(enfa1, node_gen)

if __name__ == "__main__":
    regex = "0(0+1)*1"
    print(regex)
    regex = shunting_yard(regex)
    print(regex)
    enfa = thomsons_construction("01.")
    print(enfa)
    print(enfa.transition_function)


