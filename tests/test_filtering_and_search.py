import datetime as dt

from tests.payloads.post_payloads import build_keyword_body, build_post_payload
from tests.payloads.todo_payloads import build_todo_payload
from tests.utils.assertions import assert_status


def test_filter_posts_by_user(created_post, created_user, posts_client, auth_headers):
    list_by_user = posts_client.list_posts(params={"user_id": created_user["id"]}, headers=auth_headers)
    assert_status(list_by_user, 200)
    assert any(item["id"] == created_post["id"] for item in list_by_user.json())


def test_filter_todos_by_user_and_due_on(todos_client, created_user, auth_headers):
    due_on_value = (dt.datetime.now(dt.UTC) + dt.timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S.000+05:30")
    todo_payload = build_todo_payload(created_user["id"], due_on=due_on_value)
    todo_response = todos_client.create_todo(todo_payload, headers=auth_headers)
    assert_status(todo_response, 201)
    todo = todo_response.json()

    list_by_filter = todos_client.list_todos(params={"user_id": created_user["id"], "due_on": due_on_value}, headers=auth_headers)
    assert_status(list_by_filter, 200)
    assert any(item["id"] == todo["id"] for item in list_by_filter.json())


def test_search_posts_by_body_keyword(posts_client, created_user, auth_headers, random_keyword):
    posts = []
    body_with_keyword = build_keyword_body(random_keyword)
    for body in [body_with_keyword, "this body should not match"]:
        response = posts_client.create_post(build_post_payload(created_user["id"], body=body), headers=auth_headers)
        assert_status(response, 201)
        posts.append(response.json())

    list_by_body = posts_client.list_posts(params={"body": random_keyword}, headers=auth_headers)
    assert_status(list_by_body, 200)
    result_ids = {item["id"] for item in list_by_body.json()}
    assert posts[0]["id"] in result_ids
    assert posts[1]["id"] not in result_ids

    for post in posts:
        posts_client.delete_post(post["id"], headers=auth_headers)

