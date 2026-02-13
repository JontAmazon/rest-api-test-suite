import uuid

import pytest

from tests.data.todo_payloads import build_todo_payload
from tests.data.user_payloads import build_user_payload
from tests.utils.assertions import assert_status


@pytest.mark.contract
def test_unknown_fields_ignored_on_users(users_client, auth_headers):
    payload = build_user_payload()
    payload["extra_field"] = f"extra-{uuid.uuid4().hex}"
    response = users_client.create_user(payload, headers=auth_headers)
    assert_status(response, 201)
    assert "extra_field" not in response.json()

    users_client.delete_user(response.json()["id"], headers=auth_headers)


@pytest.mark.contract
def test_unknown_fields_ignored_on_user_todos(users_client, auth_headers):
    user_response = users_client.create_user(build_user_payload(), headers=auth_headers)
    assert_status(user_response, 201)
    user = user_response.json()

    payload = build_todo_payload(user["id"])
    payload["unexpected"] = "should-not-return"
    response = users_client.create_todo_for_user(user["id"], payload, headers=auth_headers)
    assert_status(response, 201)
    assert "unexpected" not in response.json()

    users_client.delete_user(user["id"], headers=auth_headers)
