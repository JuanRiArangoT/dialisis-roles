from datetime import UTC, datetime
from unittest.mock import Mock

import pytest

from roles.application.exceptions.role_exceptions import (
    RoleConflictError,
    RoleNotFoundApplicationError,
)
from roles.application.use_cases.update_role import UpdateRoleUseCase
from roles.domain.entities.role import Role


def test_update_role_success():
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
    repository.get_by_name.return_value = role
    repository.update.return_value = role

    use_case = UpdateRoleUseCase(repository)

    result = use_case.execute(
        role_id=role.id,
        name="Administrador",
        description="Rol administrativo actualizado",
        is_active=False,
    )

    assert result.id == role.id
    assert result.name == "Administrador"
    assert result.description == "Rol administrativo actualizado"
    assert result.is_active is False
    assert result.created_at == now

    repository.get_by_id.assert_called_once_with(role.id)
    repository.get_by_name.assert_called_once_with("Administrador")
    repository.update.assert_called_once_with(role)


def test_update_role_not_found():
    repository = Mock()

    role_id = "00000000-0000-0000-0000-000000000000"

    repository.get_by_id.return_value = None

    use_case = UpdateRoleUseCase(repository)

    with pytest.raises(RoleNotFoundApplicationError) as exc_info:
        use_case.execute(
            role_id=role_id,
            name="Administrador",
        )

    assert str(exc_info.value) == f"Role not found: {role_id}"

    repository.get_by_id.assert_called_once_with(role_id)
    repository.get_by_name.assert_not_called()
    repository.update.assert_not_called()


def test_update_role_conflict():
    repository = Mock()

    role = Role(
        id="89f4d538-9c56-4fd3-b6fb-39268dcb1d53",
        name="Administrador",
        description="Rol administrativo",
        is_active=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    existing_role = Role(
        id="58f2bb52-a2f7-4070-870c-404b334413d0",
        name="Medico",
        description="Rol para medicos",
        is_active=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    repository.get_by_id.return_value = role
    repository.get_by_name.return_value = existing_role

    use_case = UpdateRoleUseCase(repository)

    with pytest.raises(RoleConflictError) as exc_info:
        use_case.execute(
            role_id=role.id,
            name="Medico",
        )

    assert str(exc_info.value) == "Role already exists: Medico"

    repository.get_by_id.assert_called_once_with(role.id)
    repository.get_by_name.assert_called_once_with("Medico")
    repository.update.assert_not_called()