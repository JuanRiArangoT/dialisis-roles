# Diálisis Roles

Microservicio de gestión de roles para la plataforma Diálisis, desarrollado con Python y FastAPI bajo los principios de Arquitectura Hexagonal.

El servicio permite crear, consultar, actualizar y eliminar roles que posteriormente pueden ser asociados a los usuarios gestionados por `dialisis-users`.

## Tecnologías

- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL 16
- Alembic
- Pytest
- Ruff
- Docker
- Docker Compose
- uv

## Arquitectura

El proyecto implementa Arquitectura Hexagonal (Ports and Adapters), separando el dominio, la lógica de aplicación, los adaptadores de entrada/salida y la infraestructura.

```text
src/
└── roles/
    ├── adapters/
    │   ├── inbound/
    │   │   └── http/
    │   │       ├── exceptions/
    │   │       ├── routes/
    │   │       └── schemas/
    │   └── outbound/
    │       └── database/
    ├── application/
    │   ├── dtos/
    │   ├── exceptions/
    │   ├── ports/
    │   └── use_cases/
    ├── domain/
    │   ├── entities/
    │   └── exceptions/
    ├── infrastructure/
    │   └── config/
    └── main.py

migrations/
├── versions/
└── env.py

tests/
```

### Responsabilidades

| Capa | Responsabilidad |
|---|---|
| Domain | Entidades y reglas propias del dominio de roles. |
| Application | Casos de uso, DTOs, puertos y excepciones. |
| Adapters Inbound | Exposición de la API HTTP mediante FastAPI. |
| Adapters Outbound | Persistencia de roles en PostgreSQL. |
| Infrastructure | Configuración y componentes técnicos. |

## Integración con otros microservicios

`dialisis-roles` es utilizado por `dialisis-users` para validar los roles asociados a los usuarios.

La comunicación entre ambos servicios se realiza mediante HTTP.

```text
┌──────────────────────┐
│   dialisis-users     │
│                      │
│ Gestión de usuarios  │
└──────────┬───────────┘
           │
           │ HTTP
           │ GET /roles/{role_id}
           ▼
┌──────────────────────┐
│   dialisis-roles     │
│                      │
│ Gestión de roles     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│     PostgreSQL       │
│                      │
│  schema: roles       │
└──────────────────────┘
```

Cuando `dialisis-users` recibe un `role_id`, consulta este microservicio para comprobar que el rol exista.

## Requisitos

Para ejecutar el proyecto se requiere:

- Python 3.13 o superior.
- uv.
- Docker y Docker Compose.
- PostgreSQL 16.

## Configuración

Crear un archivo `.env` en la raíz del proyecto.

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@dialisis-users-db:5432/dialisis

POSTGRES_PASSWORD=postgres

AUTH0_DOMAIN=<auth0-domain>
AUTH0_CLIENT_ID=<auth0-client-id>
AUTH0_CLIENT_SECRET=<auth0-client-secret>
AUTH0_AUDIENCE=<auth0-audience>
AUTH0_DB_CONNECTION=Username-Password-Authentication
AUTH0_API_AUDIENCE=<auth0-api-audience>
```

### Variables de entorno

| Variable | Descripción |
|---|---|
| DATABASE_URL | Cadena de conexión a PostgreSQL. |
| POSTGRES_PASSWORD | Contraseña utilizada para PostgreSQL. |
| AUTH0_DOMAIN | Dominio del tenant de Auth0. |
| AUTH0_CLIENT_ID | Identificador de la aplicación de Auth0. |
| AUTH0_CLIENT_SECRET | Secreto de Auth0. |
| AUTH0_AUDIENCE | Audiencia configurada para Auth0. |
| AUTH0_DB_CONNECTION | Conexión de base de datos de Auth0. |
| AUTH0_API_AUDIENCE | Audiencia de la API. |

Las variables relacionadas con Auth0 se mantienen preparadas para la configuración común de la plataforma Diálisis.

**Importante:** No subir archivos `.env`, credenciales, secretos ni tokens al repositorio.

## Ejecución con Docker

El microservicio utiliza la misma red Docker de la plataforma Diálisis:

```text
dialisis-network
```

Además, utiliza la base de datos PostgreSQL compartida por los microservicios.

### Construir la imagen

```powershell
docker compose build
```

### Iniciar el servicio

```powershell
docker compose up -d
```

### Verificar el contenedor

```powershell
docker compose ps
```

### Consultar los logs

```powershell
docker compose logs -f roles
```

### Detener el servicio

```powershell
docker compose down
```

### URLs

| Componente | Dirección |
|---|---|
| Roles API | http://localhost:8002 |
| Swagger UI | http://localhost:8002/docs |
| ReDoc | http://localhost:8002/redoc |
| PostgreSQL | localhost:5432 |

Dentro del contenedor, FastAPI escucha en:

```text
0.0.0.0:8000
```

El puerto `8000` del contenedor se publica como `8002` en el equipo local.

## Base de datos

El servicio utiliza PostgreSQL y administra sus propias tablas dentro del esquema:

```text
roles
```

La estructura lógica es:

```text
dialisis
└── roles
    ├── roles
    └── alembic_version
```

El microservicio administra exclusivamente los objetos pertenecientes al esquema `roles`.

## Migraciones

Las migraciones de base de datos se administran mediante Alembic.

### Aplicar migraciones

```powershell
docker compose exec roles uv run alembic upgrade head
```

### Consultar la revisión actual

```powershell
docker compose exec roles uv run alembic current
```

### Crear una nueva migración

```powershell
docker compose exec roles uv run alembic revision --autogenerate -m "description"
```

Las migraciones generadas automáticamente deben revisarse antes de aplicarse.

## API

La API está construida con FastAPI.

### Health Check

```http
GET /health
```

Respuesta:

```json
{
  "status": "ok",
  "service": "roles-microservice"
}
```

### Crear rol

```http
POST /roles
Content-Type: application/json
```

Ejemplo:

```json
{
  "name": "Administrador",
  "description": "Rol administrador del sistema"
}
```

Respuesta exitosa:

```json
{
  "id": "uuid",
  "name": "Administrador",
  "description": "Rol administrador del sistema",
  "is_active": true,
  "created_at": "2026-09-28T06:01:35.284772Z",
  "updated_at": "2026-09-28T06:01:35.284772Z"
}
```

### Obtener todos los roles

```http
GET /roles
```

Obtiene la lista de roles registrados.

### Obtener un rol

```http
GET /roles/{role_id}
```

Obtiene un rol utilizando su identificador.

Este endpoint es utilizado por `dialisis-users` para validar la existencia de un rol antes de asociarlo a un usuario.

Si el rol no existe, responde:

```text
404 Not Found
```

### Actualizar un rol

```http
PUT /roles/{role_id}
Content-Type: application/json
```

Permite actualizar la información de un rol existente.

### Eliminar un rol

```http
DELETE /roles/{role_id}
```

Permite eliminar un rol existente según las reglas definidas por el servicio.

## Respuestas HTTP

| Código | Descripción |
|---|---|
| 200 | Operación procesada correctamente. |
| 201 | Rol creado correctamente. |
| 404 | Rol no encontrado. |
| 409 | Conflicto con el rol. |
| 500 | Error interno del servidor. |

## Ejecución local sin Docker

Instalar las dependencias:

```powershell
uv sync
```

Configurar las variables de entorno correspondientes al entorno local.

Aplicar las migraciones:

```powershell
uv run alembic upgrade head
```

Ejecutar FastAPI:

```powershell
uv run uvicorn src.main:app --reload
```

La API estará disponible en:

```text
http://localhost:8000
```

## Pruebas

El proyecto utiliza Pytest para validar el comportamiento del microservicio.

Ejecutar todos los tests:

```powershell
uv run pytest
```

## Calidad de código

El proyecto utiliza Ruff.

Ejecutar el análisis:

```powershell
uv run ruff check .
```

Corregir automáticamente los problemas compatibles:

```powershell
uv run ruff check . --fix
```

## Documentación de la API

FastAPI genera automáticamente la documentación OpenAPI.

Con Docker:

```text
Swagger UI: http://localhost:8002/docs
ReDoc:      http://localhost:8002/redoc
OpenAPI:    http://localhost:8002/openapi.json
```

En ejecución local:

```text
Swagger UI: http://localhost:8000/docs
ReDoc:      http://localhost:8000/redoc
OpenAPI:    http://localhost:8000/openapi.json
```

## Estado del proyecto

Actualmente el microservicio cuenta con:

- CRUD de roles.
- Persistencia mediante PostgreSQL.
- Esquema independiente `roles`.
- Migraciones mediante Alembic.
- Arquitectura Hexagonal.
- API REST con FastAPI.
- Integración con `dialisis-users`.
- Endpoint de validación de existencia de roles.
- Tests automatizados con Pytest.
- Linter con Ruff.
- Contenerización mediante Docker.
- Orquestación mediante Docker Compose.