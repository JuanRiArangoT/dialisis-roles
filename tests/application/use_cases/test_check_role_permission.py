from unittest.mock import Mock

import pytest

from roles.application.exceptions.permission_exceptions import (
    PermissionNotFoundApplicationError,
)
from roles.application.exceptions.role_exceptions import (
    RoleNotFoundApplicationError,
)
from roles.application.use_cases.check_role_permission import (
    CheckRolePermissionUseCase,
)


def test_check_role_permission_returns_true_when_permission_is_assigned():
    role_repository = Mock()
    permission_repository = Mock()
    role_permission_repository = Mock()

    role_repository.get_by_id.return_value = Mock()
    permission_repository.get_by_name.return_value = Mock(
        id="permission-id"
    )
    role_permission_repository.has_permission.return_value = True

    use_case = CheckRolePermissionUseCase(
        role_repository=role_repository,
        permission_repository=permission_repository,
        role_permission_repository=role_permission_repository,
    )

    result = use_case.execute(
        role_id="role-id",
        permission_name="patients.read",
    )

    assert result is True


def test_check_role_permission_returns_false_when_permission_is_not_assigned():
    role_repository = Mock()
    permission_repository = Mock()
    role_permission_repository = Mock()

    role_repository.get_by_id.return_value = Mock()
    permission_repository.get_by_name.return_value = Mock(
        id="permission-id"
    )
    role_permission_repository.has_permission.return_value = False

    use_case = CheckRolePermissionUseCase(
        role_repository=role_repository,
        permission_repository=permission_repository,
        role_permission_repository=role_permission_repository,
    )

    result = use_case.execute(
        role_id="role-id",
        permission_name="patients.read",
    )

    assert result is False


def test_check_role_permission_raises_when_role_does_not_exist():
    role_repository = Mock()
    permission_repository = Mock()
    role_permission_repository = Mock()

    role_repository.get_by_id.return_value = None

    use_case = CheckRolePermissionUseCase(
        role_repository=role_repository,
        permission_repository=permission_repository,
        role_permission_repository=role_permission_repository,
    )

    with pytest.raises(RoleNotFoundApplicationError):
        use_case.execute(
            role_id="role-id",
            permission_name="patients.read",
        )


def test_check_role_permission_raises_when_permission_does_not_exist():
    role_repository = Mock()
    permission_repository = Mock()
    role_permission_repository = Mock()

    role_repository.get_by_id.return_value = Mock()
    permission_repository.get_by_name.return_value = None

    use_case = CheckRolePermissionUseCase(
        role_repository=role_repository,
        permission_repository=permission_repository,
        role_permission_repository=role_permission_repository,
    )

    with pytest.raises(PermissionNotFoundApplicationError):
        use_case.execute(
            role_id="role-id",
            permission_name="patients.read",
        )