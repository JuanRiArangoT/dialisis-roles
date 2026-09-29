from unittest.mock import Mock

import pytest

from roles.application.exceptions.permission_exceptions import (
    PermissionNotFoundApplicationError,
)
from roles.application.use_cases.delete_permission import DeletePermissionUseCase


def test_delete_permission_success() -> None:
    repository = Mock()

    permission = Mock()
    permission.id = "permission-123"

    repository.get_by_id.return_value = permission

    use_case = DeletePermissionUseCase(repository)

    result = use_case.execute("permission-123")

    assert result is None

    repository.get_by_id.assert_called_once_with("permission-123")
    repository.delete.assert_called_once_with("permission-123")


def test_delete_permission_not_found() -> None:
    repository = Mock()
    repository.get_by_id.return_value = None

    use_case = DeletePermissionUseCase(repository)

    with pytest.raises(PermissionNotFoundApplicationError):
        use_case.execute("permission-123")

    repository.get_by_id.assert_called_once_with("permission-123")
    repository.delete.assert_not_called()