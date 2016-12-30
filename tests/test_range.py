import pytest

from pyope.errors import InvalidRangeLimitsError
from pyope.ope import ValueRange


class TestValueRange(object):

    def test_range_simple(self):
        start = 2
        end = 1000
        r = ValueRange(start, end)
        assert r.size() == 999
        for i in range(start, end + 1):
            assert r.contains(i)
        assert not r.contains(start - 1)
        assert not r.contains(end + 1)
        assert r.range_bit_size() == 10

    def test_range_repr(self):
        a = ValueRange(1, 10)
        assert eval(repr(a)) == a

    @pytest.mark.parametrize("start,end", [
        ("123", 0),
        (0, "123"),
        ("123", "abc"),
    ])
    def test_invalid_range_ends(self, start, end):
        with pytest.raises(InvalidRangeLimitsError):
            ValueRange(start, end)
