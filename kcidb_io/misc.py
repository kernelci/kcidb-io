"""Kernel CI reporting I/O data - misc definitions"""

import os
from itertools import repeat

# Check light assertions only, if True
LIGHT_ASSERTS = not os.environ.get("KCIDB_IO_HEAVY_ASSERTS", "")

# A dictionary of JSON value types, and their identity / sorting key.
JSON_TYPES = {
    type(None): 0,
    bool:       1,
    int:        2,
    float:      3,
    str:        4,
    tuple:      5,
    list:       5,
    dict:       6
}


def json_sort_key(value, set_depth=0):
    """
    Produce a sorting (comparable) key for a JSON value.

    Args:
        value:      The JSON value to produce the sorting key for.
        set_depth:  The container depth up to which arrays should be
                    considered unordered sets.

    Returns: The sorting key.
    """
    type_identity = JSON_TYPES[type(value)]
    set_depth -= 1
    if type_identity == JSON_TYPES[list]:
        value = tuple(sorted(
            map(json_sort_key, value, repeat(set_depth)),
            key=(None if set_depth >= 0 else lambda v: 0)
        ))
    elif type_identity == JSON_TYPES[dict]:
        value = tuple(sorted(map(
            lambda kv: (kv[0], json_sort_key(kv[1], set_depth)),
            value.items()
        )))
    return (type_identity, value)


def json_cmp(a, b, set_depth=0):
    """
    Compare two (sorted) JSON values.

    Args:
        a:          The first JSON value to compare.
        b:          The second JSON value to compare.
        set_depth:  The container depth up to which arrays should be
                    considered unordered sets and sorted.

    Returns: The comparison result, one of:
        -1 - a < b,
         0 - a == b,
         1 - a > b.
    """
    a_key = json_sort_key(a, set_depth)
    b_key = json_sort_key(b, set_depth)
    return 0 if a_key == b_key else (-1 if a_key < b_key else 1)
