from roles.application.exceptions.role_exceptions import (
    RoleNotFoundApplicationError,
)
from roles.domain.repositories.role_repository import RoleRepositoryPort


class DeleteRoleUseCase:
    def __init__(self, role_repository: RoleRepositoryPort) -> None:
        self._role_repository = role_repository

    def execute(self, role_id: str) -> None:
        role = self._role_repository.get_by_id(role_id)

        if role is None:
            raise RoleNotFoundApplicationError(
                f"Role not found: {role_id}"
            )

        self._role_repository.delete(role_id)