from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from roles.adapters.inbound.http.exceptions import (
    permission_conflict_exception_handler,
    permission_not_found_exception_handler,
    role_conflict_exception_handler,
    role_not_found_exception_handler,
    role_permission_conflict_exception_handler,
    role_permission_not_found_exception_handler,
)
from roles.adapters.inbound.http.routes.permissions import (
    router as permissions_router,
)
from roles.adapters.inbound.http.routes.role_permissions import (
    router as role_permissions_router,
)
from roles.adapters.inbound.http.routes.roles import router as roles_router
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

app = FastAPI(
    title="Servicio de Roles - Diálisis",
    description="Microservicio de roles y Arquitectura Hexagonal",
    version="1.0.0",
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(roles_router)
app.include_router(permissions_router)
app.include_router(role_permissions_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "roles-microservice"}


app.add_exception_handler(
    RoleConflictError,
    role_conflict_exception_handler,
)

app.add_exception_handler(
    RoleNotFoundApplicationError,
    role_not_found_exception_handler,
)

app.add_exception_handler(
    PermissionConflictError,
    permission_conflict_exception_handler,
)

app.add_exception_handler(
    PermissionNotFoundApplicationError,
    permission_not_found_exception_handler,
)

app.add_exception_handler(
    RolePermissionConflictError,
    role_permission_conflict_exception_handler,
)

app.add_exception_handler(
    RolePermissionNotFoundApplicationError,
    role_permission_not_found_exception_handler,
)