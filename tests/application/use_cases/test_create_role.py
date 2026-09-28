from datetime import UTC, datetime
from unittest.mock import Mock
from uuid import UUID

from roles.application.exceptions.role_exceptions import RoleConflictError
from roles.application.use_cases.create_role import CreateRoleUseCase
from roles.domain.entities.role import Role


def test_create_role_success():
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

    repository.get_by_name.return_value = None
    repository.create.return_value = role

    use_case = CreateRoleUseCase(repository)

    result = use_case.execute(
        name="Administrador",
        description="Rol administrativo",
    )

    assert result.id == role.id
    assert result.name == "Administrador"
    assert result.description == "Rol administrativo"
    assert result.is_active is True

    UUID(result.id)

    repository.get_by_name.assert_called_once_with("Administrador")
    repository.create.assert_called_once()

def test_create_role_conflict():
    repository = Mock()

    existing_role = Role(
        id="89f4d538-9c56-4fd3-b6fb-39268dcb1d53",
        name="Administrador",
        description="Rol administrativo",
        is_active=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    repository.get_by_name.return_value = existing_role

    use_case = CreateRoleUseCase(repository)

    try:
        use_case.execute(
            name="Administrador",
            description="Otro rol",
        )
    except RoleConflictError as exc:
        assert str(exc) == "Role already exists: Administrador"
    else:
        raise AssertionError("Expected RoleConflictError")

    repository.create.assert_not_called()