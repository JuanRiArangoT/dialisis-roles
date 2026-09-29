from datetime import UTC, datetime

from roles.application.exceptions.permission_exceptions import (
    PermissionConflictError,
    PermissionNotFoundApplicationError,
)
from roles.domain.entities.permission import Permission
from roles.domain.repositories.permission_repository import (
    PermissionRepositoryPort,
)


class UpdatePermissionUseCase:
    def __init__(
        self,
        permission_repository: PermissionRepositoryPort,
    ) -> None:
        self._permission_repository = permission_repository

    def execute(
        self,
        permission_id: str,
        name: str | None = None,
        description: str | None = None,
        is_active: bool | None = None,
    ) -> Permission:
        current_permission = self._permission_repository.get_by_id(
            permission_id
        )

        if current_permission is None:
            raise PermissionNotFoundApplicationError(
                f"Permission not found: {permission_id}"
            )

        updated_name = (
            name if name is not None else current_permission.name
        )

        updated_description = (
            description
            if description is not None
            else current_permission.description
        )

        updated_is_active = (
            is_active
            if is_active is not None
            else current_permission.is_active
        )

        if updated_name != current_permission.name:
            existing_permission = (
                self._permission_repository.get_by_name(updated_name)
            )

            if existing_permission is not None:
                raise PermissionConflictError(
                    f"A permission with the name "
                    f"'{updated_name}' already exists."
                )

        permission = Permission(
            id=current_permission.id,
            name=updated_name,
            description=updated_description,
            is_active=updated_is_active,
            created_at=current_permission.created_at,
            updated_at=datetime.now(UTC),
        )

        return self._permission_repository.update(permission)