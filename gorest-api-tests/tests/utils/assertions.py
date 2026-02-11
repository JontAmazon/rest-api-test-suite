from __future__ import annotations

from typing import Any, Dict

import requests


EXPECTED_RATE_LIMIT_HEADERS = {
    "x-ratelimit-limit",
    "x-ratelimit-remaining",
    "x-ratelimit-reset",
}


def assert_status(response: requests.Response, expected_status: int) -> None:
    assert response.status_code == expected_status, response.text


def assert_json_content_type(response: requests.Response) -> None:
    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type


def assert_rate_limit_headers(response: requests.Response) -> None:
    missing = EXPECTED_RATE_LIMIT_HEADERS - {header.lower() for header in response.headers}
    assert not missing, f"Missing rate limit headers: {missing}"


def assert_has_keys(payload: Dict[str, Any], keys: list[str]) -> None:
    for key in keys:
        assert key in payload
