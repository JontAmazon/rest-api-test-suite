from __future__ import annotations

import datetime as dt
import uuid


def build_todo_payload(user_id: int, title: str | None = None, status: str = "active", due_on: str | None = None) -> dict:
    due_on_value = due_on or (dt.datetime.utcnow() + dt.timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%S.000+05:30")
    return {
        "user_id": user_id,
        "title": title or f"Todo {uuid.uuid4().hex[:8]}",
        "status": status,
        "due_on": due_on_value,
    }
