from pyope.util import str_to_bitstring


def test_bit_string_conversion():
    assert str_to_bitstring('') == []
    assert str_to_bitstring('A') == [0, 1, 0, 0, 0, 0, 0, 1]
    assert str_to_bitstring('AB') == [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0]