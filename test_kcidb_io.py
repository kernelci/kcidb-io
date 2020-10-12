"""kcidb_io module test"""

import unittest
from kcidb_io.misc import LIGHT_ASSERTS


class LightAssertsTestCase(unittest.TestCase):
    """Light assertions test case"""

    def test_light_asserts_are_disabled(self):
        """Check light asserts are disabled"""
        self.assertFalse(LIGHT_ASSERTS,
                         "Tests must run with KCIDB_IO_HEAVY_ASSERTS "
                         "environment variable set to a non-empty string")
