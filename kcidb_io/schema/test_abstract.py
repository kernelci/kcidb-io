"""Abstract module tests"""

import unittest
from kcidb_io.schema.abstract import Version


class VersionTestCase(unittest.TestCase):
    """Version class test case"""

    def test_correct_versions(self):
        """Check correct versions can be created"""
        # pylint: disable=unused-variable,missing-class-docstring
        class V1(Version):
            major = 1
            minor = 0
            json = dict(title="v1")
            graph = {"": []}
            id_fields = {}

        class V2(V1):
            major = 2
            minor = 0
            json = dict(title="v2")
            graph = {"": []}
            id_fields = {}

            @staticmethod
            def _inherit(data):
                pass

        class V2D1(V2):
            major = 2
            minor = 1
            json = dict(title="v2.1")
            graph = {"": []}
            id_fields = {}

        class V3(V2D1):
            major = 3
            minor = 0
            json = dict(title="v3")
            graph = {"": []}
            id_fields = {}

            @staticmethod
            def _inherit(data):
                pass

        # Piss off, old pylint
        self.assertTrue(not False)

    def test_incorrect_versions(self):
        """Check incorrect versions are detected"""
        # pylint: disable=unused-variable,missing-class-docstring
        with self.assertRaises(AssertionError):
            class VNone(Version):
                pass

        with self.assertRaises(AssertionError):
            class V1Incomplete(Version):
                major = 1

        with self.assertRaises(AssertionError):
            class VMinus1(Version):
                major = -1
                minor = 0
                json = dict(title="v-1")
                graph = {"": []}

        with self.assertRaises(AssertionError):
            class V1WithInherit(Version):
                major = 1
                minor = 0
                json = dict(title="v1")
                graph = {"": []}

                @staticmethod
                def _inherit(data):
                    pass

        with self.assertRaises(AssertionError):
            class V1WithoutInherit(Version):
                major = 1
                minor = 0
                json = dict(title="v1")
                graph = {"": []}

            class V2WithoutInherit(V1WithoutInherit):
                major = 2
                minor = 0
                json = dict(title="v2")
                graph = {"": []}

        # Minor version with _inherit() method
        with self.assertRaises(AssertionError):
            class V1D0(Version):
                major = 1
                minor = 0
                json = dict(title="v1")
                graph = {"": []}

            class V1D1(V1D0):
                major = 1
                minor = 1
                json = dict(title="v2")
                graph = {"": []}

                @staticmethod
                def _inherit(data):
                    pass

        with self.assertRaises(AssertionError):
            class V1InvalidGraph(Version):
                major = 1
                minor = 0
                json = dict(title="v1")
                graph = {}

        with self.assertRaises(AssertionError):
            class V1(Version):
                major = 1
                minor = 0
                json = dict(title="v1")
                graph = {"": []}

            class V2OldMajor(V1):
                major = 1
                minor = 0
                json = dict(title="v1")
                graph = {"": []}

                @staticmethod
                def _inherit(data):
                    pass

    def test_comparison(self):
        """Test schema version comparison is correct"""
        # pylint: disable=unused-variable,missing-class-docstring
        # pylint: disable=too-many-statements
        class V1(Version):
            major = 1
            minor = 0
            json = dict(title="v1")
            graph = {"": []}
            id_fields = {}

        class V2A(V1):
            major = 2
            minor = 0
            json = dict(title="v2a")
            graph = {"": []}
            id_fields = {}

            @staticmethod
            def _inherit(data):
                pass

        class V2B(V1):
            major = 2
            minor = 0
            json = dict(title="v2b")
            graph = {"": []}
            id_fields = {}

            @staticmethod
            def _inherit(data):
                pass

        # Calm down, it's a test, pylint: disable=comparison-with-itself
        self.assertTrue(V1 == V1)
        self.assertTrue(V2A == V2A)
        self.assertTrue(V2B == V2B)
        self.assertFalse(V1 != V1)
        self.assertFalse(V2A != V2A)
        self.assertFalse(V2B != V2B)

        self.assertTrue(V1 != V2A)
        self.assertTrue(V1 != V2B)
        self.assertTrue(V2A != V2B)
        self.assertFalse(V1 == V2A)
        self.assertFalse(V1 == V2B)
        self.assertFalse(V2A == V2B)

        self.assertTrue(V1 <= V1)
        self.assertTrue(V1 >= V1)
        self.assertFalse(V1 < V1)
        self.assertFalse(V1 > V1)
        self.assertTrue(V2A <= V2A)
        self.assertTrue(V2A >= V2A)
        self.assertFalse(V2A < V2A)
        self.assertFalse(V2A > V2A)
        self.assertTrue(V2B <= V2B)
        self.assertTrue(V2B >= V2B)
        self.assertFalse(V2B < V2B)
        self.assertFalse(V2B > V2B)

        self.assertTrue(V1 < V2A)
        self.assertTrue(V1 < V2B)
        self.assertFalse(V1 > V2A)
        self.assertFalse(V1 > V2B)

        with self.assertRaises(TypeError):
            self.assertTrue(V2A < V2B)
        with self.assertRaises(TypeError):
            self.assertTrue(V2A > V2B)
        with self.assertRaises(TypeError):
            self.assertTrue(V2A <= V2B)
        with self.assertRaises(TypeError):
            self.assertTrue(V2A >= V2B)

    def test_dedup(self):
        """Check dedup() method works correctly"""
        class V1(Version):
            """First version"""
            major = 1
            minor = 0
            json = dict(title="v1")
            graph = {"": ["revisions"], "revisions": ["builds"],
                     "builds": []}
            id_fields = dict(
                revisions=dict(id=str),
                builds=dict(id=str),
            )

            @classmethod
            def _get_version(cls, data):
                assert isinstance(data, dict)
                version = data.get("version", {})
                return version.get("major"), version.get("minor")

            @classmethod
            def _set_version(cls, data):
                assert isinstance(data, dict)
                data["version"] = dict(major=cls.major, minor=cls.minor)

        class V2(V1):
            """Second version"""
            major = 2
            minor = 0
            json = dict(title="v2")
            graph = {"": ["checkouts", "issues"], "checkouts": ["builds"],
                     "builds": [], "issues": []}
            id_fields = dict(
                checkouts=dict(id=str),
                builds=dict(id=str),
                issues=dict(id=str, version=int),
            )

            @staticmethod
            def _inherit(data):
                revisions = data.pop("revisions", None)
                if revisions is not None:
                    data["checkouts"] = revisions
                return data

        assert V1.dedup(V1.new()) == V1.new()
        assert V2.dedup(V1.new()) == V1.new()
        assert V2.upgrade(V2.dedup(V1.new())) == V2.new()
        assert V2.dedup(V2.new()) == V2.new()

        data = V1.new() | dict(revisions=[], builds=[])
        assert V1.dedup(data) == data
        data = V1.new() | dict(
            revisions=[dict(id="a")], builds=[dict(id="b")]
        )
        assert V1.dedup(data) == data
        data = V1.new() | dict(
            revisions=[dict(id="a", comment="A")],
            builds=[dict(id="b", comment="B")]
        )
        assert V1.dedup(data) == data

        data = V2.new() | dict(checkouts=[], builds=[], issues=[])
        assert V2.dedup(data) == data
        data = V2.new() | dict(
            checkouts=[dict(id="a")], builds=[dict(id="b")],
            issues=[dict(id="c", version=0xd)]
        )
        data = V2.new() | dict(
            checkouts=[dict(id="a", comment="A")],
            builds=[dict(id="b", comment="B")],
            issues=[dict(id="c", version=0xd, comment="C")]
        )
        assert V2.dedup(data) == data

        # Check identical duplicate objects are removed
        assert V1.dedup(V1.new() | dict(
            revisions=[dict(id="a", comment="A"),
                       dict(id="alpha", comment="Alpha"),
                       dict(id="a", comment="A")],
            builds=[dict(id="b", comment="B"),
                    dict(id="beta", comment="Beta"),
                    dict(id="b", comment="B")],
        )) == V1.new() | dict(
            revisions=[dict(id="a", comment="A"),
                       dict(id="alpha", comment="Alpha")],
            builds=[dict(id="b", comment="B"),
                    dict(id="beta", comment="Beta")],
        )

        assert V2.dedup(V2.new() | dict(
            checkouts=[dict(id="a", comment="A"),
                       dict(id="alpha", comment="Alpha"),
                       dict(id="a", comment="A")],
            builds=[dict(id="b", comment="B"),
                    dict(id="beta", comment="Beta"),
                    dict(id="b", comment="B")],
            issues=[dict(id="f", version=0xf, comment="F"),
                    dict(id="feta", version=0xf, comment="Feta"),
                    dict(id="feta", version=0x3, comment="Feta"),
                    dict(id="f", version=0xf, comment="F")],
        )) == V2.new() | dict(
            checkouts=[dict(id="a", comment="A"),
                       dict(id="alpha", comment="Alpha")],
            builds=[dict(id="b", comment="B"),
                    dict(id="beta", comment="Beta")],
            issues=[dict(id="f", version=0xf, comment="F"),
                    dict(id="feta", version=0xf, comment="Feta"),
                    dict(id="feta", version=0x3, comment="Feta")],
        )

        # Check field values are picked between same-ID objects
        deduped = V2.dedup(V2.new() | dict(
            checkouts=[dict(id="a", comment="A"),
                       dict(id="a", comment="Alpha")],
            builds=[dict(id="b", comment="B"),
                    dict(id="b", comment="Beta")],
            issues=[dict(id="f", version=0xf, comment="F"),
                    dict(id="f", version=0xf, comment="Feta")],
        ))
        assert set("version checkouts builds issues".split()) == set(deduped)
        assert all(
            len(ol := deduped[n]) == 1 and
            isinstance(o := ol[0], dict) and
            o["id"] == id and
            o["comment"] in (c1, c2)
            for n, (id, c1, c2) in dict(
                checkouts=("a", "A", "Alpha"),
                builds=("b", "B", "Beta"),
                issues=("f", "F", "Feta")
            ).items()
        )

        # Check deterministic value picking between same-ID objects
        deduped = V2.dedup(V2.new() | dict(
            checkouts=[dict(id="a", comment="A"),
                       dict(id="a", comment="Alpha")],
            builds=[dict(id="b", comment="B"),
                    dict(id="b", comment="Beta")],
            issues=[dict(id="f", version=0xf, comment="F"),
                    dict(id="f", version=0xf, comment="Feta")],
        ), pick_second=lambda: False)
        assert deduped == V2.new() | dict(
            checkouts=[dict(id="a", comment="A")],
            builds=[dict(id="b", comment="B")],
            issues=[dict(id="f", version=0xf, comment="F")],
        )
        deduped = V2.dedup(V2.new() | dict(
            checkouts=[dict(id="a", comment="A"),
                       dict(id="a", comment="Alpha")],
            builds=[dict(id="b", comment="B"),
                    dict(id="b", comment="Beta")],
            issues=[dict(id="f", version=0xf, comment="F"),
                    dict(id="f", version=0xf, comment="Feta")],
        ), pick_second=lambda: True)
        assert deduped == V2.new() | dict(
            checkouts=[dict(id="a", comment="Alpha")],
            builds=[dict(id="b", comment="Beta")],
            issues=[dict(id="f", version=0xf, comment="Feta")],
        )
