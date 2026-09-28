from datetime import UTC, datetime
from unittest.mock import Mock

import pytest

from roles.application.exceptions.role_exceptions import (
    RoleNotFoundApplicationError,
)
from roles.application.use_cases.get_role import GetRoleUseCase
from roles.domain.entities.role import Role


def test_get_role_success():
    repository = Mock()

    now = datetime.now(UTC)

    role = Role(
        id="89f4d538-9c56-4fd3-b6fb-39268dcb1d53",
        name="Administrador",
        description="Rol administrativo",
        is_active=True,
        created_at=now,
        updated_at=now,
    )

    repository.get_by_id.return_value = role

    use_case = GetRoleUseCase(repository)

    result = use_case.execute(role.id)

    assert result.id == role.id
    assert result.name == role.name
    assert result.description == role.description
    assert result.is_active is True
    assert result.created_at == now
    assert result.updated_at == now

    repository.get_by_id.assert_called_once_with(role.id)


def test_get_role_not_found():
    repository = Mock()

    role_id = "00000000-0000-0000-0000-000000000000"

    repository.get_by_id.return_value = None

    use_case = GetRoleUseCase(repository)

    with pytest.raises(RoleNotFoundApplicationError) as exc_info:
        use_case.execute(role_id)

    assert str(exc_info.value) == f"Role not found: {role_id}"

    repository.get_by_id.assert_called_once_with(role_id)