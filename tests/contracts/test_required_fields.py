import pytest

from tests.payloads.post_payloads import build_post_payload
from tests.payloads.todo_payloads import build_todo_payload
from tests.payloads.user_payloads import build_user_payload
from tests.utils.assertions import assert_status

CREATE_USER_REQUIRED_FIELDS = ["name", "email", "gender", "status"]
CREATE_POST_REQUIRED_FIELDS = ["user_id", "title", "body"]
CREATE_TODO_REQUIRED_FIELDS = ["user_id", "title", "status"]


def _assert_field_error(response, field_name: str) -> None:
    errors = response.json()
    assert any(error.get("field") == field_name for error in errors)


# --- Required fields not missing; expecting 201 ---

def test_create_user_with_all_required_fields(users_client, auth_headers):
    payload = build_user_payload()
    for field_name in CREATE_USER_REQUIRED_FIELDS:
        assert payload.get(field_name) is not None
    response = users_client.create_user(payload, headers=auth_headers)
    assert_status(response, 201)
    users_client.delete_user(response.json()["id"], headers=auth_headers)


def test_create_post_with_all_required_fields(created_user, posts_client, auth_headers):
    payload = build_post_payload(created_user["id"])
    for field_name in CREATE_POST_REQUIRED_FIELDS:
        assert payload.get(field_name) is not None
    response = posts_client.create_post(payload, headers=auth_headers)
    assert_status(response, 201)
    posts_client.delete_post(response.json()["id"], headers=auth_headers)


def test_create_todo_with_all_required_fields(created_user, todos_client, auth_headers):
    payload = build_todo_payload(created_user["id"])
    for field_name in CREATE_TODO_REQUIRED_FIELDS:
        assert payload.get(field_name) is not None
    response = todos_client.create_todo(payload, headers=auth_headers)
    assert_status(response, 201)
    todos_client.delete_todo(response.json()["id"], headers=auth_headers)


# --- Required fields missing; expecting 422---

@pytest.mark.parametrize("field_name", CREATE_USER_REQUIRED_FIELDS)
def test_required_fields_users(users_client, auth_headers, field_name):
    payload = build_user_payload()
    payload.pop(field_name)
    response = users_client.create_user(payload, headers=auth_headers)
    assert_status(response, 422)
    _assert_field_error(response, field_name)


@pytest.mark.parametrize("field_name", CREATE_POST_REQUIRED_FIELDS)
def test_required_fields_posts(created_user, posts_client, auth_headers, field_name):
    payload = build_post_payload(created_user["id"])
    payload.pop(field_name)
    response = posts_client.create_post(payload, headers=auth_headers)
    assert_status(response, 422)
    _assert_field_error(response, field_name)


@pytest.mark.parametrize("field_name", CREATE_TODO_REQUIRED_FIELDS)
def test_required_fields_todos(created_user, todos_client, auth_headers, field_name):
    payload = build_todo_payload(created_user["id"])
    payload.pop(field_name)
    response = todos_client.create_todo(payload, headers=auth_headers)
    assert_status(response, 422)
    _assert_field_error(response, field_name)


