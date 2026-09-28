from roles.application.dtos.role_output import RoleOutputDTO
from roles.application.exceptions.role_exceptions import (
    RoleNotFoundApplicationError,
)
from roles.domain.repositories.role_repository import RoleRepositoryPort


class GetRoleUseCase:
    def __init__(self, role_repository: RoleRepositoryPort) -> None:
        self._role_repository = role_repository

    def execute(self, role_id: str) -> RoleOutputDTO:
        role = self._role_repository.get_by_id(role_id)

        if role is None:
            raise RoleNotFoundApplicationError(
                f"Role not found: {role_id}"
            )

        return RoleOutputDTO(
            id=role.id,
            name=role.name,
            description=role.description,
            is_active=role.is_active,
            created_at=role.created_at,
            updated_at=role.updated_at,
        )