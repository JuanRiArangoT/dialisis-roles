from roles.application.exceptions.permission_exceptions import (
    PermissionNotFoundApplicationError,
)
from roles.application.exceptions.role_exceptions import (
    RoleNotFoundApplicationError,
)
from roles.domain.repositories.permission_repository import (
    PermissionRepositoryPort,
)
from roles.domain.repositories.role_permission_repository import (
    RolePermissionRepositoryPort,
)
from roles.domain.repositories.role_repository import (
    RoleRepositoryPort,
)


class CheckRolePermissionUseCase:
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
        permission_name: str,
    ) -> bool:
        role = self._role_repository.get_by_id(role_id)

        if role is None:
            raise RoleNotFoundApplicationError(
                f"Role not found: {role_id}"
            )

        permission = self._permission_repository.get_by_name(
            permission_name
        )

        if permission is None:
            raise PermissionNotFoundApplicationError(
                f"Permission not found: {permission_name}"
            )

        return self._role_permission_repository.has_permission(
            role_id=role_id,
            permission_id=permission.id,
        )