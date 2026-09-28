from datetime import UTC, datetime
from unittest.mock import Mock

from roles.application.use_cases.list_roles import ListRolesUseCase
from roles.domain.entities.role import Role


def test_list_roles_success():
    repository = Mock()

    now = datetime.now(UTC)

    roles = [
        Role(
            id="89f4d538-9c56-4fd3-b6fb-39268dcb1d53",
            name="Administrador",
            description="Rol administrativo",
            is_active=True,
            created_at=now,
            updated_at=now,
        ),
        Role(
            id="58f2bb52-a2f7-4070-870c-404b334413d0",
            name="Medico",
            description="Rol para medicos",
            is_active=True,
            created_at=now,
            updated_at=now,
        ),
    ]

    repository.get_all.return_value = roles

    use_case = ListRolesUseCase(repository)

    result = use_case.execute()

    assert len(result) == 2

    assert result[0].id == roles[0].id
    assert result[0].name == "Administrador"
    assert result[0].description == "Rol administrativo"
    assert result[0].is_active is True

    assert result[1].id == roles[1].id
    assert result[1].name == "Medico"
    assert result[1].description == "Rol para medicos"
    assert result[1].is_active is True

    repository.get_all.assert_called_once()