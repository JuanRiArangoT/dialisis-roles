from roles.application.exceptions.permission_exceptions import (
    PermissionNotFoundApplicationError,
)
from roles.application.exceptions.role_exceptions import (
    RoleNotFoundApplicationError,
)
from roles.application.exceptions.role_permission_exceptions import (
    RolePermissionConflictError,
)
from roles.domain.repositories.permission_repository import (
    PermissionRepositoryPort,
)
from roles.domain.repositories.role_permission_repository import (
    RolePermissionRepositoryPort,
)
from roles.domain.repositories.role_repository import RoleRepositoryPort


class AssignPermissionToRoleUseCase:
    def __init__(
        self,
        role_repository: RoleRepositoryPort,
        permission_repository: PermissionRepositoryPort,
        role_permission_repository: RolePermissionRepositoryPort,
    ) -> None:
        self._role_repository = role_repository
        self._permission_repository = permission_repository
        self._role_permission_repository = role_permission_repository

    def execute(
        self,
        role_id: str,
        permission_id: str,
    ) -> None:
        role = self._role_repository.get_by_id(role_id)
        if role is None:
            raise RoleNotFoundApplicationError(
                f"Role not found: {role_id}"
            )

        permission = self._permission_repository.get_by_id(permission_id)
        if permission is None:
            raise PermissionNotFoundApplicationError(
                f"Permission not found: {permission_id}"
            )

        if self._role_permission_repository.permission_exists_for_role(
            role_id,
            permission_id,
        ):
            raise RolePermissionConflictError(
                "Permission is already assigned to this role."
            )

        self._role_permission_repository.assign_permission(
            role_id,
            permission_id,
        )