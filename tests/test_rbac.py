import pytest

from fastapi import HTTPException

from app.core.permissions import check_permission


def test_admin_can_select():
    assert check_permission("admin", "SELECT") is True


def test_admin_can_update():
    assert check_permission("admin", "UPDATE") is True


def test_analyst_can_select():
    assert check_permission("analyst", "SELECT") is True


def test_viewer_can_select():
    assert check_permission("viewer", "SELECT") is True


def test_viewer_cannot_update():

    with pytest.raises(HTTPException) as error:
        check_permission("viewer", "UPDATE")

    assert error.value.status_code == 403


def test_analyst_cannot_delete():

    with pytest.raises(HTTPException) as error:
        check_permission("analyst", "DELETE")

    assert error.value.status_code == 403