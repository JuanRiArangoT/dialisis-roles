from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from roles.adapters.inbound.http.exceptions import (
    role_conflict_exception_handler,
    role_not_found_exception_handler,
)
from roles.adapters.inbound.http.routes.roles import router as roles_router
from roles.application.exceptions.role_exceptions import (
    RoleConflictError,
    RoleNotFoundApplicationError,
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