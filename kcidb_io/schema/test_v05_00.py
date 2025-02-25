"""v05_00 module tests"""

import pytest
from kcidb_io.schema.abstract import InheritanceImpossible
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


def test_build_valid_upgrade():
    """Test upgrading build valid property"""
    old_data = dict(
        **Version.previous.new(),
        builds=[
            dict(
                id='origin:valid_missing',
                origin='origin',
                checkout_id='origin:1',
            ),
            dict(
                id='origin:valid_false',
                origin='origin',
                checkout_id='origin:1',
                valid=False,
            ),
            dict(
                id='origin:valid_true',
                origin='origin',
                checkout_id='origin:1',
                valid=True,
            ),
        ]
    )
    new_data = dict(
        **Version.new(),
        builds=[
            dict(
                id='origin:valid_missing',
                origin='origin',
                checkout_id='origin:1',
            ),
            dict(
                id='origin:valid_false',
                origin='origin',
                checkout_id='origin:1',
                status='FAIL',
            ),
            dict(
                id='origin:valid_true',
                origin='origin',
                checkout_id='origin:1',
                status='PASS',
            ),
        ]
    )
    assert Version.previous.is_valid_exactly(old_data)
    assert Version.is_valid_exactly(new_data)
    assert Version.upgrade(old_data) == new_data


def test_path_restriction():
    """Test new test path restrictions are effective"""
    data_correct = dict(
        **Version.previous.new(),
        tests=[
            dict(
                id='origin:correct1',
                origin='origin',
                build_id='origin:1',
                path='',
            ),
            dict(
                id='origin:correct2',
                origin='origin',
                build_id='origin:1',
                path='ltp',
            ),
            dict(
                id='origin:correct3',
                origin='origin',
                build_id='origin:1',
                path='ltp.memcpy',
            ),
            dict(
                id='origin:correct4',
                origin='origin',
                build_id='origin:1',
                path='ltp.memcpy.subtest',
            ),
        ],
    )

    data_incorrect_list = [
        dict(**Version.previous.new(), tests=[dict(
            id='origin:new_incorrect1',
            origin='origin',
            build_id='origin:1',
            path='.',
        ),],),
        dict(**Version.previous.new(), tests=[dict(
            id='origin:new_incorrect2',
            origin='origin',
            build_id='origin:1',
            path='..',
        ),],),
        dict(**Version.previous.new(), tests=[dict(
            id='origin:new_incorrect3',
            origin='origin',
            build_id='origin:1',
            path='ltp.',
        ),],),
        dict(**Version.previous.new(), tests=[dict(
            id='origin:new_incorrect4',
            origin='origin',
            build_id='origin:1',
            path='ltp..',
        ),],),
        dict(**Version.previous.new(), tests=[dict(
            id='origin:new_incorrect5',
            origin='origin',
            build_id='origin:1',
            path='.ltp',
        ),],),
        dict(**Version.previous.new(), tests=[dict(
            id='origin:new_incorrect6',
            origin='origin',
            build_id='origin:1',
            path='..ltp',
        ),],),
        dict(**Version.previous.new(), tests=[dict(
            id='origin:new_incorrect7',
            origin='origin',
            build_id='origin:1',
            path='ltp..memcpy',
        ),],),
        dict(**Version.previous.new(), tests=[dict(
            id='origin:new_incorrect8',
            origin='origin',
            build_id='origin:1',
            path='ltp.memcpy.',
        ),],),
        dict(**Version.previous.new(), tests=[dict(
            id='origin:new_incorrect9',
            origin='origin',
            build_id='origin:1',
            path='.ltp.memcpy',
        ),],),
    ]

    assert Version.previous.is_valid_exactly(data_correct)
    data_correct_upgraded = data_correct.copy()
    data_correct_upgraded.update(**Version.new())
    assert Version.is_valid_exactly(data_correct_upgraded)
    assert data_correct_upgraded == Version.upgrade(data_correct)

    for data_incorrect in data_incorrect_list:
        assert Version.previous.is_valid_exactly(data_incorrect)
        with pytest.raises(InheritanceImpossible):
            Version.upgrade(data_incorrect)
        data_incorrect_upgraded = data_incorrect.copy()
        data_incorrect_upgraded.update(**Version.new())
        assert not Version.is_valid_exactly(data_incorrect_upgraded)
