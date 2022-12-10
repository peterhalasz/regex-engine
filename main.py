from regex import Regex


def match(regex, input_string):
    regex = Regex(regex)
    enfa = regex.create_enfa_from_regex()
    nfa = enfa.convert_to_nfa()
    dfa = nfa.convert_to_dfa()

    return dfa.is_string_accepted(input_string)


if __name__ == "__main__":
    regex = "0(0+1)*1"
    regex = Regex(regex)
    enfa = regex.create_enfa_from_regex()

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
