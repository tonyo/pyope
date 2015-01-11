from pyope.util import str_to_bitstring


def test_bit_string_conversion():
    assert str_to_bitstring(b'') == []
    assert str_to_bitstring(b'A') == [0, 1, 0, 0, 0, 0, 0, 1]
    assert str_to_bitstring(b'AB') == [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0]