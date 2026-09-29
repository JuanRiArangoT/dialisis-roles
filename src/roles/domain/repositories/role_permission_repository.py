from abc import ABC, abstractmethod


class RolePermissionRepositoryPort(ABC):
    @abstractmethod
    def assign_permission(
        self,
        role_id: str,
        permission_id: str,
    ) -> None:
        pass

    @abstractmethod
    def remove_permission(
        self,
        role_id: str,
        permission_id: str,
    ) -> None:
        pass

    @abstractmethod
    def get_permission_ids_by_role(
        self,
        role_id: str,
    ) -> list[str]:
        pass

    @abstractmethod
    def permission_exists_for_role(
        self,
        role_id: str,
        permission_id: str,
    ) -> bool:
        pass

    @abstractmethod
    def has_permission(
        self,
        role_id: str,
        permission_id: str,
    ) -> bool:
        pass