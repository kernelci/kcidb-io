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
