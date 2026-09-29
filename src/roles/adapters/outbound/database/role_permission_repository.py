from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from roles.application.exceptions.role_permission_exceptions import (
    RolePermissionConflictError,
)
from roles.domain.repositories.role_permission_repository import (
    RolePermissionRepositoryPort,
)

from .models import role_permissions


class PostgresRolePermissionRepository(RolePermissionRepositoryPort):
    def __init__(self, session: Session) -> None:
        self._session = session

    def assign_permission(
        self,
        role_id: str,
        permission_id: str,
    ) -> None:
        try:
            self._session.execute(
                role_permissions.insert().values(
                    role_id=role_id,
                    permission_id=permission_id,
                )
            )
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()

            if getattr(exc.orig, "sqlstate", None) == "23505":
                raise RolePermissionConflictError(
                    "Permission is already assigned to this role."
                ) from exc

            raise

    def remove_permission(
        self,
        role_id: str,
        permission_id: str,
    ) -> None:
        self._session.execute(
            role_permissions.delete().where(
                role_permissions.c.role_id == role_id,
                role_permissions.c.permission_id == permission_id,
            )
        )
        self._session.commit()

    def get_permission_ids_by_role(
        self,
        role_id: str,
    ) -> list[str]:
        statement = select(role_permissions.c.permission_id).where(
            role_permissions.c.role_id == role_id
        )

        return list(self._session.scalars(statement).all())

    def permission_exists_for_role(
        self,
        role_id: str,
        permission_id: str,
    ) -> bool:
        statement = select(role_permissions.c.permission_id).where(
            role_permissions.c.role_id == role_id,
            role_permissions.c.permission_id == permission_id,
        )

        return self._session.scalar(statement) is not None

    def has_permission(
        self,
        role_id: str,
        permission_id: str,
    ) -> bool:
        statement = select(role_permissions.c.permission_id).where(
            role_permissions.c.role_id == role_id,
            role_permissions.c.permission_id == permission_id,
        )

        return self._session.scalar(statement) is not None