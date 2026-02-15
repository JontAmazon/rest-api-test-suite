from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional

import time

import requests

from tests.config import API_LOG_LEVEL


SENSITIVE_HEADERS = {"authorization", "proxy-authorization", "x-api-key"}
MAX_LOG_BODY_LENGTH = 300


def _normalize_log_level(log_level: str) -> str:
    return (log_level or "INFO").strip().upper()


def _is_logging_off(log_level: str) -> bool:
    return _normalize_log_level(log_level) in {"OFF", "NONE", "0", "FALSE"}


def _resolve_log_level(log_level: str) -> int:
    level_name = _normalize_log_level(log_level)
    return {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }.get(level_name, logging.WARNING)


class BaseClient:
    """HTTP client for API endpoint requests with retry and logging.

    Logging:
    - currently just to console.
    - always logs when status code is >= 400, independently of API_LOG_LEVEL.
    """

    def __init__(self, base_url: str, session: requests.Session, timeout: int) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = session
        self.timeout = timeout
        self._log_level_name = _normalize_log_level(API_LOG_LEVEL)
        self._normal_logging_enabled = not _is_logging_off(self._log_level_name)
        self._normal_log_threshold = _resolve_log_level(self._log_level_name)
        self.logger = logging.getLogger("tests.api_client")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("\n%(levelname)s %(asctime)s\n%(message)s"))
            self.logger.addHandler(handler)
            self.logger.propagate = False
        self.logger.setLevel(min(self._normal_log_threshold, logging.ERROR))

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def _request(self, method: str, path: str, success_log_level: int = logging.DEBUG, **kwargs: Any) -> requests.Response:
        url = self._url(path)
        for attempt in range(3):
            started_at = time.perf_counter()
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            elapsed_ms = (time.perf_counter() - started_at) * 1000

            if response.status_code >= 400:
                self._log_failure(method, path, kwargs, response, elapsed_ms, attempt)
            else:
                self._log_request_summary(method, path, response, elapsed_ms, attempt, success_log_level)

            if response.status_code != 429 or attempt == 2:
                return response

            retry_after = response.headers.get("Retry-After")
            if retry_after and retry_after.isdigit():
                wait_seconds = int(retry_after)
            else:
                wait_seconds = 2**attempt
            self.logger.warning(
                "Retrying %s %s after 429 (attempt %s), waiting %ss\nresponse_snippet=%s",
                method,
                path,
                attempt + 1,
                wait_seconds,
                self._response_body_for_log(response),
            )
            time.sleep(wait_seconds)
        return response

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        success_log_level: int = logging.DEBUG,
    ) -> requests.Response:
        return self._request("GET", path, params=params, headers=headers, success_log_level=success_log_level)

    def post(
        self,
        path: str,
        payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
        success_log_level: int = logging.DEBUG,
    ) -> requests.Response:
        return self._request("POST", path, json=payload, headers=headers, success_log_level=success_log_level)

    def put(
        self,
        path: str,
        payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
        success_log_level: int = logging.DEBUG,
    ) -> requests.Response:
        return self._request("PUT", path, json=payload, headers=headers, success_log_level=success_log_level)

    def delete(self, path: str, headers: Optional[Dict[str, str]] = None, success_log_level: int = logging.DEBUG) -> requests.Response:
        return self._request("DELETE", path, headers=headers, success_log_level=success_log_level)

    # Helper methods for logging
    def _redact_headers(self, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        if not headers:
            return {}
        redacted: Dict[str, str] = {}
        for key, value in headers.items():
            if key.lower() in SENSITIVE_HEADERS:
                redacted[key] = "<redacted>"
            else:
                redacted[key] = value
        return redacted

    def _serialize_body(self, body: Any) -> str:
        if body is None:
            return "<none>"
        if isinstance(body, (dict, list)):
            try:
                rendered = json.dumps(body, ensure_ascii=True)
            except (TypeError, ValueError):
                rendered = str(body)
        else:
            rendered = str(body)
        if len(rendered) <= MAX_LOG_BODY_LENGTH:
            return rendered
        return f"{rendered[:MAX_LOG_BODY_LENGTH]}...<truncated>"

    def _request_body_for_log(self, kwargs: Dict[str, Any]) -> str:
        if "json" in kwargs:
            return self._serialize_body(kwargs.get("json"))
        if "data" in kwargs:
            return self._serialize_body(kwargs.get("data"))
        return "<none>"

    def _response_body_for_log(self, response: requests.Response) -> str:
        return self._serialize_body(response.text)

    def _log_request_summary(
        self,
        method: str,
        path: str,
        response: requests.Response,
        elapsed_ms: float,
        attempt: int,
        success_log_level: int,
    ) -> None:
        if not self._normal_logging_enabled:
            return
        if success_log_level < self._normal_log_threshold:
            return
        self.logger.log(
            success_log_level,
            "%s %s -> %s in %.1fms (attempt %s)\nresponse_snippet=%s",
            method,
            path,
            response.status_code,
            elapsed_ms,
            attempt + 1,
            self._response_body_for_log(response),
        )

    def _log_failure(self, method: str, path: str, kwargs: Dict[str, Any], response: requests.Response, elapsed_ms: float, attempt: int) -> None:
        self.logger.error(
            "%s %s -> %s in %.1fms (attempt %s)\nrequest_headers=%s\nparams=%s\nrequest_body=%s\nresponse_headers=%s\nresponse_body=%s",
            method,
            path,
            response.status_code,
            elapsed_ms,
            attempt + 1,
            self._redact_headers(kwargs.get("headers")),
            self._serialize_body(kwargs.get("params")),
            self._request_body_for_log(kwargs),
            self._redact_headers(dict(response.headers)),
            self._response_body_for_log(response),
        )

