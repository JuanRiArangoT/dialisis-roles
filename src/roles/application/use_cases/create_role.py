from datetime import UTC, datetime
from uuid import uuid4

from roles.application.dtos.role_output import RoleOutputDTO
from roles.application.exceptions.role_exceptions import RoleConflictError
from roles.domain.entities.role import Role
from roles.domain.repositories.role_repository import RoleRepositoryPort


class CreateRoleUseCase:
    def __init__(self, role_repository: RoleRepositoryPort) -> None:
        self._role_repository = role_repository

    def execute(
        self,
        name: str,
        description: str | None = None,
    ) -> RoleOutputDTO:
        existing_role = self._role_repository.get_by_name(name)

        if existing_role is not None:
            raise RoleConflictError(
                f"Role already exists: {name}"
            )

        now = datetime.now(UTC)

        role = Role(
            id=str(uuid4()),
            name=name,
            description=description,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        created_role = self._role_repository.create(role)

        return RoleOutputDTO(
            id=created_role.id,
            name=created_role.name,
            description=created_role.description,
            is_active=created_role.is_active,
            created_at=created_role.created_at,
            updated_at=created_role.updated_at,
        )