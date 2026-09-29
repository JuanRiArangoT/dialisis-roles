from unittest.mock import Mock
from uuid import UUID

import pytest

from roles.application.exceptions.permission_exceptions import (
    PermissionConflictError,
)
from roles.application.use_cases.create_permission import (
    CreatePermissionUseCase,
)


def test_create_permission_success() -> None:
    repository = Mock()
    repository.get_by_name.return_value = None
    repository.create.side_effect = lambda permission: permission

    use_case = CreatePermissionUseCase(repository)

    permission = use_case.execute(
        name="users.read",
        description="Permite consultar usuarios",
    )

    assert permission.name == "users.read"
    assert permission.description == "Permite consultar usuarios"
    assert permission.is_active is True
    assert UUID(permission.id)

    repository.get_by_name.assert_called_once_with("users.read")
    repository.create.assert_called_once_with(permission)


def test_create_permission_conflict() -> None:
    repository = Mock()
    repository.get_by_name.return_value = Mock()

    use_case = CreatePermissionUseCase(repository)

    with pytest.raises(PermissionConflictError):
        use_case.execute(
            name="users.read",
            description="Permite consultar usuarios",
        )

    repository.get_by_name.assert_called_once_with("users.read")
    repository.create.assert_not_called()