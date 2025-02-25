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


def test_build_valid_test_status_removal():
    """Check build_valid and test_status fields are removed from issues"""
    old_data1 = dict(**Version.previous.new(), issues=[
        dict(
            id="origin:1", origin="origin", version=1,
            build_valid=True,
        ),
    ],)
    old_data2 = dict(**Version.previous.new(), issues=[
        dict(
            id="origin:2", origin="origin", version=1,
            test_status="PASS",
        ),
    ],)

    new_data1 = dict(**Version.new(), issues=[
        dict(id="origin:1", origin="origin", version=1,),
    ],)
    new_data2 = dict(**Version.new(), issues=[
        dict(id="origin:2", origin="origin", version=1,),
    ],)

    assert Version.previous.is_valid_exactly(old_data1)
    assert Version.is_valid_exactly(new_data1)
    assert Version.upgrade(old_data1) == new_data1

    assert Version.previous.is_valid_exactly(old_data2)
    assert Version.is_valid_exactly(new_data2)
    assert Version.upgrade(old_data2) == new_data2

    invalid_upgraded_data1 = old_data1.copy()
    invalid_upgraded_data1.update(**Version.new())
    assert not Version.is_valid_exactly(invalid_upgraded_data1)

    invalid_upgraded_data2 = old_data2.copy()
    invalid_upgraded_data2.update(**Version.new())
    assert not Version.is_valid_exactly(invalid_upgraded_data2)
