"""v05_00 module tests"""

from kcidb_io.schema.v05_00 import Version

# We like our "id" pylint: disable=redefined-builtin


def test_empty_upgrade():
    """Test upgrading an empty dataset"""
    assert Version.upgrade(Version.previous.new()) == Version.new()
