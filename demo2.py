from regex import create_enfa_from_regex

if __name__ == "__main__":
    regex = "0"
    #regex = "0101"
    #regex = "0+1"
    #regex = "1*0*"
    #regex = "0(0+1)*1"

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
