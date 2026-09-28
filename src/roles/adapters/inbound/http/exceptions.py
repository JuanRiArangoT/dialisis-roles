from fastapi import Request
from fastapi.responses import JSONResponse

from roles.application.exceptions.role_exceptions import (
    RoleConflictError,
    RoleNotFoundApplicationError,
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