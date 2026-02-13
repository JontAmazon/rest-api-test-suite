from __future__ import annotations

import warnings

import pytest

from tests.data.todo_payloads import build_todo_payload


@pytest.fixture
def created_todo(todos_client, auth_headers, created_user):
    payload = build_todo_payload(created_user["id"])
    response = todos_client.create_todo(payload, headers=auth_headers)
    assert response.status_code == 201, response.text
    todo = response.json()
    yield todo
    delete_todo_ignore_errors(todos_client, todo["id"], headers=auth_headers)


def delete_todo_ignore_errors(todos_client, todo_id: int, headers: dict[str, str]) -> None:
    try:
        response = todos_client.delete_todo(todo_id, headers=headers)
        if response.status_code != 204:
            warnings.warn(f"Cleanup - deleting todo {todo_id} returned unexpected status {response.status_code}", stacklevel=2)
    except Exception as exc:
        warnings.warn(f"Cleanup - deleting todo {todo_id} failed: {exc}", stacklevel=2)
