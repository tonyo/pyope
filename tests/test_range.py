from pyope.ope import ValueRange


def test_range_simple():
    start = 2
    end = 1000
    r = ValueRange(start, end)
    assert r.size() == 999
    for i in range(start, end + 1):
        assert r.contains(i)
    assert not r.contains(start - 1)
    assert not r.contains(end + 1)

    assert r.range_bit_size() == 10
