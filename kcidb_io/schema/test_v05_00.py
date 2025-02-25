"""v05_00 module tests"""

from kcidb_io.schema.v05_00 import Version

# We like our "id" pylint: disable=redefined-builtin


def test_empty_upgrade():
    """Test upgrading an empty dataset"""
    assert Version.upgrade(Version.previous.new()) == Version.new()


def test_contacts_removal():
    """Check contacts field is being removed"""
    old_data = dict(
        **Version.previous.new(),
        checkouts=[
            dict(
                id="origin:1", origin="origin",
                contacts=["spbnick@gmail.com"],
            ),
            dict(
                id="origin:2", origin="origin",
                contacts=[],
            ),
        ],
    )
    new_data = dict(
        **Version.new(),
        checkouts=[
            dict(
                id="origin:1", origin="origin",
            ),
            dict(
                id="origin:2", origin="origin",
            ),
        ],
    )
    invalid_upgraded_data = old_data.copy()
    invalid_upgraded_data.update(**Version.new())
    assert not Version.is_valid_exactly(invalid_upgraded_data)
    assert Version.previous.is_valid_exactly(old_data)
    assert Version.is_valid_exactly(new_data)
    assert Version.upgrade(old_data) == new_data
