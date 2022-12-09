# regex-engine
An implementation of a regular expression engine.

NOTE: This is a work in progess.

# Why
This projects purpose is to help me with learning about formal automata.

The implementation follows a strict by-the-book approach.
The regular expression gets converted to an ε-NFA, that can be converted to an NFA, which gets
converted to a DFA. The DFA can actually run the matching.

# Usage
Clone this repo and run
```
python3 main.py
```

# Limitations
 * The input alphabet has to be {0, 1}, only strings consisting of 0 and 1 are supported.
 * Only the following operations are supported:
   * Concatenation ('01')
   * Union ('0+1')
   * Kleene star ('0\*')
 * Precedence orders with parenthesis is supported

# Under the hood
The implementation has 4 main parts, Regex, e-NFA, NFA and DFA.
The processing of the matching of a string to a regular expression happens as follows.

## Regex - regex.py
Using the Shunting-Yard algorithm, the regex is converted from infix to postifx notation. This helps
to eliminate having to parse parenthesis. For example the regex `(0+1)*0+11` would be transformed
to `01+*0.11.+`.

Out of the postfix regex the ε-NFA is created using the Thomsons's construction.

## ε-NFA - enfa.py
The epsilon-NFA is converted to an NFA by removing all ε transitions.

## NFA - nfa.py
The non-deterministic format automaton is converted to a DFA.

## DFA - dfa.py
The deterministic formal automaton can be easily executed and matched against the input string.
