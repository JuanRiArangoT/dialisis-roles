from roles.domain.entities.permission import Permission
from roles.domain.repositories.permission_repository import (
    PermissionRepositoryPort,
)


class ListPermissionsUseCase:
    def __init__(
        self,
        permission_repository: PermissionRepositoryPort,
    ) -> None:
        self._permission_repository = permission_repository

    def execute(self) -> list[Permission]:
        return self._permission_repository.get_all()