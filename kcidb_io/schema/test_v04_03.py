"""v04_03 module tests"""

from kcidb_io.schema.v04_03 import Version


def test_has_metadata():
    """Check has_metadata() works correctly"""
    assert not Version.has_metadata(Version.new())
    assert not Version.has_metadata(dict(
        version=dict(major=Version.major, minor=Version.minor),
        checkouts=[
            dict(id="_:origin1:5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                 origin="origin1",
                 patchset_hash="")
        ]
    ))
    assert not Version.has_metadata(dict(
        version=dict(major=Version.major, minor=Version.minor),
        checkouts=[
            dict(id="_:origin1:5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                 origin="origin1",
                 patchset_hash="",
                 misc=dict(_timestamp="2023-11-06T11:58:15.163000+00:00"))
        ]
    ))
    assert Version.has_metadata(dict(
        version=dict(major=Version.major, minor=Version.minor),
        checkouts=[
            dict(id="_:origin1:5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                 origin="origin1",
                 patchset_hash="",
                 _timestamp="2023-11-06T11:58:15.163000+00:00"),
        ]
    ))


def test_strip_metadata():
    """Check strip_metadata() works correctly"""
    assert Version.strip_metadata(Version.new()) == Version.new()

    io_without_metadata = dict(
        version=dict(major=Version.major, minor=Version.minor),
        checkouts=[
            dict(id="_:origin1:5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                 origin="origin1",
                 patchset_hash="")
        ]
    )
    assert Version.strip_metadata(io_without_metadata) == io_without_metadata

    io_with_misc_metadata = dict(
        version=dict(major=Version.major, minor=Version.minor),
        checkouts=[
            dict(id="_:origin1:5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                 origin="origin1",
                 patchset_hash="",
                 misc=dict(_timestamp="2023-11-06T11:58:15.163000+00:00"))
        ]
    )
    assert Version.strip_metadata(io_with_misc_metadata) == \
        io_with_misc_metadata

    io_with_metadata = dict(
        version=dict(major=Version.major, minor=Version.minor),
        checkouts=[
            dict(id="_:origin1:5e29d1443c46b6ca70a4c940a67e8c09f05dcb7e",
                 origin="origin1",
                 patchset_hash="",
                 _timestamp="2023-11-06T11:58:15.163000+00:00"),
        ]
    )
    assert Version.strip_metadata(io_with_metadata) == io_without_metadata
