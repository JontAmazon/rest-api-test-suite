from __future__ import annotations

import warnings

import pytest

from tests.data.user_payloads import build_user_payload


@pytest.fixture
def created_user(users_client, auth_headers):
    payload = build_user_payload()
    response = users_client.create_user(payload, headers=auth_headers)
    assert response.status_code == 201, response.text
    user = response.json()
    yield user
    try:
        delete_response = users_client.delete_user(user["id"], headers=auth_headers)
        if delete_response.status_code not in {204, 404}:
            warnings.warn(
                f"Fixture cleanup: deleting user {user['id']} returned {delete_response.status_code}",
                stacklevel=2,
            )
    except Exception as exc:
        warnings.warn(f"Fixture cleanup: deleting user {user['id']} failed: {exc}", stacklevel=2)

def delete_user_ignore_errors(users_client, user_id: int, headers: dict[str, str]) -> None:
    try:
        response = users_client.delete_user(user_id, headers=headers)
        if response.status_code != 204:
            warnings.warn(
                f"Cleanup - deleting user {user_id} returned unexpected status {response.status_code}", stacklevel=2,
            )
    except Exception as exc:
        warnings.warn(f"Cleanup - deleting user {user_id} failed: {exc}", stacklevel=2)