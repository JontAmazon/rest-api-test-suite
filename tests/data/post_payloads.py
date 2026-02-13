from __future__ import annotations

import uuid


def build_post_payload(user_id: int, title: str | None = None, body: str | None = None) -> dict:
    return {
        "user_id": user_id,
        "title": title or f"Post {uuid.uuid4().hex[:8]}",
        "body": body or f"Body {uuid.uuid4().hex}",
    }


def build_keyword_body(keyword: str) -> str:
    return f"This is a test body with keyword: {keyword}."
