"""Юнит-тесты парсера EVTX.

Тесты не требуют реального .evtx-файла: проверяем контракт
и поведение на отсутствующем файле.
"""
import os

import pandas as pd
import pytest

from parsers.evtx_parser import parse_evtx, UNIFIED_COLUMNS


def test_evtx_importable():
    # Модуль импортируется и функция доступна
    assert callable(parse_evtx)


def test_evtx_columns_contract():
    # Проверяем, что контракт колонок задан
    assert UNIFIED_COLUMNS == [
        "timestamp", "source", "user",
        "event_type", "severity", "raw",
    ]


def test_evtx_missing_file_raises():
    # Несуществующий файл → исключение (FileNotFoundError или подобное)
    with pytest.raises(Exception):
        parse_evtx("nonexistent_file_12345.evtx")


@pytest.mark.skipif(
    not os.path.exists("sample.evtx"),
    reason="sample.evtx отсутствует — реальный файл не скачан",
)
def test_evtx_real_file():
    # Если sample.evtx есть — проверяем контракт на реальных данных
    df = parse_evtx("sample.evtx", max_records=5)
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == UNIFIED_COLUMNS
    assert len(df) <= 5
