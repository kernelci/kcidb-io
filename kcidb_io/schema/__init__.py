"""Kernel CI reporting I/O schema"""

from kcidb_io.schema import v1, v2, v3, v4

# Version 1
V1 = v1.VERSION
# Version 2
V2 = v2.VERSION
# Version 3
V3 = v3.VERSION
# Version 4
V4 = v4.VERSION
# Latest version of the schema
LATEST = V4


def validate(data, schema=None):
    """
    Validate I/O data against one of the schema versions.

    Args:
        data:   The data to validate. Will not be changed.
        schema: Schema version to validate the data against.

    Returns:
        The validated (but unchanged) data.

    Raises:
        `jsonschema.exceptions.ValidationError` if the data did not adhere
        to any of the schema versions.
    """
    if isinstance(schema, int) and V1.major <= schema <= V4.major:
        return {
            V1.major: V1,
            V2.major: V2,
            V3.major: V3,
            V4.major: V4,
        }[schema].validate_exactly(data)
    return LATEST.validate(data)


def is_valid(data):
    """
    Check if I/O data is valid according to a schema version.

    Args:
        data:   The data to check.

    Returns:
        True if the data is valid, false otherwise.
    """
    return LATEST.is_valid(data)


def validate_latest(data):
    """
    Validate I/O data against the latest schema version only.

    Args:
        data:   The data to validate. Will not be changed.

    Returns:
        The validated (but unchanged) data.

    Raises:
        `jsonschema.exceptions.ValidationError` if the data did not adhere
        to the latest schema version.
    """
    return LATEST.validate_exactly(data)


def is_valid_latest(data):
    """
    Check if I/O data is valid according to the latest schema version.

    Args:
        data:   The data to check.

    Returns:
        True if the data is valid, false otherwise.
    """
    return LATEST.is_valid_exactly(data)


def count(data):
    """
    Calculate number of objects of any type in an I/O data set.

    Args:
        data:   The data set to count the objects in.

    Returns:
        The number of objects in the data set.
    """
    return LATEST.count(data)


def upgrade(data, copy=True):
    """
    Upgrade the data to the latest schema version from any of the previous
    versions. Validates the data. Has no effect if the data already adheres to
    the latest schema version.

    Args:
        data:   The data to upgrade and validate.
                Must adhere to a version of the schema.
        copy:   True, if the data should be copied before upgrading.
                False, if the data should be upgraded in-place.
                Optional, default is True.

    Returns:
        The upgraded and validated data.
    """
    return LATEST.upgrade(data, copy)
