from __future__ import annotations

import pytest

from tests.data.post_payloads import build_post_payload


@pytest.fixture
def created_post(posts_client, auth_headers, created_user):
    payload = build_post_payload(created_user["id"])
    response = posts_client.create_post(payload, headers=auth_headers)
    assert response.status_code == 201, response.text
    post = response.json()
    yield post
    posts_client.delete_post(post["id"], headers=auth_headers)
