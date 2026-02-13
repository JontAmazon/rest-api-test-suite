from tests.data.user_payloads import build_user_payload
from tests.utils.assertions import assert_status
from tests.utils.schema_validation import validate_schema


def test_user_create_schema(users_client, auth_headers):
    response = users_client.create_user(build_user_payload(), headers=auth_headers)
    assert_status(response, 201)
    payload = response.json()
    validate_schema(payload, "user_create.schema.json")

    users_client.delete_user(payload["id"], headers=auth_headers)


def test_todos_list_schema(todos_client):
    response = todos_client.list_todos()
    assert_status(response, 200)
    validate_schema(response.json(), "todos_list.schema.json")
