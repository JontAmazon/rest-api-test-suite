from tests.data.post_payloads import build_post_payload
from tests.data.todo_payloads import build_todo_payload
from tests.data.user_payloads import build_user_payload
from tests.utils.assertions import assert_status


def test_deleted_user_cleanup(users_client, posts_client, todos_client, auth_headers):
    user_response = users_client.create_user(build_user_payload(), headers=auth_headers)
    assert_status(user_response, 201)
    user = user_response.json()

    post_response = posts_client.create_post(build_post_payload(user["id"]), headers=auth_headers)
    assert_status(post_response, 201)
    post = post_response.json()

    todo_response = todos_client.create_todo(build_todo_payload(user["id"]), headers=auth_headers)
    assert_status(todo_response, 201)
    todo = todo_response.json()

    delete_response = users_client.delete_user(user["id"], headers=auth_headers)
    assert_status(delete_response, 204)

    get_post = posts_client.get_post(post["id"])
    assert_status(get_post, 404)

    get_todo = todos_client.get_todo(todo["id"])
    assert_status(get_todo, 404)

    create_post = posts_client.create_post(build_post_payload(user["id"]), headers=auth_headers)
    assert_status(create_post, 422)

    create_todo = todos_client.create_todo(build_todo_payload(user["id"]), headers=auth_headers)
    assert_status(create_todo, 422)
