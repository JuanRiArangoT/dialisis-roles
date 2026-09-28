from datetime import UTC, datetime

from roles.application.dtos.role_output import RoleOutputDTO
from roles.application.exceptions.role_exceptions import (
    RoleConflictError,
    RoleNotFoundApplicationError,
)
from roles.domain.repositories.role_repository import RoleRepositoryPort


class UpdateRoleUseCase:
    def __init__(self, role_repository: RoleRepositoryPort) -> None:
        self._role_repository = role_repository

    def execute(
        self,
        role_id: str,
        name: str,
        description: str | None = None,
        is_active: bool = True,
    ) -> RoleOutputDTO:
        role = self._role_repository.get_by_id(role_id)

        if role is None:
            raise RoleNotFoundApplicationError(
                f"Role not found: {role_id}"
            )

        existing_role = self._role_repository.get_by_name(name)

        if existing_role is not None and existing_role.id != role_id:
            raise RoleConflictError(
                f"Role already exists: {name}"
            )

        role.name = name
        role.description = description
        role.is_active = is_active
        role.updated_at = datetime.now(UTC)

        updated_role = self._role_repository.update(role)

        return RoleOutputDTO(
            id=updated_role.id,
            name=updated_role.name,
            description=updated_role.description,
            is_active=updated_role.is_active,
            created_at=updated_role.created_at,
            updated_at=updated_role.updated_at,
        )