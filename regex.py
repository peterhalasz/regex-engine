KLEENEE = ("*", 2)
CONCATENATION = (".", 1)
UNION = ("+", 0)

ALPHABET = {"0", "1"}
OPERATORS = {KLEENEE[0], CONCATENATION[0], UNION[0]}

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

if __name__ == "__main__":
    regex = "0(0+1)*1"
    print(regex)
    output = shunting_yard(regex)
    print(output)
