from unittest.mock import Mock

import pytest

from roles.application.exceptions.permission_exceptions import (
    PermissionNotFoundApplicationError,
)
from roles.application.use_cases.get_permission import GetPermissionUseCase


def test_get_permission_success() -> None:
    repository = Mock()
    permission = Mock()
    permission.id = "permission-123"
    permission.name = "users.read"

    repository.get_by_id.return_value = permission

    use_case = GetPermissionUseCase(repository)

    result = use_case.execute("permission-123")

    assert result is permission
    assert result.id == "permission-123"
    assert result.name == "users.read"

    repository.get_by_id.assert_called_once_with("permission-123")


def test_get_permission_not_found() -> None:
    repository = Mock()
    repository.get_by_id.return_value = None

    use_case = GetPermissionUseCase(repository)

    with pytest.raises(PermissionNotFoundApplicationError):
        use_case.execute("permission-123")

    repository.get_by_id.assert_called_once_with("permission-123")