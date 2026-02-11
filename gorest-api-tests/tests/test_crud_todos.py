import pytest

from tests.data.todo_payloads import build_todo_payload
from tests.utils.assertions import assert_json_content_type, assert_status


def test_create_read_update_delete_todo(todos_client, users_client, auth_headers, created_user):
    payload = build_todo_payload(created_user["id"])
    create_response = todos_client.create_todo(payload, headers=auth_headers)
    assert_status(create_response, 201)
    assert_json_content_type(create_response)
    todo = create_response.json()

    get_response = todos_client.get_todo(todo["id"], headers=auth_headers)
    assert_status(get_response, 200)
    assert get_response.json()["id"] == todo["id"]

    update_payload = {"status": "completed"}
    update_response = todos_client.update_todo(todo["id"], update_payload, headers=auth_headers)
    assert_status(update_response, 200)
    assert update_response.json()["status"] == "completed"

    list_by_query = todos_client.list_todos(params={"user_id": created_user["id"]}, headers=auth_headers)
    assert_status(list_by_query, 200)
    assert any(item["id"] == todo["id"] for item in list_by_query.json())

    list_by_parent = users_client.list_todos_for_user(created_user["id"], headers=auth_headers)
    assert_status(list_by_parent, 200)
    assert any(item["id"] == todo["id"] for item in list_by_parent.json())

    delete_response = todos_client.delete_todo(todo["id"], headers=auth_headers)
    assert_status(delete_response, 204)

    get_deleted = todos_client.get_todo(todo["id"], headers=auth_headers)
    assert_status(get_deleted, 404)
