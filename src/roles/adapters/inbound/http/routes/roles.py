from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from roles.adapters.inbound.http.dependencies.database import get_db
from roles.adapters.inbound.http.schemas.create_role import CreateRoleRequest
from roles.adapters.inbound.http.schemas.update_role import UpdateRoleRequest
from roles.adapters.outbound.database.role_repository import (
    PostgresRoleRepository,
)
from roles.application.use_cases.create_role import CreateRoleUseCase
from roles.application.use_cases.delete_role import DeleteRoleUseCase
from roles.application.use_cases.get_role import GetRoleUseCase
from roles.application.use_cases.list_roles import ListRolesUseCase
from roles.application.use_cases.update_role import UpdateRoleUseCase

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)


@router.get("")
def list_roles(
    db: Session = Depends(get_db),
):
    repository = PostgresRoleRepository(db)
    use_case = ListRolesUseCase(repository)

    return use_case.execute()

@router.get("/{role_id}")
def get_role(
    role_id: str,
    db: Session = Depends(get_db),
):
    repository = PostgresRoleRepository(db)
    use_case = GetRoleUseCase(repository)

    return use_case.execute(role_id)

@router.post("", status_code=status.HTTP_201_CREATED)
def create_role(
    request: CreateRoleRequest,
    db: Session = Depends(get_db),
):
    repository = PostgresRoleRepository(db)
    use_case = CreateRoleUseCase(repository)

    return use_case.execute(
        name=request.name,
        description=request.description,
    )

@router.put("/{role_id}")
def update_role(
    role_id: str,
    request: UpdateRoleRequest,
    db: Session = Depends(get_db),
):
    repository = PostgresRoleRepository(db)
    use_case = UpdateRoleUseCase(repository)

    return use_case.execute(
        role_id=role_id,
        name=request.name,
        description=request.description,
        is_active=request.is_active,
    )

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: str,
    db: Session = Depends(get_db),
):
    repository = PostgresRoleRepository(db)
    use_case = DeleteRoleUseCase(repository)

    use_case.execute(role_id)