from unittest.mock import Mock

import pytest

from roles.application.exceptions.role_exceptions import (
    RoleNotFoundApplicationError,
)
from roles.application.use_cases.list_role_permissions import (
    ListRolePermissionsUseCase,
)


def test_list_role_permissions_success() -> None:
    role_repository = Mock()
    permission_repository = Mock()
    role_permission_repository = Mock()

    role_repository.get_by_id.return_value = Mock()
    role_permission_repository.get_permission_ids_by_role.return_value = [
        "permission-1",
        "permission-2",
    ]

    permission_1 = Mock()
    permission_1.id = "permission-1"
    permission_1.name = "users.read"

    permission_2 = Mock()
    permission_2.id = "permission-2"
    permission_2.name = "users.create"

    permission_repository.get_by_id.side_effect = [
        permission_1,
        permission_2,
    ]

    use_case = ListRolePermissionsUseCase(
        role_repository,
        permission_repository,
        role_permission_repository,
    )

    result = use_case.execute("role-123")

    assert result == [permission_1, permission_2]
    assert result[0].name == "users.read"
    assert result[1].name == "users.create"

    role_repository.get_by_id.assert_called_once_with("role-123")
    role_permission_repository.get_permission_ids_by_role.assert_called_once_with(
        "role-123"
    )
    assert permission_repository.get_by_id.call_count == 2


def test_list_role_permissions_role_not_found() -> None:
    role_repository = Mock()
    permission_repository = Mock()
    role_permission_repository = Mock()

    role_repository.get_by_id.return_value = None

    use_case = ListRolePermissionsUseCase(
        role_repository,
        permission_repository,
        role_permission_repository,
    )

    with pytest.raises(RoleNotFoundApplicationError):
        use_case.execute("role-123")

    role_permission_repository.get_permission_ids_by_role.assert_not_called()
    permission_repository.get_by_id.assert_not_called()