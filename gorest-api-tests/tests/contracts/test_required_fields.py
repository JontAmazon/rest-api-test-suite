import pytest

from tests.data.post_payloads import build_post_payload
from tests.data.todo_payloads import build_todo_payload
from tests.data.user_payloads import build_user_payload
from tests.utils.assertions import assert_status


def _assert_field_error(response, field_name: str) -> None:
    errors = response.json()
    assert any(error.get("field") == field_name for error in errors)


@pytest.mark.contract
@pytest.mark.parametrize("field_name", ["name", "email", "gender", "status"])
def test_required_fields_users(users_client, auth_headers, field_name):
    payload = build_user_payload()
    payload.pop(field_name)
    response = users_client.create_user(payload, headers=auth_headers)
    assert_status(response, 422)
    _assert_field_error(response, field_name)


@pytest.mark.contract
@pytest.mark.parametrize("field_name", ["user_id", "title", "body"])
def test_required_fields_posts(posts_client, users_client, auth_headers, field_name):
    user_response = users_client.create_user(build_user_payload(), headers=auth_headers)
    assert_status(user_response, 201)
    user = user_response.json()

    payload = build_post_payload(user["id"])
    payload.pop(field_name)
    response = posts_client.create_post(payload, headers=auth_headers)
    assert_status(response, 422)
    _assert_field_error(response, field_name)

    users_client.delete_user(user["id"], headers=auth_headers)


@pytest.mark.contract
@pytest.mark.parametrize("field_name", ["user_id", "title", "status", "due_on"])
def test_required_fields_todos(todos_client, users_client, auth_headers, field_name):
    user_response = users_client.create_user(build_user_payload(), headers=auth_headers)
    assert_status(user_response, 201)
    user = user_response.json()

    payload = build_todo_payload(user["id"])
    payload.pop(field_name)
    response = todos_client.create_todo(payload, headers=auth_headers)
    assert_status(response, 422)
    _assert_field_error(response, field_name)

    users_client.delete_user(user["id"], headers=auth_headers)
