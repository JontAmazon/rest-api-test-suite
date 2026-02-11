from typing import Any, Dict, Optional

import requests


class BaseClient:
    def __init__(self, base_url: str, session: requests.Session, timeout: int) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = session
        self.timeout = timeout

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.session.get(self._url(path), params=params, headers=headers, timeout=self.timeout)

    def post(self, path: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.session.post(self._url(path), json=payload, headers=headers, timeout=self.timeout)

    def put(self, path: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.session.put(self._url(path), json=payload, headers=headers, timeout=self.timeout)

    def delete(self, path: str, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.session.delete(self._url(path), headers=headers, timeout=self.timeout)
