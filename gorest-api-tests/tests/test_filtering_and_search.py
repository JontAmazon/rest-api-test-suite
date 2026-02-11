import datetime as dt

from tests.data.post_payloads import build_keyword_body, build_post_payload
from tests.data.todo_payloads import build_todo_payload
from tests.data.user_payloads import build_user_payload
from tests.utils.assertions import assert_status


def test_filter_posts_by_user(posts_client, users_client, auth_headers):
    user_payload = build_user_payload()
    user_response = users_client.create_user(user_payload, headers=auth_headers)
    assert_status(user_response, 201)
    user = user_response.json()

    post_response = posts_client.create_post(build_post_payload(user["id"]), headers=auth_headers)
    assert_status(post_response, 201)
    post = post_response.json()

    list_by_user = posts_client.list_posts(params={"user_id": user["id"]})
    assert_status(list_by_user, 200)
    assert any(item["id"] == post["id"] for item in list_by_user.json())

    posts_client.delete_post(post["id"], headers=auth_headers)
    users_client.delete_user(user["id"], headers=auth_headers)


def test_filter_todos_by_user_and_due_on(todos_client, users_client, auth_headers):
    user_payload = build_user_payload()
    user_response = users_client.create_user(user_payload, headers=auth_headers)
    assert_status(user_response, 201)
    user = user_response.json()

    due_on_value = (dt.datetime.utcnow() + dt.timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S.000+05:30")
    todo_payload = build_todo_payload(user["id"], due_on=due_on_value)
    todo_response = todos_client.create_todo(todo_payload, headers=auth_headers)
    assert_status(todo_response, 201)
    todo = todo_response.json()

    list_by_filter = todos_client.list_todos(params={"user_id": user["id"], "due_on": due_on_value})
    assert_status(list_by_filter, 200)
    assert any(item["id"] == todo["id"] for item in list_by_filter.json())

    todos_client.delete_todo(todo["id"], headers=auth_headers)
    users_client.delete_user(user["id"], headers=auth_headers)


def test_search_posts_by_body_keyword(posts_client, users_client, auth_headers, random_keyword):
    users = []
    posts = []

    for _ in range(2):
        user_response = users_client.create_user(build_user_payload(), headers=auth_headers)
        assert_status(user_response, 201)
        users.append(user_response.json())

    matched_body = build_keyword_body(random_keyword)
    for user in users:
        response = posts_client.create_post(
            build_post_payload(user["id"], body=matched_body if user == users[0] else "No match body"),
            headers=auth_headers,
        )
        assert_status(response, 201)
        posts.append(response.json())

    list_by_body = posts_client.list_posts(params={"body": random_keyword})
    assert_status(list_by_body, 200)
    result_ids = {item["id"] for item in list_by_body.json()}
    assert posts[0]["id"] in result_ids

    for post in posts:
        posts_client.delete_post(post["id"], headers=auth_headers)
    for user in users:
        users_client.delete_user(user["id"], headers=auth_headers)
