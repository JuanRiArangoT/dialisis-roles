from datetime import UTC, datetime
from uuid import uuid4

from roles.application.exceptions.permission_exceptions import (
    PermissionConflictError,
)
from roles.domain.entities.permission import Permission
from roles.domain.repositories.permission_repository import (
    PermissionRepositoryPort,
)


class CreatePermissionUseCase:
    def __init__(
        self,
        permission_repository: PermissionRepositoryPort,
    ) -> None:
        self._permission_repository = permission_repository

    def execute(
        self,
        name: str,
        description: str | None = None,
    ) -> Permission:
        existing_permission = self._permission_repository.get_by_name(name)

        if existing_permission is not None:
            raise PermissionConflictError(
                f"A permission with the name '{name}' already exists."
            )

        now = datetime.now(UTC)

        permission = Permission(
            id=str(uuid4()),
            name=name,
            description=description,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        return self._permission_repository.create(permission)