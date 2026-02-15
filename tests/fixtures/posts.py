from __future__ import annotations

import logging

import pytest

from tests.payloads.post_payloads import build_post_payload

logger = logging.getLogger(__name__)


@pytest.fixture
def created_post(created_user, posts_client, auth_headers):
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
            logger.warning("Cleanup - deleting post %s returned unexpected status %s", post_id, response.status_code)
    except Exception:
        logger.exception("Cleanup - deleting post %s failed", post_id)

