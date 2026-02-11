import pytest

from tests.data.post_payloads import build_post_payload
from tests.data.todo_payloads import build_todo_payload
from tests.data.user_payloads import build_user_payload
from tests.utils.assertions import assert_status


def _expected_status(token_case: str) -> int:
    return 401 if token_case in {"missing", "garbage"} else 201


@pytest.mark.auth
@pytest.mark.parametrize("token_case", ["missing", "garbage", "valid"])
def test_auth_on_create_user(users_client, auth_headers, garbage_token_headers, missing_token_headers, token_case):
    payload = build_user_payload()
    headers = {
        "missing": missing_token_headers,
        "garbage": garbage_token_headers,
        "valid": auth_headers,
    }[token_case]
    response = users_client.create_user(payload, headers=headers)
    expected = 401 if token_case != "valid" else 201
    assert_status(response, expected)

    if token_case == "valid":
        users_client.delete_user(response.json()["id"], headers=auth_headers)


@pytest.mark.auth
@pytest.mark.parametrize("token_case", ["missing", "garbage", "valid"])
def test_auth_on_update_user(users_client, auth_headers, garbage_token_headers, missing_token_headers, token_case):
    user_response = users_client.create_user(build_user_payload(), headers=auth_headers)
    assert_status(user_response, 201)
    user = user_response.json()

    headers = {
        "missing": missing_token_headers,
        "garbage": garbage_token_headers,
        "valid": auth_headers,
    }[token_case]
    response = users_client.update_user(user["id"], {"name": "Auth Update"}, headers=headers)
    expected = 401 if token_case != "valid" else 200
    assert_status(response, expected)

    users_client.delete_user(user["id"], headers=auth_headers)


@pytest.mark.auth
@pytest.mark.parametrize("token_case", ["missing", "garbage", "valid"])
def test_auth_on_delete_user(users_client, auth_headers, garbage_token_headers, missing_token_headers, token_case):
    user_response = users_client.create_user(build_user_payload(), headers=auth_headers)
    assert_status(user_response, 201)
    user = user_response.json()

    headers = {
        "missing": missing_token_headers,
        "garbage": garbage_token_headers,
        "valid": auth_headers,
    }[token_case]
    response = users_client.delete_user(user["id"], headers=headers)
    expected = 401 if token_case != "valid" else 204
    assert_status(response, expected)

    users_client.delete_user(user["id"], headers=auth_headers)


@pytest.mark.auth
@pytest.mark.parametrize("token_case", ["missing", "garbage", "valid"])
def test_auth_on_create_post(posts_client, users_client, auth_headers, garbage_token_headers, missing_token_headers, token_case):
    user_response = users_client.create_user(build_user_payload(), headers=auth_headers)
    assert_status(user_response, 201)
    user = user_response.json()

    headers = {
        "missing": missing_token_headers,
        "garbage": garbage_token_headers,
        "valid": auth_headers,
    }[token_case]
    response = posts_client.create_post(build_post_payload(user["id"]), headers=headers)
    expected = _expected_status(token_case)
    assert_status(response, expected)

    if token_case == "valid":
        posts_client.delete_post(response.json()["id"], headers=auth_headers)

    users_client.delete_user(user["id"], headers=auth_headers)


@pytest.mark.auth
@pytest.mark.parametrize("token_case", ["missing", "garbage", "valid"])
def test_auth_on_create_todo(todos_client, users_client, auth_headers, garbage_token_headers, missing_token_headers, token_case):
    user_response = users_client.create_user(build_user_payload(), headers=auth_headers)
    assert_status(user_response, 201)
    user = user_response.json()

    headers = {
        "missing": missing_token_headers,
        "garbage": garbage_token_headers,
        "valid": auth_headers,
    }[token_case]
    response = todos_client.create_todo(build_todo_payload(user["id"]), headers=headers)
    expected = _expected_status(token_case)
    assert_status(response, expected)

    if token_case == "valid":
        todos_client.delete_todo(response.json()["id"], headers=auth_headers)

    users_client.delete_user(user["id"], headers=auth_headers)
