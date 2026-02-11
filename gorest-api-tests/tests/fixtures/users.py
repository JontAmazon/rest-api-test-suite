from __future__ import annotations

import pytest

from tests.data.user_payloads import build_user_payload


@pytest.fixture
def created_user(users_client, auth_headers):
    payload = build_user_payload()
    response = users_client.create_user(payload, headers=auth_headers)
    assert response.status_code == 201, response.text
    user = response.json()
    yield user
    users_client.delete_user(user["id"], headers=auth_headers)
