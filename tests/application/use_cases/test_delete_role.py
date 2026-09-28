from datetime import UTC, datetime
from unittest.mock import Mock

import pytest

from roles.application.exceptions.role_exceptions import (
    RoleNotFoundApplicationError,
)
from roles.application.use_cases.delete_role import DeleteRoleUseCase
from roles.domain.entities.role import Role


def test_delete_role_success():
    repository = Mock()

    role = Role(
        id="89f4d538-9c56-4fd3-b6fb-39268dcb1d53",
        name="Administrador",
        description="Rol administrativo",
        is_active=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    repository.get_by_id.return_value = role

    use_case = DeleteRoleUseCase(repository)

    result = use_case.execute(role.id)

    assert result is None

    repository.get_by_id.assert_called_once_with(role.id)
    repository.delete.assert_called_once_with(role.id)


def test_delete_role_not_found():
    repository = Mock()

    role_id = "00000000-0000-0000-0000-000000000000"

    repository.get_by_id.return_value = None

    use_case = DeleteRoleUseCase(repository)

    with pytest.raises(RoleNotFoundApplicationError) as exc_info:
        use_case.execute(role_id)

    assert str(exc_info.value) == f"Role not found: {role_id}"

    repository.get_by_id.assert_called_once_with(role_id)
    repository.delete.assert_not_called()