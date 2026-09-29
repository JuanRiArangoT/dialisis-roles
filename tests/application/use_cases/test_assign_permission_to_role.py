from unittest.mock import Mock

import pytest

from roles.application.exceptions.permission_exceptions import (
    PermissionNotFoundApplicationError,
)
from roles.application.exceptions.role_exceptions import (
    RoleNotFoundApplicationError,
)
from roles.application.exceptions.role_permission_exceptions import (
    RolePermissionConflictError,
)
from roles.application.use_cases.assign_permission_to_role import (
    AssignPermissionToRoleUseCase,
)


def test_assign_permission_to_role_success() -> None:
    role_repository = Mock()
    permission_repository = Mock()
    role_permission_repository = Mock()

    role_repository.get_by_id.return_value = Mock()
    permission_repository.get_by_id.return_value = Mock()
    role_permission_repository.permission_exists_for_role.return_value = False

    use_case = AssignPermissionToRoleUseCase(
        role_repository,
        permission_repository,
        role_permission_repository,
    )

    result = use_case.execute(
        role_id="role-123",
        permission_id="permission-123",
    )

    assert result is None

    role_repository.get_by_id.assert_called_once_with("role-123")
    permission_repository.get_by_id.assert_called_once_with("permission-123")
    role_permission_repository.permission_exists_for_role.assert_called_once_with(
        "role-123",
        "permission-123",
    )
    role_permission_repository.assign_permission.assert_called_once_with(
        "role-123",
        "permission-123",
    )


def test_assign_permission_to_role_role_not_found() -> None:
    role_repository = Mock()
    permission_repository = Mock()
    role_permission_repository = Mock()

    role_repository.get_by_id.return_value = None

    use_case = AssignPermissionToRoleUseCase(
        role_repository,
        permission_repository,
        role_permission_repository,
    )

    with pytest.raises(RoleNotFoundApplicationError):
        use_case.execute(
            role_id="role-123",
            permission_id="permission-123",
        )

    permission_repository.get_by_id.assert_not_called()
    role_permission_repository.assign_permission.assert_not_called()


def test_assign_permission_to_role_permission_not_found() -> None:
    role_repository = Mock()
    permission_repository = Mock()
    role_permission_repository = Mock()

    role_repository.get_by_id.return_value = Mock()
    permission_repository.get_by_id.return_value = None

    use_case = AssignPermissionToRoleUseCase(
        role_repository,
        permission_repository,
        role_permission_repository,
    )

    with pytest.raises(PermissionNotFoundApplicationError):
        use_case.execute(
            role_id="role-123",
            permission_id="permission-123",
        )

    role_permission_repository.assign_permission.assert_not_called()


def test_assign_permission_to_role_conflict() -> None:
    role_repository = Mock()
    permission_repository = Mock()
    role_permission_repository = Mock()

    role_repository.get_by_id.return_value = Mock()
    permission_repository.get_by_id.return_value = Mock()
    role_permission_repository.permission_exists_for_role.return_value = True

    use_case = AssignPermissionToRoleUseCase(
        role_repository,
        permission_repository,
        role_permission_repository,
    )

    with pytest.raises(RolePermissionConflictError):
        use_case.execute(
            role_id="role-123",
            permission_id="permission-123",
        )

    role_permission_repository.assign_permission.assert_not_called()