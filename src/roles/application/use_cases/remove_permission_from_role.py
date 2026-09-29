from roles.application.exceptions.role_exceptions import (
    RoleNotFoundApplicationError,
)
from roles.application.exceptions.role_permission_exceptions import (
    RolePermissionNotFoundApplicationError,
)
from roles.domain.repositories.role_permission_repository import (
    RolePermissionRepositoryPort,
)
from roles.domain.repositories.role_repository import RoleRepositoryPort


class RemovePermissionFromRoleUseCase:
    def __init__(
        self,
        role_repository: RoleRepositoryPort,
        role_permission_repository: RolePermissionRepositoryPort,
    ) -> None:
        self._role_repository = role_repository
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

        if not self._role_permission_repository.permission_exists_for_role(
            role_id,
            permission_id,
        ):
            raise RolePermissionNotFoundApplicationError(
                "Permission is not assigned to this role."
            )

        self._role_permission_repository.remove_permission(
            role_id,
            permission_id,
        )