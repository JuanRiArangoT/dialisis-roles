from collections.abc import Mapping
from datetime import datetime
from typing import ClassVar

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    Table,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column(
        "role_id",
        String(36),
        ForeignKey("roles.roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "permission_id",
        String(36),
        ForeignKey("roles.permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    schema="roles",
)


class RoleModel(Base):
    __tablename__ = "roles"
    __table_args__: ClassVar[Mapping[str, str]] = {"schema": "roles"}

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    permissions: Mapped[list["PermissionModel"]] = relationship(
        secondary=role_permissions,
        back_populates="roles",
        passive_deletes=True,
    )


class PermissionModel(Base):
    __tablename__ = "permissions"
    __table_args__: ClassVar[Mapping[str, str]] = {"schema": "roles"}

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    roles: Mapped[list["RoleModel"]] = relationship(
        secondary=role_permissions,
        back_populates="permissions",
        passive_deletes=True,
    )