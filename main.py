from regex import create_enfa_from_regex


def compile_and_test_regex(regex, input_string):
    enfa = create_enfa_from_regex(regex)
    nfa = enfa.convert_to_nfa()
    dfa = nfa.convert_to_dfa()

    return dfa.is_string_accepted(input_string)


if __name__ == "__main__":
    regex = "0(0+1)*1"
    enfa = create_enfa_from_regex(regex)
    enfa.print()
    enfa.plot()

    input("Press return to continue")

    nfa = enfa.convert_to_nfa()
    nfa.print()
    nfa.plot()

    input("Press return to continue")

    dfa = nfa.convert_to_dfa()
    dfa.print()
    dfa.plot()
