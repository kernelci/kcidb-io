"""v4 module tests"""

import unittest
from kcidb_io.schema.v04_00 import Version

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
            version=dict(major=Version.previous.major,
                         minor=Version.previous.minor),
            revisions=[
                dict(id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     origin="origin1"),
                dict(id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e"
                        "+01ba4719c80b6fe911b091a7c05124b64eeece9"
                        "64e09c058ef8f9805daca546b",
                     origin="origin2")
            ],
            builds=[
                dict(revision_id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     id="origin1:1",
                     origin="origin1"),
                dict(revision_id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e"
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
            version=dict(major=Version.major,
                         minor=Version.minor),
            checkouts=[
                dict(id="_:origin1:5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     origin="origin1",
                     patchset_hash=""),
                dict(id="_:origin2:5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e"
                        "+01ba4719c80b6fe911b091a7c05124b64eeece9"
                        "64e09c058ef8f9805daca546b",
                     patchset_hash="01ba4719c80b6fe911b091a7c05124b6"
                                   "4eeece964e09c058ef8f9805daca546b",
                     origin="origin2")
            ],
            builds=[
                dict(checkout_id="_:origin1:"
                                 "5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     id="origin1:1",
                     origin="origin1"),
                dict(checkout_id="_:origin2:"
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

        self.assertEqual(Version.upgrade(prev_version_data), new_version_data)

    def test_inherit_patchset_files(self):
        """Check revision's patchset_files are inherited appropriately"""
        prev_version_data = dict(
            version=dict(major=Version.previous.major,
                         minor=Version.previous.minor),
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
            version=dict(major=Version.major,
                         minor=Version.minor),
            checkouts=[
                dict(id="_:origin1:5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     origin="origin1",
                     patchset_files=[
                         dict(name="0001.patch",
                              url="https://example.com/0001.patch"),
                         dict(name="0002.patch",
                              url="https://example.com/0002.patch"),
                     ],
                     patchset_hash=""),
                dict(id="_:origin2:6150cc0cf631fdf766321368464e9f403fef3428",
                     origin="origin2",
                     patchset_files=[],
                     patchset_hash=""),
                dict(id="_:origin3:3f1c54e6d648205fa1e3d3b405740e0d162ea264",
                     origin="origin3",
                     patchset_hash="")
            ],
        )

        self.assertEqual(Version.upgrade(prev_version_data), new_version_data)

    def test_inherit_patchset_hash(self):
        """Check revision's patchset_hash is inherited appropriately"""
        prev_version_data = dict(
            version=dict(major=Version.previous.major,
                         minor=Version.previous.minor),
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
            version=dict(major=Version.major,
                         minor=Version.minor),
            checkouts=[
                dict(id="_:origin1:5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     origin="origin1",
                     patchset_hash=""),
                dict(id="_:origin2:6150cc0cf631fdf766321368464e9f403fef3428+"
                        "e3b0c44298fc1c149afbf4c8996fb92427ae41e46"
                        "49b934ca495991b7852b855",
                     origin="origin2",
                     patchset_hash="e3b0c44298fc1c149afbf4c8996fb924"
                                   "27ae41e4649b934ca495991b7852b855"),
            ],
        )

        self.assertEqual(Version.upgrade(prev_version_data), new_version_data)

    def test_inherit_discovery_time(self):
        """Check revision's discovery_time is inherited appropriately"""
        prev_version_data = dict(
            version=dict(major=Version.previous.major,
                         minor=Version.previous.minor),
            revisions=[
                dict(id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     origin="origin1",
                     discovery_time="2020-08-14T23:08:06.967000+00:00"),
                dict(id="3f1c54e6d648205fa1e3d3b405740e0d162ea264",
                     origin="origin2"),
            ],
        )
        new_version_data = dict(
            version=dict(major=Version.major,
                         minor=Version.minor),
            checkouts=[
                dict(id="_:origin1:5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     origin="origin1",
                     patchset_hash="",
                     start_time="2020-08-14T23:08:06.967000+00:00"),
                dict(id="_:origin2:3f1c54e6d648205fa1e3d3b405740e0d162ea264",
                     origin="origin2",
                     patchset_hash="")
            ],
        )

        self.assertEqual(Version.upgrade(prev_version_data), new_version_data)

    def test_drop_publishing_time(self):
        """Check revision's publishing_time is dropped appropriately"""
        prev_version_data = dict(
            version=dict(major=Version.previous.major,
                         minor=Version.previous.minor),
            revisions=[
                dict(id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     origin="origin1",
                     publishing_time="2020-08-14T23:08:06.967000+00:00"),
                dict(id="3f1c54e6d648205fa1e3d3b405740e0d162ea264",
                     origin="origin2"),
            ],
        )
        new_version_data = dict(
            version=dict(major=Version.major,
                         minor=Version.minor),
            checkouts=[
                dict(id="_:origin1:5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     origin="origin1",
                     patchset_hash=""),
                dict(id="_:origin2:3f1c54e6d648205fa1e3d3b405740e0d162ea264",
                     origin="origin2",
                     patchset_hash="")
            ],
        )

        self.assertEqual(Version.upgrade(prev_version_data), new_version_data)

    def test_description_to_comment_rename(self):
        """Check renaming 'description' to 'comment'"""
        prev_version_data = dict(
            version=dict(major=Version.previous.major,
                         minor=Version.previous.minor),
            revisions=[
                dict(id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     origin="origin1",
                     description="A revision with a comment"),
                dict(id="a538920a149edf64f9022722eb48d680bfda6dc8",
                     origin="origin1"),
            ],
            builds=[
                dict(revision_id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     id="origin2:1",
                     origin="origin2",
                     description="A build with a comment"),
                dict(revision_id="5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     id="origin3:2",
                     origin="origin3"),
            ],
            tests=[
                dict(build_id="origin2:1", id="origin4:1-1", origin="origin4",
                     description="A test with a comment"),
                dict(build_id="origin2:1", id="origin5:1-2", origin="origin5"),
                dict(build_id="origin3:2", id="origin6:2-1", origin="origin6",
                     description="Another test with a comment"),
                dict(build_id="origin3:2", id="origin7:2-2", origin="origin7"),
            ],
        )
        new_version_data = dict(
            version=dict(major=Version.major,
                         minor=Version.minor),
            checkouts=[
                dict(id="_:origin1:5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     origin="origin1",
                     patchset_hash="",
                     comment="A revision with a comment"),
                dict(id="_:origin1:a538920a149edf64f9022722eb48d680bfda6dc8",
                     origin="origin1",
                     patchset_hash=""),
            ],
            builds=[
                dict(checkout_id="_:origin2:"
                                 "5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     id="origin2:1",
                     origin="origin2",
                     comment="A build with a comment"),
                dict(checkout_id="_:origin3:"
                                 "5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                     id="origin3:2",
                     origin="origin3"),
            ],
            tests=[
                dict(build_id="origin2:1", id="origin4:1-1", origin="origin4",
                     comment="A test with a comment"),
                dict(build_id="origin2:1", id="origin5:1-2", origin="origin5"),
                dict(build_id="origin3:2", id="origin6:2-1", origin="origin6",
                     comment="Another test with a comment"),
                dict(build_id="origin3:2", id="origin7:2-2", origin="origin7"),
            ],
        )

        self.assertEqual(Version.upgrade(prev_version_data), new_version_data)
