import pytest

from tests.data.post_payloads import build_post_payload
from tests.utils.assertions import assert_json_content_type, assert_status


def test_create_read_update_delete_post(posts_client, users_client, auth_headers, created_user):
    # create post
    payload = build_post_payload(created_user["id"])
    create_response = posts_client.create_post(payload, headers=auth_headers)
    assert_status(create_response, 201)
    assert_json_content_type(create_response)
    post = create_response.json()

    # GET /posts/{post_id}
    get_response = posts_client.get_post(post["id"], headers=auth_headers)
    assert_status(get_response, 200)
    assert get_response.json()["id"] == post["id"]

    # GET /posts?user_id={user_id}
    list_by_query = posts_client.list_posts(params={"user_id": created_user["id"]}, headers=auth_headers)
    assert_status(list_by_query, 200)
    assert any(item["id"] == post["id"] for item in list_by_query.json())

    # GET users/{user_id}/posts   (optional)
    list_by_parent = users_client.list_posts_for_user(created_user["id"], headers=auth_headers)
    assert_status(list_by_parent, 200)
    assert any(item["id"] == post["id"] for item in list_by_parent.json())

    # update post title
    update_payload = {"title": "Updated title"}
    update_response = posts_client.update_post(post["id"], update_payload, headers=auth_headers)
    assert_status(update_response, 200)
    assert update_response.json()["title"] == "Updated title"

    # delete post
    delete_response = posts_client.delete_post(post["id"], headers=auth_headers)
    assert_status(delete_response, 204)

    get_deleted = posts_client.get_post(post["id"], headers=auth_headers)
    assert_status(get_deleted, 404)
