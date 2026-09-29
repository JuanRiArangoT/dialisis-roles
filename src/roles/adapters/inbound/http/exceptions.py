from fastapi import Request, status
from fastapi.responses import JSONResponse

from roles.application.exceptions.permission_exceptions import (
    PermissionConflictError,
    PermissionNotFoundApplicationError,
)
from roles.application.exceptions.role_exceptions import (
    RoleConflictError,
    RoleNotFoundApplicationError,
)
from roles.application.exceptions.role_permission_exceptions import (
    RolePermissionConflictError,
    RolePermissionNotFoundApplicationError,
)


def role_not_found_exception_handler(
    request: Request,
    exc: RoleNotFoundApplicationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


def role_conflict_exception_handler(
    request: Request,
    exc: RoleConflictError,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )

def permission_conflict_exception_handler(
    request: Request,
    exc: PermissionConflictError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


def permission_not_found_exception_handler(
    request: Request,
    exc: PermissionNotFoundApplicationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )

def role_permission_conflict_exception_handler(
    request: Request,
    exc: RolePermissionConflictError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


def role_permission_not_found_exception_handler(
    request: Request,
    exc: RolePermissionNotFoundApplicationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )