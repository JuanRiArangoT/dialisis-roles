from abc import ABC, abstractmethod

from roles.domain.entities.permission import Permission


class PermissionRepositoryPort(ABC):
    @abstractmethod
    def create(self, permission: Permission) -> Permission:
        pass

    @abstractmethod
    def get_by_id(self, permission_id: str) -> Permission | None:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Permission | None:
        pass

    @abstractmethod
    def get_all(self) -> list[Permission]:
        pass

    @abstractmethod
    def update(self, permission: Permission) -> Permission:
        pass

    @abstractmethod
    def delete(self, permission_id: str) -> None:
        pass