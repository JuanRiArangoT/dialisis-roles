from roles.application.exceptions.permission_exceptions import (
    PermissionNotFoundApplicationError,
)
from roles.domain.repositories.permission_repository import (
    PermissionRepositoryPort,
)


class DeletePermissionUseCase:
    def __init__(
        self,
        permission_repository: PermissionRepositoryPort,
    ) -> None:
        self._permission_repository = permission_repository

    def execute(self, permission_id: str) -> None:
        permission = self._permission_repository.get_by_id(permission_id)

        if permission is None:
            raise PermissionNotFoundApplicationError(
                f"Permission not found: {permission_id}"
            )

        self._permission_repository.delete(permission_id)