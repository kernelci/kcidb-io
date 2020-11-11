"""Kernel CI reporting I/O data"""

from copy import deepcopy
from kcidb_io import schema, misc
from kcidb_io.misc import LIGHT_ASSERTS

# Silence flake8 "imported but unused" warning
__all__ = ["schema", "misc", "new", "merge"]


def new():
    """
    Create an empty I/O data set.

    Returns:
        An empty I/O data set adhering to the latest schema version.
    """
    data = dict(version=dict(major=schema.LATEST.major,
                             minor=schema.LATEST.minor))
    assert LIGHT_ASSERTS or schema.is_valid_latest(data)
    return data


def count(data):
    """
    Calculate number of objects of any type in an I/O data set.

    Args:
        data:   The data set to count the objects in.

    Returns:
        The number of objects in the data set.
    """
    assert LIGHT_ASSERTS or schema.is_valid(data)
    return schema.count(data)


def get_obj_num(data):
    """
    Calculate number of objects of any type in an I/O data set adhering to the
    latest schema. DEPRECATED, use count() instead.

    Args:
        data:   The data set to count the objects in.
                Must adhere to the latest schema.

    Returns:
        The number of objects in the data set.
    """
    assert LIGHT_ASSERTS or schema.is_valid(data)
    return count(data)


def merge(target, sources, copy_target=True, copy_sources=True):
    """
    Merge multiple I/O data into a destination.

    Args:
        target:         The data to merge into.
        sources:        An iterable containing data sets to merge from.
        copy_target:    True if "target" contents should be copied before
                        upgrading and modifying. False if not.
                        Default is True.
        copy_sources:   True if "source" contents should be copied before
                        upgrading and referencing. False if not.
                        Default is True.

    Returns:
        The merged data, adhering to the latest schema version.
    """
    assert LIGHT_ASSERTS or schema.is_valid(target)

    if copy_target:
        target = deepcopy(target)
    target = schema.upgrade(target, copy=False)

    for source in sources:
        assert LIGHT_ASSERTS or schema.is_valid(source)
        if copy_sources:
            source = deepcopy(source)
        source = schema.upgrade(source, copy=False)
        for obj_list_name in schema.LATEST.tree:
            if obj_list_name in source:
                target[obj_list_name] = \
                    target.get(obj_list_name, []) + source[obj_list_name]

    assert LIGHT_ASSERTS or schema.is_valid_latest(target)
    return target
