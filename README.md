# GoRest API Test Suite
A pytest + requests-based API test suite.

## Application under test
GoRest is a publicly available API designed specifically for practicing and demonstrating REST API testing and automation. **Application features** include registering users, login, and each user can create posts and todos.

Endpoints: `/users`, `/posts`, and `/todos`.

## Test Coverage
- **CRUD operations:** positive and negative tests for CRUD flows.
- **Filtering/searching:** filtering posts by `user_id`, filtering todos by `user_id + due_on`, and searching posts by keyword.
- **Auth behavior:** authorized vs unauthorized access, and token validation.
- **Idempotency:** duplicate user creation and deletion requests are handled gracefully.
- **Cleanup behavior:** deleting a user triggers cleanup of posts and todos.
- **API contract checks:** verifies response headers (e.g. Content-Type, pagination), required fields, and API behavior for unknown fields, and invalid input values.
- **JSON schema validation:** response bodies for `POST /users (201)` and `GET /todos (200)` are validated against JSON schemas, asserting required fields and data types while allowing non-breaking additions (optional parameters).


## Features
- fixtures for creating users, posts and todos.
   - setup and cleanup separated from tests.
- parametrization for e.g. required fields and auth tests.
- logging of requests.


## Project structure
```
gorest-api-tests/
├── README.md
├── requirements.txt
├── .env.example
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── config.py
    ├── clients/
    ├── fixtures/
    ├── payloads/
    ├── schemas/
    ├── utils/
    ├── test_crud_users.py
    ├── test_crud_posts.py
    ├── test_crud_todos.py
    ├── test_filtering_and_search.py
    ├── test_auth.py
    ├── test_deleted_user_cleanup.py
    ├── test_idempotency.py
    ├── test_input_validation.py
    └── contracts/
        ├── test_input_validation.py
        ├── test_required_fields.py
        ├── test_response_headers.py
        ├── test_schema_validation.py
        └── test_unknown_fields.py
```

## Setup
(Recommended: Create a Python virtual environment - venv).

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a free account at (GoRest)[https://gorest.co.in/my-account/access-tokens].
3. Copy your API token.
4. Create `.env`:
   ```bash
   cp .env.example .env
   ```
5. Update `GOREST_TOKEN` with your API token.


## Running tests
```bash
pytest
```

HTML reports are written to `reports/report.html`.
