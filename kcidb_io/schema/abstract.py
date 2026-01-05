"""Kernel CI reporting I/O schema - abstract definitions"""

from copy import deepcopy
from abc import ABC, ABCMeta, abstractmethod
from functools import lru_cache
import random
import jsonschema
from kcidb_io.misc import LIGHT_ASSERTS, json_cmp


@lru_cache(maxsize=None)
def _build_validator_for(schema_cls):
    """Return a compiled Draft7 validator for a given Version subclass.

    Cached per-class via lru_cache; safe across supported Python versions.
    """
    return jsonschema.Draft7Validator(
        schema=schema_cls.json,
        format_checker=jsonschema.Draft7Validator.FORMAT_CHECKER,
    )


class MetaVersion(ABCMeta):
    """Abstract schema version metaclass"""
    def __init__(cls, name, bases, _dict, **kwargs):
        """
        Initialize a version class.

        Args:
            cls:    The class to be initialized.
            name:   The name of the class being initialized.
            bases:  A list of base classes for the initialized class.
            _dict:  The class dictionary.
            kwargs: Other (opaque) metaclass arguments.
        """
        assert len(bases) == 1
        # Require each version to have its own major/minor number to minimize
        # chance of accidental inheritance
        assert "major" in _dict, "Version has no own major number"
        assert "minor" in _dict, "Version has no own minor number"
        # Require each version to have its own JSON schema and the
        # corresponding graph to minimize chance of accidental inheritance
        assert "json" in _dict, "Version has no own schema"
        assert "graph" in _dict, "Version has no own graph"
        super().__init__(name, bases, _dict, **kwargs)
        # We need it for later, pylint: disable=fixme
        base = bases[0]
        # If this is not the abstract version
        if base is not ABC:
            assert isinstance(cls.major, int) and cls.major >= 0
            assert isinstance(cls.minor, int) and cls.minor >= 0
            # If this is the first non-abstract version
            if base is Version:
                assert "_inherit" not in _dict, \
                    "First version has own _inherit() method"
            # Else, this is not the first non-abstract version
            else:
                assert cls.major >= base.major, \
                    "Major version number is lower than the previous one"
                assert cls.major > base.major or "_inherit" not in _dict, \
                    "Minor version has own _inherit() method"
                assert cls.major == base.major or "_inherit" in _dict, \
                    "Major version has no own _inherit() method"
                assert cls.major > base.major or cls.minor > base.minor, \
                    "Minor version number is lower than the previous one"
            assert isinstance(cls.json, dict)
            assert cls.json != base.json
            assert isinstance(cls.graph, dict)
            assert all(isinstance(k, str) and
                       isinstance(v, list) and
                       all(isinstance(e, str) for e in v)
                       for k, v in cls.graph.items())
            assert "" in cls.graph
            assert isinstance(cls.id_fields, dict)
            assert set(cls.graph) - {""} == set(cls.id_fields)
            assert all(isinstance(fields, dict) and
                       len(fields) > 0 and
                       all(isinstance(n, str) and isinstance(t, type)
                           for n, t in fields.items())
                       for fields in cls.id_fields.values())

    def __str__(cls):
        return f"v{cls.major}.{cls.minor}"

    def __le__(cls, other):
        if isinstance(other, type) and \
           (issubclass(cls, other) or issubclass(other, cls)):
            return issubclass(other, cls)
        return NotImplemented

    def __ge__(cls, other):
        if isinstance(other, type) and \
           (issubclass(cls, other) or issubclass(other, cls)):
            return issubclass(cls, other)
        return NotImplemented

    def __lt__(cls, other):
        if isinstance(other, type) and \
           (issubclass(cls, other) or issubclass(other, cls)):
            return issubclass(other, cls) and cls is not other
        return NotImplemented

    def __gt__(cls, other):
        if isinstance(other, type) and \
           (issubclass(cls, other) or issubclass(other, cls)):
            return issubclass(cls, other) and cls is not other
        return NotImplemented

    @property
    def previous(cls):
        """The previous version"""
        base = cls.__bases__[0]
        assert base is not ABC
        return None if base.__bases__[0] is ABC else base

    @property
    def lineage(cls):
        """
        A generator returning every version in (reverse order of) history,
        starting with this one and ending with the first version (the direct
        child of the abstract version).
        """
        while cls.__bases__[0] is not ABC:
            yield cls
            # Piss off, pylint: disable=self-cls-assignment
            cls = cls.__bases__[0]

    @property
    def history(cls):
        """
        A tuple containing every version in history, starting with the
        first version (the direct child of the abstract version) and ending
        with this one.
        """
        return tuple(reversed(tuple(cls.lineage)))


class InheritanceImpossible(Exception):
    """Inheritance into new schema is impossible as data is ambiguous"""


class Version(ABC, metaclass=MetaVersion):
    """Abstract schema version"""

    # The major version number. A non-negative integer. Increases represent
    # backward-incompatible changes. E.g. deleting or renaming a property,
    # changing a property type, restricting values, making a property
    # required, or adding a new required property.
    major = None
    # The minor version number. A non-negative integer. Increases represent
    # backward-compatible changes. E.g. relaxing value restrictions, making a
    # property optional, or adding a new optional property.
    minor = None
    # The JSON schema for this version.
    json = None
    # A directed graph of parent-child relationships for objects in data's
    # top-level lists, expressed as a dictionary of object list names to a
    # list of the same, with the empty string mapping to a list of topmost
    # object list names.
    graph = None
    # A map of object names and dictionaries of their ID fields and types
    id_fields = None

    # Validator compiled per-class via module-level lru_cache

    @classmethod
    @abstractmethod
    def _get_version(cls, data):
        """
        Retrieve the schema version from a data.

        Args:
            data:   The data to retrieve the schema version from.

        Returns:
            The major and the minor schema version numbers from the data,
            or (None, None), if not found.
        """

    @classmethod
    @abstractmethod
    def _set_version(cls, data):
        """
        Set the schema version of a data to version numbers of this class.

        Args:
            data:   The data to set the schema version of.
        """

    @classmethod
    def is_compatible_directly(cls, data):
        """
        Check (without validating) if a data is directly compatible (without
        upgrading) with this schema version.

        Args:
            data:   The data to check compatibility of.

        Returns:
            True if the data is directly compatible with the schema,
            false otherwise.
        """
        version = cls._get_version(data)
        return version[0] == cls.major and version[1] <= cls.minor

    @classmethod
    def get_directly_compatible(cls, data):
        """
        Get a schema version directly-compatible (without upgrading) with
        the schema version of a data, without validating.

        Args:
            data:   The data to get an exactly-compatible schema for.

        Returns:
            A schema version exactly-compatible with the data version, or
            None, if not found.
        """
        for version in cls.lineage:
            if version.is_compatible_directly(data):
                return version
        return None

    @classmethod
    def is_compatible_exactly(cls, data):
        """
        Check (without validating) if a data is compatible with this schema
        version exactly.

        Args:
            data:   The data to check compatibility of.

        Returns:
            True if the data is exactly compatible with the schema,
            false otherwise.
        """
        return cls._get_version(data) == (cls.major, cls.minor)

    @classmethod
    def get_exactly_compatible(cls, data):
        """
        Get the schema version exactly-compatible with the schema version of a
        data, without validating.

        Args:
            data:   The data to get the exactly-compatible schema for.

        Returns:
            The schema exactly-compatible with the data version, or None, if
            not found.
        """
        for version in cls.lineage:
            if version.is_compatible_exactly(data):
                return version
        return None

    @classmethod
    def is_compatible(cls, data):
        """
        Check (without validating) if a data is compatible with this or
        a previous schema version.

        Args:
            data:   The data to check compatibility of.

        Returns:
            True if the data is compatible with this or a previous schema
            version, false otherwise.
        """
        return cls.get_exactly_compatible(data) is not None

    @classmethod
    def count(cls, data):
        """
        Calculate number of objects of any type in an I/O data set adhering to
        this or a previous schema version.

        Args:
            data:   The data set to count the objects in.

        Returns:
            The number of objects in the data set.
        """
        assert cls.is_compatible(data)
        assert LIGHT_ASSERTS or cls.is_valid(data)
        return sum(len(data[k])
                   for k in cls.get_exactly_compatible(data).graph
                   if k and k in data)

    @classmethod
    def get_ids(cls, data):
        """
        Get the IDs of objects in a data set.

        Args:
            data:   The data set to extract object IDs from.

        Returns:
            A dictionary of object list names (types), and lists of IDs of
            objects in the data set. Each ID is either a tuple of values or a
            single value (equivalent to a single-value tuple). The values
            match the types, the order, and the number of the object's ID
            fields as described by the schema's "id_fields" attribute.
        """
        assert cls.is_compatible(data)
        assert LIGHT_ASSERTS or cls.is_valid(data)
        return {
            obj_list_name: [
                obj[list(id_fields)[0]]
                if len(id_fields) == 1 else
                tuple(obj[n] for n in id_fields)
                for obj in data[obj_list_name]
            ]
            for obj_list_name, id_fields in
            cls.get_exactly_compatible(data).id_fields.items()
            if data.get(obj_list_name, [])
        }

    @classmethod
    def validate_exactly(cls, data):
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
        # Validate using the compiled validator cached per-class
        _build_validator_for(cls).validate(data)
        return data

    @classmethod
    def is_valid_exactly(cls, data):
        """
        Check if data is valid according to this schema version only.

        Args:
            data:   The data to check against the schema.

        Returns:
            True if the data is valid, false otherwise.
        """
        try:
            cls.validate_exactly(data)
        except jsonschema.exceptions.ValidationError:
            return False
        return True

    @classmethod
    def validate(cls, data):
        """
        Validate the data against this or a previous schema version.

        Args:
            data:   The data to validate. Will not be changed.

        Returns:
            The validated (but unchanged) data.

        Raises:
            `jsonschema.exceptions.ValidationError` if the data did not adhere
            to this or a previous version of the schema.
        """
        exactly_compatible = cls.get_exactly_compatible(data)
        # Produce this version's validation failure if not compatible
        return (exactly_compatible or cls).validate_exactly(data)

    @classmethod
    def is_valid(cls, data):
        """
        Check if data is valid according to this or previous schema version.

        Args:
            data:   The data to check against the schema.

        Returns:
            True if the data is valid, false otherwise.
        """
        try:
            cls.validate(data)
        except jsonschema.exceptions.ValidationError:
            return False
        return True

    @classmethod
    def new(cls):
        """
        Create an empty dataset for this schema version.

        Returns:
            An empty dataset adhering to this schema version.
        """
        data = dict(version=dict(major=cls.major, minor=cls.minor))
        assert cls.is_compatible_exactly(data)
        assert LIGHT_ASSERTS or cls.is_valid_exactly(data)
        return data

    @classmethod
    def has_metadata(cls, data):
        """
        Check if a dataset has metadata.

        Args:
            data:   The dataset to check.

        Returns:
            True if the dataset has metadata fields.
        """
        assert cls.is_compatible_exactly(data)
        assert LIGHT_ASSERTS or cls.is_valid_exactly(data)

        def node_has_metadata(node):
            """Check if a dataset node has metadata"""
            if isinstance(node, dict):
                return any(
                    k.startswith("_") or k != "misc" and node_has_metadata(v)
                    for k, v in node.items()
                )
            if isinstance(node, list):
                return any(node_has_metadata(v) for v in node)
            return False

        return node_has_metadata(data)

    @classmethod
    def strip_metadata(cls, data, copy=True):
        """
        Remove metadata from a dataset, if any.

        Args:
            data:   The dataset to remove metadata from.
            copy:   True, if the data should be copied before handling.
                    False, if the metadata should be removed in-place.

        Returns:
            The (copy of the) dataset with metadata removed.
        """
        assert cls.is_compatible_exactly(data)
        assert LIGHT_ASSERTS or cls.is_valid_exactly(data)

        # Copy the data, if requested
        if copy:
            data = deepcopy(data)

        def node_strip_metadata(node):
            """Strip metadata from a node in a dataset"""
            if isinstance(node, dict):
                for k, v in list(node.items()):
                    if k.startswith("_"):
                        del node[k]
                    elif k != "misc":
                        node_strip_metadata(v)
            elif isinstance(node, list):
                for v in node:
                    node_strip_metadata(v)

        node_strip_metadata(data)
        return data

    @staticmethod
    @abstractmethod
    def _inherit(data):
        """
        Inherit data, i.e. convert data adhering to the previous major version
        of the schema to satisfy this version of the schema. Doesn't update
        the data's version numbers.

        Args:
            data:   The data to inherit. Will be modified in place.

        Returns:
            The inherited data.

        Raises:
            InheritanceImpossible - the previous schema's data is ambiguous
                                    and cannot be inherited. Read the message,
                                    disambiguate/cleanup, and retry.
        """

    @classmethod
    def upgrade(cls, data, copy=True):
        """
        Upgrade the data to this version from any of the previous schema
        versions. Has no effect if the data already adheres to this schema
        version.

        Args:
            data:   The data to upgrade. Must adhere to this version,
                    or any of the previous versions. Will not be validated.
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
        # Copy the data, if requested
        if copy:
            data = deepcopy(data)

        # Find the first compatible version (if any), and remember all newer
        # versions in history order
        newer_versions = []
        for version in cls.lineage:
            if version.is_compatible_exactly(data):
                assert LIGHT_ASSERTS or version.is_valid_exactly(data)
                break
            newer_versions.insert(0, version)
        else:
            # No compatible version found, fail validation with this version
            cls.validate_exactly(data)
            # We shouldn't get here
            assert False, "Data validated unexpectedly"
            return None

        # Inherit data through all newer versions up to this one
        for version in newer_versions:
            # No it's not, pylint: disable=protected-access
            if "_inherit" in version.__dict__:
                data = version._inherit(data)
            version._set_version(data)
            assert LIGHT_ASSERTS or version.is_valid_exactly(data)

        return data

    @classmethod
    def align(cls, first, second, copy_first=True, copy_second=True):
        """
        Align schema versions of two datasets: upgrade the dataset with older
        schema version to the version of the other, if different.

        Args:
            first:          The first dataset to align.
            second:         The second dataset to align.
            copy_first:     If true, the first dataset should be copied before
                            upgrading.
            copy_second:    If true, the second dataset should be copied
                            before upgrading.

        Returns:
            The schema version both datasets are adhering to, the first
            dataset, and the second dataset, where one of them is possibly
            upgraded.
        """
        assert cls.is_compatible(first)
        assert cls.is_compatible(second)
        v_first = cls.get_exactly_compatible(first)
        v_second = cls.get_exactly_compatible(second)
        if copy_first:
            first = deepcopy(first)
        if copy_second:
            second = deepcopy(second)
        v = max(v_first, v_second)
        return v, v.upgrade(first, copy=False), v.upgrade(second, copy=False)

    @classmethod
    def merge(cls, target, sources, copy_target=True, copy_sources=True):
        """
        Merge multiple datasets into a destination dataset.

        Args:
            target:         The dataset to merge into.
            sources:        An iterable containing datasets to merge from.
            copy_target:    True if "target" contents should be copied before
                            upgrading and modifying. False if not.
                            Default is True.
            copy_sources:   True if "source" contents should be copied before
                            upgrading and referencing. False if not.
                            Default is True.

        Returns:
            The merged dataset, adhering to this schema version.
        """
        assert cls.is_compatible(target)
        assert LIGHT_ASSERTS or cls.is_valid(target)
        if copy_target:
            target = deepcopy(target)
        version = cls.get_exactly_compatible(target)
        for source in sources:
            assert cls.is_compatible(source)
            assert LIGHT_ASSERTS or cls.is_valid(source)
            # Upgrade both target and source to the same version
            version, target, source = cls.align(target, source,
                                                copy_first=False,
                                                copy_second=copy_sources)
            # Merge the source into the target
            for obj_list_name in version.graph:
                if obj_list_name in source:
                    target[obj_list_name] = \
                        target.get(obj_list_name, []) + source[obj_list_name]
        assert version.is_compatible_exactly(target)
        assert LIGHT_ASSERTS or version.is_valid_exactly(target)
        return target

    @classmethod
    def dedup(cls, data, copy=True, pick_second=None):
        """
        Deduplicate objects in a dataset of this or earlier schema version.

        Objects with the same type and ID are merged pairwise and removed
        until only one remains, which takes the list position of the first
        one. Each top-level attribute's value is picked with the help of
        pick_second() function parameter from either of the two objects, if
        it's present in both. Otherwise it's taken from whichever object has
        it.

        Args:
            data:           The dataset to deduplicate.
            copy:           True if the data should be copied before handling.
                            False if it should be modified in place.
            pick_second:    A function called for each deduplicated attribute
                            pair, without arguments. If it returns false, the
                            first attribute's value (in object order) is
                            picked. The second attribute's value is picked
                            otherwise. If None, random.getrandbits(1) is used,
                            resulting in the same deduplication logic
                            databases are expected to employ.

        Returns:
            The deduplicated dataset.
        """
        version = cls.get_exactly_compatible(data)
        assert version is not None
        assert LIGHT_ASSERTS or version.is_valid_exactly(data)
        if pick_second is None:
            def pick_second():
                return random.getrandbits(1)
        assert callable(pick_second)
        if copy:
            data = deepcopy(data)

        def merge_objs(first, second):
            """Merge the second object into the first, unless the same."""
            if first is not second:
                for attr in first:
                    if attr in second and pick_second():
                        first[attr] = second[attr]
                for attr in second:
                    if attr not in first:
                        first[attr] = second[attr]
            return first

        for obj_list_name in version.graph:
            if obj_list_name in data:
                obj_dict = {}
                for obj in data[obj_list_name]:
                    obj_id = tuple(map(
                        obj.get, version.id_fields[obj_list_name]
                    ))
                    merge_objs(obj_dict.setdefault(obj_id, obj), obj)
                data[obj_list_name] = list(obj_dict.values())
        return data

    @classmethod
    def cmp_directly_compatible(cls, first, second):
        """
        Compare two datasets directly compatible with this schema version.

        Args:
            first:          The first dataset to compare.
            second:         The second dataset to compare.

        Returns: The comparison result, one of:
            -1 - a < b,
             0 - a == b,
             1 - a > b.
        """
        assert cls.is_compatible_directly(first)
        assert cls.is_compatible_directly(second)
        # NOTE This only works while schema versions keep more-or-less the
        #      same structure. Otherwise this would need to be customized.
        return json_cmp(first, second,
                        # Treat object lists as unordered sets
                        set_depth=2)

    @classmethod
    def cmp(cls, first, second, copy_first=True, copy_second=True):
        """
        Compare two datasets of this or an earlier schema version.

        Args:
            first:          The first dataset to compare.
            second:         The second dataset to compare.
            copy_first:     If true, the first dataset should be copied before
                            comparison and possible upgrading. Otherwise the
                            upgrade will be done in place, if required.
            copy_second:    If true, the second dataset should be copied
                            before comparison and possible upgrading.
                            Otherwise the upgrade will be done in place, if
                            required.

        Returns: The comparison result, one of:
            -1 - a < b,
             0 - a == b,
             1 - a > b.
        """
        version, first, second = cls.align(first, second,
                                           copy_first=copy_first,
                                           copy_second=copy_second)
        return version.cmp_directly_compatible(first, second)
