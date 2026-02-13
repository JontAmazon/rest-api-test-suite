# GoRest API Test Suite
A pytest + requests-based API test suite.

## Application under test
GoRest is a publicly available API designed specifically for practicing and demonstrating REST API testing and automation. **Application features** include registering users, login, and each user can create posts and todos.

Endpoints: `/users`, `/posts`, and `/todos`.

## Test Coverage
- **CRUD operations:** happy-path and failure-path tests for CRUD flows.
- **Filtering/searching:** exact/partial matches, combined filters, sorting, and pagination boundaries.
   - TODO: what exactly do we test?
- **Auth behavior:** authorized vs unauthorized access, and token validation.
- **Idempotency:** Duplicate user creation and deletion requests are handled gracefully.
- **Input validation:** required-field checks, enum/value validation (e.g., gender/status), and expected 422 error responses for invalid payloads.

- **JSON schema validation:** response bodies are validated for `POST /users` (`201`) and `GET /todos` (`200`), including required fields and base data types for user objects and todo-list items.

- **API contract checks:** response headers (Content-Type, pagination headers), required-field error behavior (422 + field errors), and unknown-field handling are verified to catch breaking changes.

- **Cleanup behavior:** deleting a user triggers cleanup of posts and todos.

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
    ├── data/
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
    └──---
    └──---
    └──---
    └──---    
```

## Setup
(Recommended: Create a Python virtual environment (venv)).

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
