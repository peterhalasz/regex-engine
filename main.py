from dfa import Dfa

def compile_and_test_dfa(dfa, input_string):
    return dfa.is_string_accepted(input_string)

def compile_and_test_nfa(nfa, input_string):
    dfa = nfa.convert_to_dfa()

    return dfa.is_string_accepted(input_string)
