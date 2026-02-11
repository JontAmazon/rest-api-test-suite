import pytest

from tests.data.user_payloads import build_user_payload
from tests.utils.assertions import assert_has_keys, assert_json_content_type, assert_status
from tests.utils.schema_validation import validate_schema


@pytest.mark.smoke
def test_create_read_update_delete_user(users_client, auth_headers):
    payload = build_user_payload()
    create_response = users_client.create_user(payload, headers=auth_headers)
    assert_status(create_response, 201)
    assert_json_content_type(create_response)
    user = create_response.json()
    assert_has_keys(user, ["id", "name", "email", "gender", "status"])
    validate_schema(user, "user_create.schema.json")

    get_response = users_client.get_user(user["id"])
    assert_status(get_response, 200)
    assert_json_content_type(get_response)
    fetched = get_response.json()
    assert fetched["id"] == user["id"]

    update_payload = {"name": "Updated Name"}
    update_response = users_client.update_user(user["id"], update_payload, headers=auth_headers)
    assert_status(update_response, 200)
    assert update_response.json()["name"] == "Updated Name"

    delete_response = users_client.delete_user(user["id"], headers=auth_headers)
    assert_status(delete_response, 204)

    get_deleted = users_client.get_user(user["id"])
    assert_status(get_deleted, 404)
