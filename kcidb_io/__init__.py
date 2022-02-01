"""Kernel CI reporting I/O data"""

from kcidb_io import schema, misc # noqa Silence flake8 "imported but unused" warning
from kcidb_io.misc import LIGHT_ASSERTS


def new():
    """
    Create an empty I/O data set.

    Returns:
        An empty I/O data set adhering to the latest schema version.
    """
    return schema.LATEST.new()


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
    assert LIGHT_ASSERTS or schema.LATEST.is_valid(target)
    return schema.LATEST.merge(
        target,
        sources,
        copy_target=copy_target,
        copy_sources=copy_sources
    )
