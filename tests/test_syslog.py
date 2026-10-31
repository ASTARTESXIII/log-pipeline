"""Юнит-тесты парсера Syslog."""
from parsers.syslog_parser import parse_syslog_5424, parse_syslog_3164


# --- позитивные ---

def test_syslog_5424_ok():
    line = "<34>1 2025-01-02T03:04:05Z host1 sshd 1234 ID47 [x] Failed password for alice"
    rec = parse_syslog_5424(line)
    assert rec is not None
    assert rec["event_type"] == "sshd"
    assert rec["severity"] == "34"
    assert rec["source"] == "syslog"
    assert rec["timestamp"] == "2025-01-02T03:04:05Z"


def test_syslog_3164_ok():
    line = "<34>Jan  2 03:04:05 host1 sshd[1234]: Failed password for alice"
    rec = parse_syslog_3164(line)
    assert rec is not None
    assert rec["event_type"] == "sshd"
    assert rec["severity"] == "34"


# --- негативные ---

def test_syslog_5424_broken():
    assert parse_syslog_5424("совсем не syslog") is None


def test_syslog_5424_empty():
    assert parse_syslog_5424("") is None
    assert parse_syslog_5424("   ") is None


def test_syslog_3164_broken():
    assert parse_syslog_3164("совсем не syslog") is None
