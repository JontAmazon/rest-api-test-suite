from __future__ import annotations

import os
import uuid

pytest_plugins = [
    "tests.fixtures.users",
    "tests.fixtures.posts",
    "tests.fixtures.todos",
]

import pytest
import requests

from tests.clients.posts_client import PostsClient
from tests.clients.todos_client import TodosClient
from tests.clients.users_client import UsersClient
from tests.config import BASE_URL, GOREST_TOKEN, REQUEST_TIMEOUT


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def request_timeout() -> int:
    return REQUEST_TIMEOUT


@pytest.fixture(scope="session")
def session() -> requests.Session:
    return requests.Session()


@pytest.fixture(scope="session")
def users_client(base_url: str, session: requests.Session, request_timeout: int) -> UsersClient:
    return UsersClient(base_url, session, request_timeout)


@pytest.fixture(scope="session")
def posts_client(base_url: str, session: requests.Session, request_timeout: int) -> PostsClient:
    return PostsClient(base_url, session, request_timeout)


@pytest.fixture(scope="session")
def todos_client(base_url: str, session: requests.Session, request_timeout: int) -> TodosClient:
    return TodosClient(base_url, session, request_timeout)


@pytest.fixture(scope="session")
def valid_token() -> str | None:
    return GOREST_TOKEN


@pytest.fixture(scope="session")
def auth_headers(valid_token: str | None) -> dict[str, str]:
    if not valid_token:
        pytest.skip("GOREST_TOKEN is not configured")
    return {"Authorization": f"Bearer {valid_token}"}


@pytest.fixture(scope="session")
def garbage_token_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer garbage-{uuid.uuid4().hex}"}


@pytest.fixture(scope="session")
def missing_token_headers() -> dict[str, str]:
    return {}


@pytest.fixture(scope="session")
def random_keyword() -> str:
    return f"keyword-{uuid.uuid4().hex}-{os.getpid()}"
