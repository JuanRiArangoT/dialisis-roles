from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from roles.application.exceptions.role_exceptions import RoleConflictError
from roles.domain.entities.role import Role
from roles.domain.repositories.role_repository import RoleRepositoryPort

from .models import RoleModel


class PostgresRoleRepository(RoleRepositoryPort):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, role: Role) -> Role:
        model = RoleModel(
            id=role.id,
            name=role.name,
            description=role.description,
            is_active=role.is_active,
            created_at=role.created_at,
            updated_at=role.updated_at,
        )

        try:
            self._session.add(model)
            self._session.commit()
            self._session.refresh(model)

        except IntegrityError as exc:
            self._session.rollback()

            if getattr(exc.orig, "sqlstate", None) == "23505":
                raise RoleConflictError(
                    f"A role with the name '{role.name}' already exists."
                ) from exc

            raise

        return self._to_entity(model)

    def get_by_id(self, role_id: str) -> Role | None:
        model = self._session.get(RoleModel, role_id)

        if model is None:
            return None

        return self._to_entity(model)

    def get_by_name(self, name: str) -> Role | None:
        statement = select(RoleModel).where(RoleModel.name == name)

        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_entity(model)

    def get_all(self) -> list[Role]:
        statement = select(RoleModel).order_by(RoleModel.name)

        models = self._session.scalars(statement).all()

        return [self._to_entity(model) for model in models]

    def update(self, role: Role) -> Role:
        model = self._session.get(RoleModel, role.id)

        if model is None:
            raise ValueError(f"Role not found: {role.id}")

        model.name = role.name
        model.description = role.description
        model.is_active = role.is_active
        model.updated_at = role.updated_at

        try:
            self._session.commit()
            self._session.refresh(model)

        except IntegrityError as exc:
            self._session.rollback()

            if getattr(exc.orig, "sqlstate", None) == "23505":
                raise RoleConflictError(
                    f"A role with the name '{role.name}' already exists."
                ) from exc

            raise

        return self._to_entity(model)

    def delete(self, role_id: str) -> None:
        model = self._session.get(RoleModel, role_id)

        if model is None:
            return

        self._session.delete(model)
        self._session.commit()

    @staticmethod
    def _to_entity(model: RoleModel) -> Role:
        return Role(
            id=model.id,
            name=model.name,
            description=model.description,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )