"""v5 module tests"""

import unittest
from kcidb_io.schema.v5 import VERSION

# Disable long line checking for JSON data
# flake8: noqa
# pylint: disable=line-too-long


class UpgradeTestCase(unittest.TestCase):
    """upgrade() test case"""

    def setUp(self):
        """Setup tests"""
        # pylint: disable=invalid-name
        self.maxDiff = None

    def test_upgrade(self):
        """Check upgrade works in general"""
        prev_version_data = dict(
            version=dict(major=VERSION.previous.major,
                         minor=VERSION.previous.minor),
            checkouts=[
                dict(id="origin1:5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     origin="origin1"),
                dict(id="origin2:5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e"
                        "+01ba4719c80b6fe911b091a7c05124b64eeece9"
                        "64e09c058ef8f9805daca546b",
                     patchset_hash="01ba4719c80b6fe911b091a7c05124b6"
                                   "4eeece964e09c058ef8f9805daca546b",
                     origin="origin2")
            ],
            builds=[
                dict(checkout_id="origin1:"
                                 "5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     id="origin1:1",
                     origin="origin1"),
                dict(checkout_id="origin2:"
                                 "5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e"
                                 "+01ba4719c80b6fe911b091a7c05124b64eeece9"
                                 "64e09c058ef8f9805daca546b",
                     id="origin2:2",
                     origin="origin2"),
            ],
            tests=[
                dict(build_id="origin1:1", id="origin4:1-1", origin="origin4"),
                dict(build_id="origin1:1", id="origin5:1-2", origin="origin5"),
                dict(build_id="origin2:2", id="origin6:2-1", origin="origin6"),
                dict(build_id="origin2:2", id="origin7:2-2", origin="origin7"),
            ],
        )
        new_version_data = dict(
            version=dict(major=VERSION.major,
                         minor=VERSION.minor),
            checkouts=[
                dict(id="origin1:5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     origin="origin1"),
                dict(id="origin2:5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e"
                        "+01ba4719c80b6fe911b091a7c05124b64eeece9"
                        "64e09c058ef8f9805daca546b",
                     patchset_hash="01ba4719c80b6fe911b091a7c05124b6"
                                   "4eeece964e09c058ef8f9805daca546b",
                     origin="origin2")
            ],
            builds=[
                dict(checkout_id="origin1:"
                                 "5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     id="origin1:1",
                     origin="origin1"),
                dict(checkout_id="origin2:"
                                 "5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e"
                                 "+01ba4719c80b6fe911b091a7c05124b64eeece9"
                                 "64e09c058ef8f9805daca546b",
                     id="origin2:2",
                     origin="origin2"),
            ],
            tests=[
                dict(build_id="origin1:1", id="origin4:1-1", origin="origin4"),
                dict(build_id="origin1:1", id="origin5:1-2", origin="origin5"),
                dict(build_id="origin2:2", id="origin6:2-1", origin="origin6"),
                dict(build_id="origin2:2", id="origin7:2-2", origin="origin7"),
            ],
        )

        self.assertEqual(VERSION.upgrade(prev_version_data), new_version_data)
