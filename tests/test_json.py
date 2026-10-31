"""Юнит-тесты парсера JSON."""
import pytest

from parsers.json_parser import parse_json_line


# --- позитивные ---

def test_json_ok_basic():
    rec = parse_json_line(
        '{"timestamp":"2025-01-02T03:04:05Z","user":"bob",'
        '"event_type":"login_failed","severity":"high"}'
    )
    assert rec is not None
    assert rec["user"] == "bob"
    assert rec["event_type"] == "login_failed"
    assert rec["severity"] == "high"
    assert rec["source"] == "json"


def test_json_ok_cloudtrail_nested_user():
    rec = parse_json_line(
        '{"eventTime":"2025-01-02T03:04:05Z",'
        '"eventName":"ConsoleLogin",'
        '"userIdentity":{"userName":"alice"}}'
    )
    assert rec is not None
    assert rec["user"] == "alice"
    assert rec["event_type"] == "ConsoleLogin"
    assert rec["timestamp"] == "2025-01-02T03:04:05Z"


# --- негативные ---

def test_json_broken():
    assert parse_json_line("не json") is None


def test_json_empty():
    assert parse_json_line("") is None
    assert parse_json_line("   ") is None


def test_json_not_a_dict():
    # валидный JSON, но не объект
    assert parse_json_line("[1, 2, 3]") is None
    assert parse_json_line("42") is None
