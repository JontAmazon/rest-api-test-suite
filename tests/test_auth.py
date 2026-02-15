import pytest

from tests.payloads.post_payloads import build_post_payload
from tests.payloads.todo_payloads import build_todo_payload
from tests.payloads.user_payloads import build_user_payload
from tests.utils.assertions import assert_status


def _expected_status(token_case: str) -> int:
    return 401 if token_case in {"missing", "garbage"} else 201


@pytest.mark.auth
@pytest.mark.parametrize("token_case", ["missing", "garbage", "valid"])
def test_auth_on_create_user(users_client, auth_headers, garbage_token_headers, missing_token_headers, token_case):
    payload = build_user_payload()
    headers = {"missing": missing_token_headers, "garbage": garbage_token_headers, "valid": auth_headers}[token_case]
    response = users_client.create_user(payload, headers=headers)
    expected = 401 if token_case != "valid" else 201
    assert_status(response, expected)

    if token_case == "valid":
        users_client.delete_user(response.json()["id"], headers=auth_headers)


@pytest.mark.auth
@pytest.mark.parametrize("token_case", ["missing", "garbage", "valid"])
def test_auth_on_update_user(created_user, users_client, auth_headers, garbage_token_headers, missing_token_headers, token_case):
    headers = {"missing": missing_token_headers, "garbage": garbage_token_headers, "valid": auth_headers}[token_case]
    response = users_client.update_user(created_user["id"], {"name": "Auth Update"}, headers=headers)
    if token_case == "missing":
        expected = 404
    elif token_case == "garbage":
        expected = 401
    else:
        expected = 200
    assert_status(response, expected)


@pytest.mark.auth
@pytest.mark.parametrize("token_case", ["missing", "garbage", "valid"])
def test_auth_on_delete_user(created_user, users_client, auth_headers, garbage_token_headers, missing_token_headers, token_case):
    headers = {"missing": missing_token_headers, "garbage": garbage_token_headers, "valid": auth_headers}[token_case]
    response = users_client.delete_user(created_user["id"], headers=headers)
    if token_case == "missing":
        expected = 404
    elif token_case == "garbage":
        expected = 401
    else:
        expected = 204
    assert_status(response, expected)


@pytest.mark.auth
@pytest.mark.parametrize("token_case", ["missing", "garbage", "valid"])
def test_auth_on_create_post(created_user, posts_client, auth_headers, garbage_token_headers, missing_token_headers, token_case):
    headers = {"missing": missing_token_headers, "garbage": garbage_token_headers, "valid": auth_headers}[token_case]
    response = posts_client.create_post(build_post_payload(created_user["id"]), headers=headers)
    expected = _expected_status(token_case)
    assert_status(response, expected)

    if token_case == "valid":
        posts_client.delete_post(response.json()["id"], headers=auth_headers)


@pytest.mark.auth
@pytest.mark.parametrize("token_case", ["missing", "garbage", "valid"])
def test_auth_on_create_todo(created_user, todos_client, auth_headers, garbage_token_headers, missing_token_headers, token_case):
    headers = {"missing": missing_token_headers, "garbage": garbage_token_headers, "valid": auth_headers}[token_case]
    response = todos_client.create_todo(build_todo_payload(created_user["id"]), headers=headers)
    expected = _expected_status(token_case)
    assert_status(response, expected)

    if token_case == "valid":
        todos_client.delete_todo(response.json()["id"], headers=auth_headers)


