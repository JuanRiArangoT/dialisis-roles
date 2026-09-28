from abc import ABC, abstractmethod

from roles.domain.entities.role import Role


class RoleRepositoryPort(ABC):

    @abstractmethod
    def create(self, role: Role) -> Role:
        """Create a role."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, role_id: str) -> Role | None:
        """Get a role by its identifier."""
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, name: str) -> Role | None:
        """Get a role by its name."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Role]:
        """Get all roles."""
        raise NotImplementedError

    @abstractmethod
    def update(self, role: Role) -> Role:
        """Update a role."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, role_id: str) -> None:
        """Delete a role."""
        raise NotImplementedError