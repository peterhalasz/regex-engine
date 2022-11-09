# regex-engine
An implementation of a regular expression engine.

NOTE: This is a work in progess an has a few bugs.

# Why
This projects purpose is to help me with learning about formal automata.

The implementation follows a strict by-the-book approach.
The regular expression gets converted to an ε-NFA, that can be converted to an NFA, which gets
converted to a DFA. The DFA can actually run the matching.

# How

# TODOs
 - [ ] Refactor NFA-DFA algorithm
 - [ ] Add more integration tests
 - [ ] Add comments / docs
 - [ ] Fix start and final state in the printer
