from main import match

import re


if __name__ == "__main__":
    assert re.match("1", "1")
    assert re.match("01", "01")
    assert re.match("[01]", "1")
    assert re.match("[01]", "0")
    assert re.match("[01]*", "0101011010111000")
    assert re.match("1[01]*01", "1010101101010101")

    assert match("1", "1")
    assert match("01", "01")
    assert match("0+1", "1")
    assert match("0+1", "0")
    assert match("(0+1)*", "0101011010111000")
    assert match("1(0+1)*01", "1010101101010101")
