"""Интеграционные тесты пайплайна."""
import os

import pandas as pd
import pytest

from pipeline import run_pipeline, UNIFIED_COLUMNS


def _write_jsonl(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def _write_syslog(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def test_pipeline_unknown_source():
    with pytest.raises(ValueError):
        run_pipeline("whatever", "unknown_type")


def test_pipeline_json_contract(tmp_path):
    p = tmp_path / "demo.jsonl"
    _write_jsonl(p, [
        '{"timestamp":"2025-01-02T03:04:05Z","user":"alice",'
        '"event_type":"login_failed","severity":"high"}',
        '{"eventTime":"2025-01-02T03:05:00Z","eventName":"ConsoleLogin",'
        '"userIdentity":{"userName":"bob"}}',
        "битая строка",
    ])
    df = run_pipeline(str(p), "json")
    assert list(df.columns) == UNIFIED_COLUMNS
    assert str(df["timestamp"].dtype) == "datetime64[ns, UTC]"
    assert (df["source"] == "json").all()
    assert len(df) == 2  # битая строка отброшена


def test_pipeline_syslog_contract(tmp_path):
    p = tmp_path / "demo.log"
    _write_syslog(p, [
        "<34>1 2025-01-02T03:04:05Z host1 sshd 1234 ID47 [x] Failed password",
        "не syslog",
    ])
    df = run_pipeline(str(p), "syslog")
    assert list(df.columns) == UNIFIED_COLUMNS
    assert str(df["timestamp"].dtype) == "datetime64[ns, UTC]"
    assert (df["source"] == "syslog").all()
    assert len(df) == 1


def test_pipeline_nat_for_bad_ts(tmp_path):
    p = tmp_path / "bad.jsonl"
    _write_jsonl(p, [
        '{"timestamp":"не-дата","user":"x","event_type":"y"}',
    ])
    df = run_pipeline(str(p), "json")
    assert pd.isna(df["timestamp"].iloc[0])
