from regex import create_enfa_from_regex


def compile_and_test_dfa(dfa, input_string):
    return dfa.is_string_accepted(input_string)


def compile_and_test_nfa(nfa, input_string):
    dfa = nfa.convert_to_dfa()

    return dfa.is_string_accepted(input_string)


def compile_and_test_enfa(enfa, input_string):
    nfa = enfa.convert_to_nfa()
    dfa = nfa.convert_to_dfa()

    return dfa.is_string_accepted(input_string)


def compile_and_test_regex(regex, input_string):
    enfa = create_enfa_from_regex(regex)
    nfa = enfa.convert_to_nfa()
    dfa = nfa.convert_to_dfa()

    return dfa.is_string_accepted(input_string)
