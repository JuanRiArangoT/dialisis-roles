from roles.application.dtos.role_output import RoleOutputDTO
from roles.domain.repositories.role_repository import RoleRepositoryPort


class ListRolesUseCase:
    def __init__(self, role_repository: RoleRepositoryPort) -> None:
        self._role_repository = role_repository

    def execute(self) -> list[RoleOutputDTO]:
        roles = self._role_repository.get_all()

        return [
            RoleOutputDTO(
                id=role.id,
                name=role.name,
                description=role.description,
                is_active=role.is_active,
                created_at=role.created_at,
                updated_at=role.updated_at,
            )
            for role in roles
        ]