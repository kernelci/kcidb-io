"""Tests for miscellaneous definitions"""

import math
from kcidb_io.misc import json_cmp


def test_json_cmp():
    """Check json_cmp() works correctly"""
    assert json_cmp(None, None) == 0
    assert json_cmp(0, 0) == 0
    assert json_cmp(0, 1) == -1
    assert json_cmp(1, 0) == 1
    assert json_cmp("", "") == 0
    assert json_cmp("a", "a") == 0
    assert json_cmp("a", "b") == -1
    assert json_cmp("b", "a") == 1
    assert json_cmp(None, 10) == -1
    assert json_cmp([1, 10], [10, 1]) == -1
    assert json_cmp([1, 10], [10, 1], set_depth=1) == 0
    assert json_cmp([0, 1, None], []) == 1
    assert json_cmp([0, 1, False], [], set_depth=1) == 1
    assert json_cmp([0, 1, None], [], set_depth=1) == 1
    assert json_cmp(dict(), dict()) == 0
    assert json_cmp(dict(), dict(a=1)) == -1
    assert json_cmp(dict(a=1), dict(a=1)) == 0
    assert json_cmp(dict(a=1), dict(a=2)) == -1
    assert json_cmp(dict(a=2), dict(a=1)) == 1
    assert json_cmp(dict(a=1, b=2), dict(b=2, a=1)) == 0
    assert json_cmp(dict(a=[1], b=[2]), dict(b=[2], a=[1])) == 0
    assert json_cmp(dict(a=[1, 2], b=[2, 3]),
                    dict(b=[3, 2], a=[2, 1])) == -1
    assert json_cmp(dict(a=[1, 2], b=[2, 3]),
                    dict(b=[3, 2], a=[2, 1]),
                    set_depth=1) == -1
    assert json_cmp(dict(a=[1, 2], b=[2, 3]),
                    dict(b=[3, 2], a=[2, 1]),
                    set_depth=2) == 0
    assert json_cmp(dict(a=[1, 2], b=[2, 3]),
                    dict(b=[3, 2], a=[2, 1]),
                    set_depth=math.inf) == 0
