# GoRest API Test Suite

A pytest + requests-based REST API test suite for the GoRest API (v2). The suite exercises CRUD operations, filtering/searching, auth behavior, input validation, and contract/schema checks for `/users`, `/posts`, and `/todos`.

## Project structure
```
gorest-api-tests/
├── README.md
├── requirements.txt
├── pytest.ini
├── .gitignore
├── .env.example
├── reports/
│   └── .gitkeep
├── .github/
│   └── workflows/
│       └── api-tests.yml
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
```

## Setup
1. Create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.env` from the example:
   ```bash
   cp .env.example .env
   ```
4. Update `GOREST_TOKEN` with your API token.

## Running tests
```bash
pytest
```

HTML reports are written to `reports/report.html`.

## Notes
- GoRest resets data daily, so tests create their own resources and clean up when possible.
- Only write endpoints require auth; GETs are intentionally unauthenticated in tests.
