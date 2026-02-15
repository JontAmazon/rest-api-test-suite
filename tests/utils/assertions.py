from __future__ import annotations

from typing import Any, Dict

import requests


EXPECTED_PAGINATION_HEADERS = {
    "x-pagination-limit",
    "x-pagination-page",
    "x-pagination-pages",
    "x-pagination-total",
}


def assert_status(response: requests.Response, expected_status: int) -> None:
    assert response.status_code == expected_status, response.text


def assert_json_content_type(response: requests.Response) -> None:
    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type


def assert_pagination_headers(response: requests.Response) -> None:
    missing = EXPECTED_PAGINATION_HEADERS - {header.lower() for header in response.headers}
    assert not missing, f"Missing pagination headers: {missing}"


def assert_has_keys(payload: Dict[str, Any], keys: list[str]) -> None:
    for key in keys:
        assert key in payload

