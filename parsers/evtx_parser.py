"""Парсер Windows Event Log (EVTX) в унифицированную схему."""
from __future__ import annotations

import xml.etree.ElementTree as ET

import pandas as pd

NS = {"ns": "http://schemas.microsoft.com/win/2004/08/events/event"}

UNIFIED_COLUMNS = [
    "timestamp", "source", "user",
    "event_type", "severity", "raw",
]


def parse_evtx(path: str, max_records: int | None = None) -> pd.DataFrame:
    """Разбирает EVTX-файл в DataFrame с унифицированной схемой.

    Каждая запись обёрнута в try/except: одна битая запись
    не роняет разбор всего файла (в EVTX встречаются бинарные типы,
    которые python-evtx не умеет обрабатывать).

    Args:
        path: путь к .evtx-файлу.
        max_records: ограничение на число записей (для быстрой проверки).

    Returns:
        DataFrame с колонками UNIFIED_COLUMNS.

    Raises:
        ImportError: если не установлен python-evtx.
        FileNotFoundError: если файл не найден.
    """
    try:
        import Evtx.Evtx as evtx
    except ImportError as e:
        raise ImportError(
            "Установите python-evtx: pip install python-evtx"
        ) from e

    rows: list[dict] = []
    with evtx.Evtx(path) as log:
        for i, record in enumerate(log.records()):
            if max_records is not None and i >= max_records:
                break
            try:
                root = ET.fromstring(record.xml())
                eid = root.find(".//ns:EventID", NS)
                ts_el = root.find(".//ns:TimeCreated", NS)
                data = {
                    x.get("Name", ""): x.text
                    for x in root.findall(".//ns:Data", NS)
                }
                rows.append({
                    "timestamp": ts_el.get("SystemTime") if ts_el is not None else None,
                    "source": "evtx",
                    "user": data.get("SubjectUserName", ""),
                    "event_type": f"EventID_{eid.text}" if eid is not None else "",
                    "severity": "",
                    "raw": record.xml()[:500],
                })
            except Exception:
                continue  # плохая запись — пропускаем

    return pd.DataFrame(rows, columns=UNIFIED_COLUMNS)
