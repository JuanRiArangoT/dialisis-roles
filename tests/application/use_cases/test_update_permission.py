from unittest.mock import Mock

import pytest

from roles.application.exceptions.permission_exceptions import (
    PermissionConflictError,
    PermissionNotFoundApplicationError,
)
from roles.application.use_cases.update_permission import UpdatePermissionUseCase


def test_update_permission_success() -> None:
    repository = Mock()

    current_permission = Mock()
    current_permission.id = "permission-123"
    current_permission.name = "users.read"
    current_permission.description = "Descripción anterior"
    current_permission.is_active = True
    current_permission.created_at = Mock()

    repository.get_by_id.return_value = current_permission
    repository.get_by_name.return_value = None
    repository.update.side_effect = lambda permission: permission

    use_case = UpdatePermissionUseCase(repository)

    result = use_case.execute(
        permission_id="permission-123",
        description="Descripción actualizada",
    )

    assert result.id == "permission-123"
    assert result.name == "users.read"
    assert result.description == "Descripción actualizada"
    assert result.is_active is True
    assert result.created_at is current_permission.created_at

    repository.get_by_id.assert_called_once_with("permission-123")
    repository.update.assert_called_once_with(result)


def test_update_permission_not_found() -> None:
    repository = Mock()
    repository.get_by_id.return_value = None

    use_case = UpdatePermissionUseCase(repository)

    with pytest.raises(PermissionNotFoundApplicationError):
        use_case.execute(
            permission_id="permission-123",
            description="Nueva descripción",
        )

    repository.get_by_id.assert_called_once_with("permission-123")
    repository.update.assert_not_called()


def test_update_permission_name_conflict() -> None:
    repository = Mock()

    current_permission = Mock()
    current_permission.id = "permission-123"
    current_permission.name = "users.read"
    current_permission.description = "Descripción"
    current_permission.is_active = True
    current_permission.created_at = Mock()

    repository.get_by_id.return_value = current_permission
    repository.get_by_name.return_value = Mock()

    use_case = UpdatePermissionUseCase(repository)

    with pytest.raises(PermissionConflictError):
        use_case.execute(
            permission_id="permission-123",
            name="users.create",
        )

    repository.get_by_id.assert_called_once_with("permission-123")
    repository.get_by_name.assert_called_once_with("users.create")
    repository.update.assert_not_called()