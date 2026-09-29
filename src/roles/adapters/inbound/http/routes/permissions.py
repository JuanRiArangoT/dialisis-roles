from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from roles.adapters.inbound.http.dependencies.database import get_db
from roles.adapters.inbound.http.schemas.create_permission import (
    CreatePermissionRequest,
)
from roles.adapters.inbound.http.schemas.update_permission import (
    UpdatePermissionRequest,
)
from roles.adapters.outbound.database.permission_repository import (
    PostgresPermissionRepository,
)
from roles.application.dtos.permission_output import PermissionOutputDTO
from roles.application.use_cases.create_permission import (
    CreatePermissionUseCase,
)
from roles.application.use_cases.delete_permission import (
    DeletePermissionUseCase,
)
from roles.application.use_cases.get_permission import (
    GetPermissionUseCase,
)
from roles.application.use_cases.list_permissions import (
    ListPermissionsUseCase,
)
from roles.application.use_cases.update_permission import (
    UpdatePermissionUseCase,
)

router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
)


@router.post(
    "",
    response_model=PermissionOutputDTO,
    status_code=status.HTTP_201_CREATED,
)
def create_permission(
    request: CreatePermissionRequest,
    db: Session = Depends(get_db),
) -> PermissionOutputDTO:
    repository = PostgresPermissionRepository(db)
    use_case = CreatePermissionUseCase(repository)

    permission = use_case.execute(
        name=request.name,
        description=request.description,
    )

    return PermissionOutputDTO(
        permission_id=permission.id,
        name=permission.name,
        description=permission.description,
        is_active=permission.is_active,
        created_at=permission.created_at,
        updated_at=permission.updated_at,
    )

@router.get(
    "/{permission_id}",
    response_model=PermissionOutputDTO,
)
def get_permission(
    permission_id: str,
    db: Session = Depends(get_db),
) -> PermissionOutputDTO:
    repository = PostgresPermissionRepository(db)
    use_case = GetPermissionUseCase(repository)

    permission = use_case.execute(permission_id)

    return PermissionOutputDTO(
        permission_id=permission.id,
        name=permission.name,
        description=permission.description,
        is_active=permission.is_active,
        created_at=permission.created_at,
        updated_at=permission.updated_at,
    )

@router.get(
    "",
    response_model=list[PermissionOutputDTO],
)
def list_permissions(
    db: Session = Depends(get_db),
) -> list[PermissionOutputDTO]:
    repository = PostgresPermissionRepository(db)
    use_case = ListPermissionsUseCase(repository)

    permissions = use_case.execute()

    return [
        PermissionOutputDTO(
            permission_id=permission.id,
            name=permission.name,
            description=permission.description,
            is_active=permission.is_active,
            created_at=permission.created_at,
            updated_at=permission.updated_at,
        )
        for permission in permissions
    ]

@router.put(
    "/{permission_id}",
    response_model=PermissionOutputDTO,
)
def update_permission(
    permission_id: str,
    request: UpdatePermissionRequest,
    db: Session = Depends(get_db),
) -> PermissionOutputDTO:
    repository = PostgresPermissionRepository(db)
    use_case = UpdatePermissionUseCase(repository)

    permission = use_case.execute(
        permission_id=permission_id,
        name=request.name,
        description=request.description,
        is_active=request.is_active,
    )

    return PermissionOutputDTO(
        permission_id=permission.id,
        name=permission.name,
        description=permission.description,
        is_active=permission.is_active,
        created_at=permission.created_at,
        updated_at=permission.updated_at,
    )

@router.delete(
    "/{permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_permission(
    permission_id: str,
    db: Session = Depends(get_db),
) -> None:
    repository = PostgresPermissionRepository(db)
    use_case = DeletePermissionUseCase(repository)
    use_case.execute(permission_id)