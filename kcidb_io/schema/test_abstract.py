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

            @classmethod
            def _inherit(cls, data):
                pass

        class V2(V1):
            major = 2
            minor = 0
            json = dict(title="v2")
            graph = {"": []}

            @classmethod
            def _inherit(cls, data):
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
            class V0(Version):
                major = 0
                minor = 0
                json = dict(title="v0")
                graph = {"": []}

                @classmethod
                def _inherit(cls, data):
                    pass

        with self.assertRaises(AssertionError):
            class V1WithoutInherit(Version):
                major = 1
                minor = 0
                json = dict(title="v1")
                graph = {"": []}

        with self.assertRaises(AssertionError):
            class V1WithInherit(Version):
                major = 1
                minor = 0
                json = dict(title="v1")
                graph = {"": []}

                @classmethod
                def _inherit(cls, data):
                    pass

            class V2WithoutInherit(V1WithInherit):
                major = 2
                minor = 0
                json = dict(title="v2")
                graph = {"": []}

        with self.assertRaises(AssertionError):
            class V1InvalidGraph(Version):
                major = 1
                minor = 0
                json = dict(title="v1")
                graph = {}

                @classmethod
                def _inherit(cls, data):
                    pass

        with self.assertRaises(AssertionError):
            class V1(Version):
                major = 1
                minor = 0
                json = dict(title="v1")
                graph = {"": []}

                @classmethod
                def _inherit(cls, data):
                    pass

            class V2OldMajor(V1):
                major = 1
                minor = 0
                json = dict(title="v1")
                graph = {"": []}

                @classmethod
                def _inherit(cls, data):
                    pass

        # Piss off, old pylint
        self.assertTrue(not False)

    def test_comparison(self):
        """Test schema version comparison is correct"""
        # pylint: disable=unused-variable,missing-class-docstring
        # pylint: disable=too-many-statements
        class V1(Version):
            major = 1
            minor = 0
            json = dict(title="v1")
            graph = {"": []}

            @classmethod
            def _inherit(cls, data):
                pass

        class V2A(V1):
            major = 2
            minor = 0
            json = dict(title="v2a")
            graph = {"": []}

            @classmethod
            def _inherit(cls, data):
                pass

        class V2B(V1):
            major = 2
            minor = 0
            json = dict(title="v2b")
            graph = {"": []}

            @classmethod
            def _inherit(cls, data):
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

        with self.assertRaises(NotImplementedError):
            self.assertTrue(V2A < V2B)
        with self.assertRaises(NotImplementedError):
            self.assertTrue(V2A > V2B)
        with self.assertRaises(NotImplementedError):
            self.assertTrue(V2A <= V2B)
        with self.assertRaises(NotImplementedError):
            self.assertTrue(V2A >= V2B)
