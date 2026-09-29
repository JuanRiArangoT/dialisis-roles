from roles.application.exceptions.role_exceptions import (
    RoleNotFoundApplicationError,
)
from roles.domain.repositories.permission_repository import (
    PermissionRepositoryPort,
)
from roles.domain.repositories.role_permission_repository import (
    RolePermissionRepositoryPort,
)
from roles.domain.repositories.role_repository import RoleRepositoryPort


class ListRolePermissionsUseCase:
    def __init__(
        self,
        role_repository: RoleRepositoryPort,
        permission_repository: PermissionRepositoryPort,
        role_permission_repository: RolePermissionRepositoryPort,
    ) -> None:
        self._role_repository = role_repository
        self._permission_repository = permission_repository
        self._role_permission_repository = role_permission_repository

    def execute(self, role_id: str):
        role = self._role_repository.get_by_id(role_id)
        if role is None:
            raise RoleNotFoundApplicationError(
                f"Role not found: {role_id}"
            )

        permission_ids = (
            self._role_permission_repository.get_permission_ids_by_role(
                role_id
            )
        )

        return [
            self._permission_repository.get_by_id(permission_id)
            for permission_id in permission_ids
        ]