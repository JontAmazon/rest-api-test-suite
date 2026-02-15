from tests.payloads.post_payloads import build_post_payload
from tests.payloads.todo_payloads import build_todo_payload
from tests.payloads.user_payloads import build_user_payload
from tests.utils.assertions import assert_status


def test_deleted_user_cleanup(created_user, created_post, created_todo,users_client, posts_client, todos_client, auth_headers):
    # Delete the user. This should also delete the associated post and todo.
    delete_response = users_client.delete_user(created_user["id"], headers=auth_headers)
    assert_status(delete_response, 204)

    get_post = posts_client.get_post(created_post["id"])
    assert_status(get_post, 404)

    get_todo = todos_client.get_todo(created_todo["id"])
    assert_status(get_todo, 404)

    # It shall not be possible to create new posts or todos for the deleted user.
    create_post = posts_client.create_post(build_post_payload(created_user["id"]), headers=auth_headers)
    assert_status(create_post, 422)

    create_todo = todos_client.create_todo(build_todo_payload(created_user["id"]), headers=auth_headers)
    assert_status(create_todo, 422)

