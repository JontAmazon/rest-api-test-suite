from typing import Any, Dict, Optional

import time

import requests


class BaseClient:
    def __init__(self, base_url: str, session: requests.Session, timeout: int) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = session
        self.timeout = timeout

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = self._url(path)
        for attempt in range(3):
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            if response.status_code != 429 or attempt == 2:
                return response
            retry_after = response.headers.get("Retry-After")
            if retry_after and retry_after.isdigit():
                wait_seconds = int(retry_after)
            else:
                wait_seconds = 2**attempt
            time.sleep(wait_seconds)
        return response

    def get(self, path: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self._request("GET", path, params=params, headers=headers)

    def post(self, path: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self._request("POST", path, json=payload, headers=headers)

    def put(self, path: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self._request("PUT", path, json=payload, headers=headers)

    def delete(self, path: str, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self._request("DELETE", path, headers=headers)
