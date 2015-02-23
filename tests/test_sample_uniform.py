import itertools
import pytest
from pyope.ope import ValueRange
from pyope.stat import sample_uniform


def test_uniform_short():
    value = 10
    unit_range = ValueRange(value, value)
    assert sample_uniform(unit_range, []) == value

    short_range = ValueRange(value, value + 1)
    assert sample_uniform(short_range, [0]) == value
    assert sample_uniform(short_range, [1]) == value + 1
    assert sample_uniform(short_range, [0, 0, 1, 0, 'llama']) == value, "More bits yield no effect"

    with pytest.raises(Exception):
        sample_uniform(short_range, [])


def test_uniform_medium():
    start_range = 20
    end_range = start_range + 15
    range1 = ValueRange(start_range, start_range + 15)
    assert sample_uniform(range1, [0, 0, 0, 0]) == start_range
    assert sample_uniform(range1, [0, 0, 0, 1]) == start_range + 1
    assert sample_uniform(range1, [1, 1, 1, 1]) == end_range

    # Test with a generator object
    assert sample_uniform(range1, itertools.repeat(0, 10)) == start_range

