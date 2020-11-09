"""v4 module tests"""

import unittest
from kcidb_io.schema.v4 import VERSION

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
            revisions=[
                dict(id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     origin="origin1")
            ],
            builds=[
                dict(revision_id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     id="origin2:1",
                     origin="origin2"),
                dict(revision_id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     id="origin3:2",
                     origin="origin3"),
            ],
            tests=[
                dict(build_id="origin2:1", id="origin4:1-1", origin="origin4"),
                dict(build_id="origin2:1", id="origin5:1-2", origin="origin5"),
                dict(build_id="origin3:2", id="origin6:2-1", origin="origin6"),
                dict(build_id="origin3:2", id="origin7:2-2", origin="origin7"),
            ],
        )
        new_version_data = dict(
            version=dict(major=VERSION.major,
                         minor=VERSION.minor),
            revisions=[
                dict(id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     origin="origin1",
                     patchset_hash="")
            ],
            builds=[
                dict(revision_id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     id="origin2:1",
                     origin="origin2"),
                dict(revision_id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     id="origin3:2",
                     origin="origin3"),
            ],
            tests=[
                dict(build_id="origin2:1", id="origin4:1-1", origin="origin4"),
                dict(build_id="origin2:1", id="origin5:1-2", origin="origin5"),
                dict(build_id="origin3:2", id="origin6:2-1", origin="origin6"),
                dict(build_id="origin3:2", id="origin7:2-2", origin="origin7"),
            ],
        )

        self.assertEqual(VERSION.upgrade(prev_version_data), new_version_data)

    def test_inherit_patchset_files(self):
        """Check revision's patchset_files are inherited appropriately"""
        prev_version_data = dict(
            version=dict(major=VERSION.previous.major,
                         minor=VERSION.previous.minor),
            revisions=[
                dict(id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     origin="origin1",
                     patch_mboxes=[
                         dict(name="0001.patch",
                              url="https://example.com/0001.patch"),
                         dict(name="0002.patch",
                              url="https://example.com/0002.patch"),
                     ]),
                dict(id="6150cc0cf631fdf766321368464e9f403fef3428",
                     origin="origin2",
                     patch_mboxes=[]),
                dict(id="3f1c54e6d648205fa1e3d3b405740e0d162ea264",
                     origin="origin3"),
            ],
        )
        new_version_data = dict(
            version=dict(major=VERSION.major,
                         minor=VERSION.minor),
            revisions=[
                dict(id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     origin="origin1",
                     patchset_files=[
                         dict(name="0001.patch",
                              url="https://example.com/0001.patch"),
                         dict(name="0002.patch",
                              url="https://example.com/0002.patch"),
                     ],
                     patchset_hash=""),
                dict(id="6150cc0cf631fdf766321368464e9f403fef3428",
                     origin="origin2",
                     patchset_files=[],
                     patchset_hash=""),
                dict(id="3f1c54e6d648205fa1e3d3b405740e0d162ea264",
                     origin="origin3",
                     patchset_hash="")
            ],
        )

        self.assertEqual(VERSION.upgrade(prev_version_data), new_version_data)

    def test_inherit_patchset_hash(self):
        """Check revision's patchset_hash is inherited appropriately"""
        prev_version_data = dict(
            version=dict(major=VERSION.previous.major,
                         minor=VERSION.previous.minor),
            revisions=[
                dict(id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     origin="origin1"),
                dict(id="6150cc0cf631fdf766321368464e9f403fef3428+"
                        "e3b0c44298fc1c149afbf4c8996fb92427ae41e46"
                        "49b934ca495991b7852b855",
                     origin="origin2"),
            ],
        )
        new_version_data = dict(
            version=dict(major=VERSION.major,
                         minor=VERSION.minor),
            revisions=[
                dict(id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     origin="origin1",
                     patchset_hash=""),
                dict(id="6150cc0cf631fdf766321368464e9f403fef3428+"
                        "e3b0c44298fc1c149afbf4c8996fb92427ae41e46"
                        "49b934ca495991b7852b855",
                     origin="origin2",
                     patchset_hash="e3b0c44298fc1c149afbf4c8996fb924"
                                   "27ae41e4649b934ca495991b7852b855"),
            ],
        )

        self.assertEqual(VERSION.upgrade(prev_version_data), new_version_data)
