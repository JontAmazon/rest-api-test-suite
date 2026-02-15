from __future__ import annotations

import logging

import pytest

from tests.payloads.todo_payloads import build_todo_payload

logger = logging.getLogger(__name__)


@pytest.fixture
def created_todo(created_user, todos_client, auth_headers):
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
            logger.warning("Cleanup - deleting todo %s returned unexpected status %s", todo_id, response.status_code)
    except Exception:
        logger.exception("Cleanup - deleting todo %s failed", todo_id)

