from __future__ import annotations

import warnings

import pytest

from tests.data.post_payloads import build_post_payload


@pytest.fixture
def created_post(posts_client, auth_headers, created_user):
    payload = build_post_payload(created_user["id"])
    response = posts_client.create_post(payload, headers=auth_headers)
    assert response.status_code == 201, response.text
    post = response.json()
    yield post
    delete_post_ignore_errors(posts_client, post["id"], headers=auth_headers)


def delete_post_ignore_errors(posts_client, post_id: int, headers: dict[str, str]) -> None:
    try:
        response = posts_client.delete_post(post_id, headers=headers)
        if response.status_code != 204:
            warnings.warn(f"Cleanup - deleting post {post_id} returned unexpected status {response.status_code}", stacklevel=2)
    except Exception as exc:
        warnings.warn(f"Cleanup - deleting post {post_id} failed: {exc}", stacklevel=2)
