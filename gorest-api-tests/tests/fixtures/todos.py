from __future__ import annotations

import pytest

from tests.data.todo_payloads import build_todo_payload


@pytest.fixture
def created_todo(todos_client, auth_headers, created_user):
    payload = build_todo_payload(created_user["id"])
    response = todos_client.create_todo(payload, headers=auth_headers)
    assert response.status_code == 201, response.text
    todo = response.json()
    yield todo
    todos_client.delete_todo(todo["id"], headers=auth_headers)
