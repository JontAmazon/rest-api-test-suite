from tests.data.todo_payloads import build_todo_payload
from tests.data.user_payloads import build_user_payload
from tests.utils.assertions import assert_status


def test_user_gender_validation(users_client, auth_headers):
    payload = build_user_payload(gender="invalid")
    response = users_client.create_user(payload, headers=auth_headers)
    assert_status(response, 422)


def test_todo_status_validation(todos_client, users_client, auth_headers):
    user_response = users_client.create_user(build_user_payload(), headers=auth_headers)
    assert_status(user_response, 201)
    user = user_response.json()

    payload = build_todo_payload(user["id"], status="invalid")
    response = todos_client.create_todo(payload, headers=auth_headers)
    assert_status(response, 422)

    users_client.delete_user(user["id"], headers=auth_headers)
