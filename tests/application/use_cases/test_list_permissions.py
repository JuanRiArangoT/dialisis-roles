from unittest.mock import Mock

from roles.application.use_cases.list_permissions import ListPermissionsUseCase


def test_list_permissions() -> None:
    repository = Mock()

    permission_1 = Mock()
    permission_1.id = "permission-1"
    permission_1.name = "users.read"

    permission_2 = Mock()
    permission_2.id = "permission-2"
    permission_2.name = "users.create"

    repository.get_all.return_value = [permission_1, permission_2]

    use_case = ListPermissionsUseCase(repository)

    result = use_case.execute()

    assert result == [permission_1, permission_2]
    assert len(result) == 2
    assert result[0].name == "users.read"
    assert result[1].name == "users.create"

    repository.get_all.assert_called_once_with()