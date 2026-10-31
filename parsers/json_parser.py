"""Парсер JSON-логов (JSON Lines) в унифицированную схему события ИБ."""
from __future__ import annotations

import json

UNIFIED_KEYS = [
    "timestamp", "source", "user",
    "event_type", "severity", "raw",
]


def parse_json_line(line: str) -> dict | None:
    """Разбирает одну строку JSON-лога.

    Поддерживает разные имена полей (ts / timestamp / eventTime),
    вложенный userIdentity.userName (CloudTrail-подобные логи).

    Args:
        line: одна строка JSON-лога.

    Returns:
        dict с ключами UNIFIED_KEYS или None, если строка битая / пустая.
    """
    if not line or not line.strip():
        return None

    try:
        obj = json.loads(line)
    except (json.JSONDecodeError, TypeError):
        return None

    if not isinstance(obj, dict):
        return None

    # user может быть вложенным (CloudTrail)
    user = obj.get("user")
    if not user and isinstance(obj.get("userIdentity"), dict):
        user = obj["userIdentity"].get("userName", "")

    return {
        "timestamp": obj.get("ts") or obj.get("timestamp") or obj.get("eventTime", ""),
        "source": "json",
        "user": user or "",
        "event_type": obj.get("event_type") or obj.get("eventName", ""),
        "severity": str(obj.get("severity", "")),
        "raw": line,
    }
