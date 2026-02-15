from typing import Any, Dict, Optional

import requests

from tests.clients.base_client import BaseClient


class PostsClient(BaseClient):
    def list_posts(self, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.get("posts", params=params, headers=headers)

    def get_post(self, post_id: int, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.get(f"posts/{post_id}", headers=headers)

    def create_post(self, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.post("posts", payload=payload, headers=headers)

    def update_post(self, post_id: int, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.put(f"posts/{post_id}", payload=payload, headers=headers)

    def delete_post(self, post_id: int, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.delete(f"posts/{post_id}", headers=headers)

