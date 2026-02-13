from tests.data.user_payloads import build_user_payload
from tests.utils.assertions import assert_status


def test_delete_user_twice(created_user, users_client, auth_headers):
    user_id = created_user["id"]

    first_delete = users_client.delete_user(user_id, headers=auth_headers)
    assert_status(first_delete, 204)

    second_delete = users_client.delete_user(user_id, headers=auth_headers)
    assert_status(second_delete, 404)


def test_create_user_email_already_exists(users_client, auth_headers):
    user_payload = build_user_payload()
    create_response = users_client.create_user(user_payload, headers=auth_headers)
    assert_status(create_response, 201)
    user = create_response.json()

    duplicate_response = users_client.create_user(user_payload, headers=auth_headers)
    assert_status(duplicate_response, 422)

    users_client.delete_user(user["id"], headers=auth_headers)
