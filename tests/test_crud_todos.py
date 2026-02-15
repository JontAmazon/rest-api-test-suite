import pytest

from tests.payloads.todo_payloads import build_todo_payload
from tests.utils.assertions import assert_json_content_type, assert_status


def test_create_read_update_delete_todo(created_user, todos_client, users_client, auth_headers):
    # create todo
    payload = build_todo_payload(created_user["id"])
    create_response = todos_client.create_todo(payload, headers=auth_headers)
    assert_status(create_response, 201)
    assert_json_content_type(create_response)
    todo = create_response.json()

    # GET /todos/{todo_id}
    get_response = todos_client.get_todo(todo["id"], headers=auth_headers)
    assert_status(get_response, 200)
    assert get_response.json()["id"] == todo["id"]

    # GET /todos?user_id={user_id}
    list_by_query = todos_client.list_todos(params={"user_id": created_user["id"]}, headers=auth_headers)
    assert_status(list_by_query, 200)
    assert any(item["id"] == todo["id"] for item in list_by_query.json())

    # GET users/{user_id}/todos   (optional)
    list_by_parent = users_client.list_todos_for_user(created_user["id"], headers=auth_headers)
    assert_status(list_by_parent, 200)
    assert any(item["id"] == todo["id"] for item in list_by_parent.json())

    # update todo status
    update_payload = {"status": "completed"}
    update_response = todos_client.update_todo(todo["id"], update_payload, headers=auth_headers)
    assert_status(update_response, 200)
    assert update_response.json()["status"] == "completed"

    # delete todo
    delete_response = todos_client.delete_todo(todo["id"], headers=auth_headers)
    assert_status(delete_response, 204)

    get_deleted = todos_client.get_todo(todo["id"], headers=auth_headers)
    assert_status(get_deleted, 404)

