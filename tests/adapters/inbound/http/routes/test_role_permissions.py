from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_assign_permission_to_role() -> None:
    with (
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresRoleRepository"
        ) as role_repository,
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresPermissionRepository"
        ) as permission_repository,
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresRolePermissionRepository"
        ) as role_permission_repository,
    ):
        role_repository.return_value.get_by_id.return_value = MagicMock()
        permission_repository.return_value.get_by_id.return_value = MagicMock()
        role_permission_repository.return_value.permission_exists_for_role.return_value = False

        response = client.post(
            "/roles/role-1/permissions/permission-1"
        )

    assert response.status_code == 204

def test_assign_permission_to_role_conflict() -> None:
    with (
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresRoleRepository"
        ) as role_repository,
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresPermissionRepository"
        ) as permission_repository,
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresRolePermissionRepository"
        ) as role_permission_repository,
    ):
        role_repository.return_value.get_by_id.return_value = MagicMock()
        permission_repository.return_value.get_by_id.return_value = MagicMock()
        role_permission_repository.return_value.permission_exists_for_role.return_value = True

        response = client.post(
            "/roles/role-1/permissions/permission-1"
        )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Permission is already assigned to this role."
    }

def test_assign_permission_to_role_not_found() -> None:
    with patch(
        "roles.adapters.inbound.http.routes.role_permissions.PostgresRoleRepository"
    ) as role_repository:
        role_repository.return_value.get_by_id.return_value = None

        response = client.post(
            "/roles/role-1/permissions/permission-1"
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Role not found: role-1"
    }

def test_remove_permission_from_role() -> None:
    with (
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresRoleRepository"
        ) as role_repository,
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresRolePermissionRepository"
        ) as role_permission_repository,
    ):
        role_repository.return_value.get_by_id.return_value = MagicMock()
        role_permission_repository.return_value.permission_exists_for_role.return_value = True

        response = client.delete(
            "/roles/role-1/permissions/permission-1"
        )

    assert response.status_code == 204

def test_remove_permission_from_role_not_found() -> None:
    with (
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresRoleRepository"
        ) as role_repository,
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresRolePermissionRepository"
        ) as role_permission_repository,
    ):
        role_repository.return_value.get_by_id.return_value = MagicMock()
        role_permission_repository.return_value.permission_exists_for_role.return_value = False

        response = client.delete(
            "/roles/role-1/permissions/permission-1"
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Permission is not assigned to this role."
    }

def test_list_role_permissions() -> None:
    permission = MagicMock()
    permission.id = "permission-1"
    permission.name = "users.read"
    permission.description = "Permite consultar usuarios"
    permission.is_active = True

    with (
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresRoleRepository"
        ) as role_repository,
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresPermissionRepository"
        ) as permission_repository,
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresRolePermissionRepository"
        ) as role_permission_repository,
    ):
        role_repository.return_value.get_by_id.return_value = MagicMock()
        role_permission_repository.return_value.get_permission_ids_by_role.return_value = [
            "permission-1"
        ]
        permission_repository.return_value.get_by_id.return_value = permission

        response = client.get(
            "/roles/role-1/permissions"
        )

    assert response.status_code == 200
    assert response.json() == [
        {
            "permission_id": "permission-1",
            "name": "users.read",
            "description": "Permite consultar usuarios",
            "is_active": True,
        }
    ]

def test_list_role_permissions_not_found() -> None:
    with patch(
        "roles.adapters.inbound.http.routes.role_permissions.PostgresRoleRepository"
    ) as role_repository:
        role_repository.return_value.get_by_id.return_value = None

        response = client.get(
            "/roles/role-1/permissions"
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Role not found: role-1"
    }

def test_check_role_permission_returns_true() -> None:
    with (
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresRoleRepository"
        ) as role_repository,
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresPermissionRepository"
        ) as permission_repository,
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresRolePermissionRepository"
        ) as role_permission_repository,
    ):
        role_repository.return_value.get_by_id.return_value = MagicMock()

        permission = MagicMock()
        permission.id = "permission-1"

        permission_repository.return_value.get_by_name.return_value = permission
        role_permission_repository.return_value.has_permission.return_value = True

        response = client.get(
            "/roles/role-1/permissions/users.read"
        )

    assert response.status_code == 200
    assert response.json() == {
        "has_permission": True
    }


def test_check_role_permission_returns_false() -> None:
    with (
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresRoleRepository"
        ) as role_repository,
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresPermissionRepository"
        ) as permission_repository,
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresRolePermissionRepository"
        ) as role_permission_repository,
    ):
        role_repository.return_value.get_by_id.return_value = MagicMock()

        permission = MagicMock()
        permission.id = "permission-1"

        permission_repository.return_value.get_by_name.return_value = permission
        role_permission_repository.return_value.has_permission.return_value = False

        response = client.get(
            "/roles/role-1/permissions/users.read"
        )

    assert response.status_code == 200
    assert response.json() == {
        "has_permission": False
    }


def test_check_role_permission_role_not_found() -> None:
    with patch(
        "roles.adapters.inbound.http.routes.role_permissions.PostgresRoleRepository"
    ) as role_repository:
        role_repository.return_value.get_by_id.return_value = None

        response = client.get(
            "/roles/role-1/permissions/users.read"
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Role not found: role-1"
    }


def test_check_role_permission_permission_not_found() -> None:
    with (
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresRoleRepository"
        ) as role_repository,
        patch(
            "roles.adapters.inbound.http.routes.role_permissions.PostgresPermissionRepository"
        ) as permission_repository,
    ):
        role_repository.return_value.get_by_id.return_value = MagicMock()
        permission_repository.return_value.get_by_name.return_value = None

        response = client.get(
            "/roles/role-1/permissions/users.read"
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Permission not found: users.read"
    }