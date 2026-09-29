from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from roles.adapters.inbound.http.dependencies.database import get_db
from roles.adapters.outbound.database.permission_repository import (
    PostgresPermissionRepository,
)
from roles.adapters.outbound.database.role_permission_repository import (
    PostgresRolePermissionRepository,
)
from roles.adapters.outbound.database.role_repository import (
    PostgresRoleRepository,
)
from roles.application.use_cases.assign_permission_to_role import (
    AssignPermissionToRoleUseCase,
)
from roles.application.use_cases.check_role_permission import (
    CheckRolePermissionUseCase,
)
from roles.application.use_cases.list_role_permissions import (
    ListRolePermissionsUseCase,
)
from roles.application.use_cases.remove_permission_from_role import (
    RemovePermissionFromRoleUseCase,
)

router = APIRouter(
    prefix="/roles",
    tags=["Role Permissions"],
)


@router.post(
    "/{role_id}/permissions/{permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def assign_permission_to_role(
    role_id: str,
    permission_id: str,
    db: Session = Depends(get_db),
) -> None:
    role_repository = PostgresRoleRepository(db)
    permission_repository = PostgresPermissionRepository(db)
    role_permission_repository = PostgresRolePermissionRepository(db)

    use_case = AssignPermissionToRoleUseCase(
        role_repository=role_repository,
        permission_repository=permission_repository,
        role_permission_repository=role_permission_repository,
    )

    use_case.execute(
        role_id=role_id,
        permission_id=permission_id,
    )

@router.delete(
    "/{role_id}/permissions/{permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_permission_from_role(
    role_id: str,
    permission_id: str,
    db: Session = Depends(get_db),
) -> None:
    role_repository = PostgresRoleRepository(db)
    role_permission_repository = PostgresRolePermissionRepository(db)

    use_case = RemovePermissionFromRoleUseCase(
        role_repository=role_repository,
        role_permission_repository=role_permission_repository,
    )

    use_case.execute(
        role_id=role_id,
        permission_id=permission_id,
    )

@router.get(
    "/{role_id}/permissions",
)
def list_role_permissions(
    role_id: str,
    db: Session = Depends(get_db),
):
    role_repository = PostgresRoleRepository(db)
    permission_repository = PostgresPermissionRepository(db)
    role_permission_repository = PostgresRolePermissionRepository(db)

    use_case = ListRolePermissionsUseCase(
        role_repository=role_repository,
        permission_repository=permission_repository,
        role_permission_repository=role_permission_repository,
    )

    permissions = use_case.execute(role_id)

    return [
        {
            "permission_id": permission.id,
            "name": permission.name,
            "description": permission.description,
            "is_active": permission.is_active,
        }
        for permission in permissions
    ]

@router.get(
    "/{role_id}/permissions/{permission_name}",
)
def check_role_permission(
    role_id: str,
    permission_name: str,
    db: Session = Depends(get_db),
):
    role_repository = PostgresRoleRepository(db)
    permission_repository = PostgresPermissionRepository(db)
    role_permission_repository = PostgresRolePermissionRepository(db)

    use_case = CheckRolePermissionUseCase(
        role_repository=role_repository,
        permission_repository=permission_repository,
        role_permission_repository=role_permission_repository,
    )

    has_permission = use_case.execute(
        role_id=role_id,
        permission_name=permission_name,
    )

    return {
        "has_permission": has_permission,
    }