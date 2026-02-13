from typing import Any, Dict, Optional

import requests

from tests.clients.base_client import BaseClient


class TodosClient(BaseClient):
    def list_todos(self, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.get("todos", params=params, headers=headers)

    def get_todo(self, todo_id: int, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.get(f"todos/{todo_id}", headers=headers)

    def create_todo(self, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.post("todos", payload=payload, headers=headers)

    def update_todo(self, todo_id: int, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.put(f"todos/{todo_id}", payload=payload, headers=headers)

    def delete_todo(self, todo_id: int, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.delete(f"todos/{todo_id}", headers=headers)
