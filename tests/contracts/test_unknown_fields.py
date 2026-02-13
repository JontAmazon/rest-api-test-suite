import uuid

from tests.data.todo_payloads import build_todo_payload
from tests.data.user_payloads import build_user_payload
from tests.utils.assertions import assert_status


def test_unknown_fields_ignored_on_users(users_client, auth_headers):
    payload = build_user_payload()
    payload["extra_field"] = f"extra-{uuid.uuid4().hex}"
    response = users_client.create_user(payload, headers=auth_headers)
    assert_status(response, 201)
    assert "extra_field" not in response.json()

    users_client.delete_user(response.json()["id"], headers=auth_headers)


def test_unknown_fields_ignored_on_user_todos(todos_client, created_user, auth_headers):
    payload = build_todo_payload(created_user["id"])
    payload["unexpected"] = "should-not-return"
    response = todos_client.create_todo(payload, headers=auth_headers)
    assert_status(response, 201)
    assert "unexpected" not in response.json()

    todos_client.delete_todo(response.json()["id"], headers=auth_headers)

