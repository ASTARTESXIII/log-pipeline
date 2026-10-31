"""Парсер Syslog (RFC 5424 + опционально RFC 3164)."""
from __future__ import annotations

import re

RE_SYSLOG_5424 = re.compile(
    r"<(?P<pri>\d+)>(?P<ver>\d+)\s+"
    r"(?P<timestamp>\S+)\s+(?P<host>\S+)\s+"
    r"(?P<app>\S+)\s+(?P<procid>\S+)\s+"
    r"(?P<msgid>\S+)\s+(?P<structured>\[.*?\])?\s*"
    r"(?P<message>.*)$"
)

RE_SYSLOG_3164 = re.compile(
    r"<(?P<pri>\d+)>"
    r"(?P<timestamp>[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+"
    r"(?P<host>\S+)\s+"
    r"(?P<app>\S+?)(?:\[(?P<procid>\d+)\])?:\s*"
    r"(?P<message>.*)$"
)


def parse_syslog_5424(line: str) -> dict | None:
    """Разбирает строку Syslog RFC 5424.

    Args:
        line: строка вида
            '<34>1 2025-01-02T03:04:05.123Z host1 sshd 1234 ID47 [x] Failed password'.

    Returns:
        dict с ключами UNIFIED_KEYS или None, если строка не по формату.
    """
    if not line or not line.strip():
        return None

    m = RE_SYSLOG_5424.match(line)
    if not m:
        return None

    d = m.groupdict()
    return {
        "timestamp": d["timestamp"],
        "source": "syslog",
        "user": "",
        "event_type": d["app"],
        "severity": d["pri"],
        "raw": line,
    }


def parse_syslog_3164(line: str) -> dict | None:
    """Разбирает строку Syslog RFC 3164 (BSD-формат).

    Args:
        line: строка вида
            '<34>Jan  2 03:04:05 host1 sshd[1234]: Failed password for alice'.

    Returns:
        dict с ключами UNIFIED_KEYS или None, если строка не по формату.
        timestamp остаётся строкой (без года) — нормализация в pipeline.
    """
    if not line or not line.strip():
        return None

    m = RE_SYSLOG_3164.match(line)
    if not m:
        return None

    d = m.groupdict()
    return {
        "timestamp": d["timestamp"],
        "source": "syslog",
        "user": "",
        "event_type": d["app"],
        "severity": d["pri"],
        "raw": line,
    }
