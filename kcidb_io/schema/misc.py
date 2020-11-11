"""Kernel CI reporting I/O schema - misc definitions"""

from copy import deepcopy
import jsonschema
from kcidb_io.misc import LIGHT_ASSERTS


class Version:
    """A version of the schema"""
    # pylint: disable=too-many-arguments
    def __init__(self, major, minor, json, tree, get_version,
                 previous=None, inherit=None):
        """
        Initialize the version.

        Args:
            major:          The major version number. A non-negative integer.
                            Increases represent backward-incompatible changes.
                            E.g. deleting or renaming a property, changing a
                            property type, restricting values, making a
                            property required, or adding a new required
                            property.
            minor:          The minor version number. A non-negative integer.
                            Increases represent backward-compatible changes.
                            E.g. relaxing value restrictions, making a
                            property optional, or adding a new optional
                            property.
            json:           The JSON schema for this version.
            tree:           A tree of parent-child relationships for objects
                            in data's top-level lists, expressed as a
                            dictionary of object list names to a list of the
                            same, with the empty string mapping to a list of
                            topmost object list names.
            get_version:    A function retrieving both the major and the minor
                            version numbers from a data, or returning (None,
                            None) if it is not found in the data.
            previous:       The previous schema version, or None if none.
                            Must have lower major number, if not None.
            inherit:        The data inheritance function. Must accept data
                            adhering to the "previous" version of the schema
                            as the only argument, and return the data adhering
                            to this version. Can modify the argument. Can be
                            None, meaning no transformation needed. Must be
                            None if "previous" is None.
        """
        assert isinstance(major, int) and major >= 0
        assert isinstance(minor, int) and minor >= 0
        assert json is not None
        assert isinstance(tree, dict)
        assert all(isinstance(k, str) and
                   isinstance(v, list) and
                   all(isinstance(e, str) for e in v)
                   for k, v in tree.items())
        assert callable(get_version)
        assert previous is None or \
            isinstance(previous, Version) and (major > previous.major)
        assert inherit is None or previous is not None and callable(inherit)

        self.major = major
        self.minor = minor
        self.json = json
        self.tree = tree
        self.get_version = get_version
        self.previous = previous
        self.inherit = inherit

    def is_compatible_exactly(self, data):
        """
        Check if a data's version is compatible with this schema exactly,
        without validating.

        Args:
            data:   The data to check compatibility of.

        Returns:
            True if the data is compatible with the schema, false otherwise.
        """
        major, minor = self.get_version(data)
        return major == self.major and minor <= self.minor

    def get_exactly_compatible(self, data):
        """
        Get the schema version exactly-compatible with the schema version of a
        data, without validating.

        Args:
            data:   The data to get the exactly-compatible schema for.

        Returns:
            The schema exactly-compatible with the data version, or None, if
            not found.
        """
        if self.is_compatible_exactly(data):
            return self
        if self.previous:
            return self.previous.get_exactly_compatible(data)
        return None

    def is_compatible(self, data):
        """
        Check if a data's version is compatible with this or previous schema
        versions, without validating.

        Args:
            data:   The data to check compatibility of.

        Returns:
            True if the data is compatible with this or a previous schema,
            false otherwise.
        """
        return self.get_exactly_compatible(data) is not None

    def count(self, data):
        """
        Calculate number of objects of any type in an I/O data set adhering to
        this or a previous schema version.

        Args:
            data:   The data set to count the objects in.

        Returns:
            The number of objects in the data set.
        """
        assert LIGHT_ASSERTS or self.is_valid(data)
        return sum(len(data[k])
                   for k in self.get_exactly_compatible(data).tree
                   if k and k in data)

    def validate_exactly(self, data):
        """
        Validate the data against this schema version only.

        Args:
            data:   The data to validate. Will not be changed.

        Returns:
            The validated (but unchanged) data.

        Raises:
            `jsonschema.exceptions.ValidationError` if the data did not adhere
            to this version of the schema.
        """
        jsonschema.validate(instance=data, schema=self.json,
                            format_checker=jsonschema.draft7_format_checker)
        return data

    def is_valid_exactly(self, data):
        """
        Check if data is valid according to this schema version only.

        Args:
            data:   The data to check against the schema.

        Returns:
            True if the data is valid, false otherwise.
        """
        try:
            self.validate_exactly(data)
        except jsonschema.exceptions.ValidationError:
            return False
        return True

    def validate(self, data):
        """
        Validate the data against this or previous schema versions.

        Args:
            data:   The data to validate. Will not be changed.

        Returns:
            The validated (but unchanged) data.

        Raises:
            `jsonschema.exceptions.ValidationError` if the data did not adhere
            to this or a previous version of the schema.
        """
        exactly_compatible = self.get_exactly_compatible(data)
        if exactly_compatible:
            return exactly_compatible.validate_exactly(data)
        # Produce validation failure if not compatible
        return self.validate_exactly(data)

    def is_valid(self, data):
        """
        Check if data is valid according to this or previous schema version.

        Args:
            data:   The data to check against the schema.

        Returns:
            True if the data is valid, false otherwise.
        """
        try:
            self.validate(data)
        except jsonschema.exceptions.ValidationError:
            return False
        return True

    def upgrade(self, data, copy=True):
        """
        Upgrade the data to this version from any of the previous schema
        versions. Has no effect if the data already adheres to this schema
        version.

        Args:
            data:   The data to upgrade. Must adhere to this version,
                    or any of the previous versions.
            copy:   True, if the data should be copied before handling.
                    False, if the data should be upgraded in-place, or
                    returned as is, if it already adheres to this version.
                    Optional, default is True.

        Returns:
            The upgraded (and/or copied) data, valid for this schema version.

        Raises:
            jsonschema.exceptions.ValidationError: Data didn't adhere to this,
                                                   or any of the previous
                                                   schema versions.
        """
        assert LIGHT_ASSERTS or self.is_valid(data)
        if copy:
            data = deepcopy(data)
        if not self.is_compatible_exactly(data):
            if self.previous and self.previous.is_compatible(data):
                data = self.previous.upgrade(data, copy=False)
                if self.inherit:
                    data = self.inherit(data)
        return self.validate_exactly(data)
