from roles.application.exceptions.permission_exceptions import (
    PermissionNotFoundApplicationError,
)
from roles.domain.entities.permission import Permission
from roles.domain.repositories.permission_repository import (
    PermissionRepositoryPort,
)


class GetPermissionUseCase:
    def __init__(
        self,
        permission_repository: PermissionRepositoryPort,
    ) -> None:
        self._permission_repository = permission_repository

    def execute(self, permission_id: str) -> Permission:
        permission = self._permission_repository.get_by_id(permission_id)

        if permission is None:
            raise PermissionNotFoundApplicationError(
                f"Permission not found: {permission_id}"
            )

        return permission