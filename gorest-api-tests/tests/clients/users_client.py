from typing import Any, Dict, Optional

import requests

from tests.clients.base_client import BaseClient


class UsersClient(BaseClient):
    def list_users(self, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.get("users", params=params, headers=headers)

    def get_user(self, user_id: int, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.get(f"users/{user_id}", headers=headers)

    def create_user(self, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.post("users", payload=payload, headers=headers)

    def update_user(self, user_id: int, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.put(f"users/{user_id}", payload=payload, headers=headers)

    def delete_user(self, user_id: int, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.delete(f"users/{user_id}", headers=headers)

    def list_posts_for_user(self, user_id: int, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.get(f"users/{user_id}/posts", headers=headers)

    def list_todos_for_user(self, user_id: int, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.get(f"users/{user_id}/todos", headers=headers)

    def create_todo_for_user(self, user_id: int, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.post(f"users/{user_id}/todos", payload=payload, headers=headers)
