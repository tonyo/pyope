import itertools
import random
import pytest
from pyope.hgd import HGD
from pyope.ope import ValueRange
from pyope.stat import sample_uniform


def test_uniform():
    # Short ranges
    value = 10
    unit_range = ValueRange(value, value)
    assert sample_uniform(unit_range, []) == value

    short_range = ValueRange(value, value + 1)
    assert sample_uniform(short_range, [0]) == value
    assert sample_uniform(short_range, [1]) == value + 1
    assert sample_uniform(short_range, [0, 0, 1, 0, 'llama']) == value, "More bits yield no effect"

    with pytest.raises(Exception):
        sample_uniform(short_range, [])

    # Medium ranges
    start_range = 20
    end_range = start_range + 15
    range1 = ValueRange(start_range, start_range + 15)
    assert sample_uniform(range1, [0, 0, 0, 0]) == start_range
    assert sample_uniform(range1, [0, 0, 0, 1]) == start_range + 1
    assert sample_uniform(range1, [1, 1, 1, 1]) == end_range

    # Test with a generator object
    assert sample_uniform(range1, itertools.repeat(0, 10)) == start_range

    # Negative range
    start_range = -32
    end_range = -17
    range = ValueRange(start_range, end_range)
    assert sample_uniform(range, [0] * 5) == start_range
    assert sample_uniform(range, [1] * 5) == end_range

    # Mixed range
    start_range = -32
    end_range = 31
    range = ValueRange(start_range, end_range)
    assert sample_uniform(range, [0] * 6) == start_range
    assert sample_uniform(range, [1] * 6) == end_range


def test_hypergeometric():
    # Infinite random coins
    coins = (x for x in iter(lambda: random.randrange(2), 2))
    # Small values
    assert HGD.rhyper(5, 0, 5, coins) == 0
    assert HGD.rhyper(6, 6, 0, coins) == 6

    # Large values
    assert HGD.rhyper(2**32, 0, 2**32, coins) == 0
    assert HGD.rhyper(2**64, 2**64, 0, coins) == 2**64
    assert HGD.rhyper(2**32, 2, 2**32 - 2, coins) == 2
