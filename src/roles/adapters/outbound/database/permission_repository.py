from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from roles.application.exceptions.permission_exceptions import (
    PermissionConflictError,
)
from roles.domain.entities.permission import Permission
from roles.domain.repositories.permission_repository import (
    PermissionRepositoryPort,
)

from .models import PermissionModel


class PostgresPermissionRepository(PermissionRepositoryPort):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, permission: Permission) -> Permission:
        model = PermissionModel(
            id=permission.id,
            name=permission.name,
            description=permission.description,
            is_active=permission.is_active,
            created_at=permission.created_at,
            updated_at=permission.updated_at,
        )

        try:
            self._session.add(model)
            self._session.commit()
            self._session.refresh(model)

        except IntegrityError as exc:
            self._session.rollback()

            if getattr(exc.orig, "sqlstate", None) == "23505":
                raise PermissionConflictError(
                    f"A permission with the name "
                    f"'{permission.name}' already exists."
                ) from exc

            raise

        return self._to_entity(model)

    def get_by_id(self, permission_id: str) -> Permission | None:
        model = self._session.get(PermissionModel, permission_id)

        if model is None:
            return None

        return self._to_entity(model)

    def get_by_name(self, name: str) -> Permission | None:
        statement = select(PermissionModel).where(
            PermissionModel.name == name
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_entity(model)

    def get_all(self) -> list[Permission]:
        statement = select(PermissionModel).order_by(PermissionModel.name)

        models = self._session.scalars(statement).all()

        return [self._to_entity(model) for model in models]

    def update(self, permission: Permission) -> Permission:
        model = self._session.get(PermissionModel, permission.id)

        if model is None:
            raise ValueError(
                f"Permission not found: {permission.id}"
            )

        model.name = permission.name
        model.description = permission.description
        model.is_active = permission.is_active
        model.updated_at = permission.updated_at

        try:
            self._session.commit()
            self._session.refresh(model)

        except IntegrityError as exc:
            self._session.rollback()

            if getattr(exc.orig, "sqlstate", None) == "23505":
                raise PermissionConflictError(
                    f"A permission with the name "
                    f"'{permission.name}' already exists."
                ) from exc

            raise

        return self._to_entity(model)

    def delete(self, permission_id: str) -> None:
        model = self._session.get(PermissionModel, permission_id)

        if model is None:
            return

        self._session.delete(model)
        self._session.commit()

    @staticmethod
    def _to_entity(model: PermissionModel) -> Permission:
        return Permission(
            id=model.id,
            name=model.name,
            description=model.description,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )