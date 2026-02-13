from __future__ import annotations

import uuid


def unique_email(prefix: str = "user") -> str:
    token = uuid.uuid4().hex
    return f"{prefix}-{token}@example.com"


def build_user_payload(name: str | None = None, gender: str = "female", status: str = "active") -> dict:
    return {
        "name": name or f"Test User {uuid.uuid4().hex[:8]}",
        "email": unique_email("gorest"),
        "gender": gender,
        "status": status,
    }
