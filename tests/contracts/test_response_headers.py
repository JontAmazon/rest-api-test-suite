import pytest

from tests.utils.assertions import assert_json_content_type, assert_pagination_headers, assert_status


@pytest.mark.contract
@pytest.mark.parametrize(
    "client_fixture,method",
    [
        ("users_client", "list_users"),
        ("posts_client", "list_posts"),
        ("todos_client", "list_todos"),
    ],
)
def test_response_headers_for_main_endpoints(request, client_fixture, method):
    client = request.getfixturevalue(client_fixture)
    response = getattr(client, method)()
    assert_status(response, 200)
    assert_json_content_type(response)
    assert_pagination_headers(response)
