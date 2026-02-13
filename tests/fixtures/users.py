from __future__ import annotations

import pytest

from schedule import logger

from tests.data.user_payloads import build_user_payload


@pytest.fixture
def created_user(users_client, auth_headers):
    payload = build_user_payload()
    response = users_client.create_user(payload, headers=auth_headers)
    assert response.status_code == 201, response.text
    user = response.json()
    yield user
    delete_user_ignore_errors(users_client, user["id"], headers=auth_headers)


def delete_user_ignore_errors(users_client, user_id: int, headers: dict[str, str]) -> None:
    try:
        response = users_client.delete_user(user_id, headers=headers)
        if response.status_code != 204:
            logger.warning(f"Cleanup - deleting user {user_id} returned unexpected status {response.status_code}")
    except Exception as exc:
        logger.warning(f"Cleanup - deleting user {user_id} returned unexpected status {response.status_code}")
