"""Единый пайплайн: путь + тип источника → DataFrame унифицированной схемы."""
from __future__ import annotations

import pandas as pd

from parsers.json_parser import parse_json_line
from parsers.syslog_parser import parse_syslog_5424
from parsers.evtx_parser import parse_evtx

UNIFIED_COLUMNS = [
    "timestamp", "source", "user",
    "event_type", "severity", "raw",
]


def _parse_json_file(path: str) -> pd.DataFrame:
    rows: list[dict] = []
    skipped = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            rec = parse_json_line(line.strip())
            if rec:
                rows.append(rec)
            else:
                skipped += 1
    print(f"[json] разобрано {len(rows)}, пропущено {skipped}")
    return pd.DataFrame(rows, columns=UNIFIED_COLUMNS)


def _parse_syslog_file(path: str) -> pd.DataFrame:
    rows: list[dict] = []
    skipped = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            rec = parse_syslog_5424(line.strip())
            if rec:
                rows.append(rec)
            else:
                skipped += 1
    print(f"[syslog] разобрано {len(rows)}, пропущено {skipped}")
    return pd.DataFrame(rows, columns=UNIFIED_COLUMNS)


def _parse_evtx_file(path: str) -> pd.DataFrame:
    return parse_evtx(path)


def normalize_timestamp(
    df: pd.DataFrame, col: str = "timestamp"
) -> pd.DataFrame:
    """Приводит колонку timestamp к UTC timezone-aware datetime.

    errors='coerce' — нераспознанные строки становятся NaT, не падаем.
    """
    out = df.copy()
    out[col] = pd.to_datetime(out[col], utc=True, errors="coerce")
    return out


def run_pipeline(path: str, source_type: str) -> pd.DataFrame:
    """Единая точка входа: путь + тип источника → DataFrame.

    Args:
        path: путь к файлу лога.
        source_type: один из 'json', 'syslog', 'evtx'.

    Returns:
        DataFrame с колонками UNIFIED_COLUMNS, timestamp в UTC,
        source проштампован значением source_type.

    Raises:
        ValueError: если source_type неизвестен.
    """
    parsers = {
        "json": _parse_json_file,
        "syslog": _parse_syslog_file,
        "evtx": _parse_evtx_file,
    }
    if source_type not in parsers:
        raise ValueError(
            f"Неизвестный тип источника: {source_type!r}. "
            f"Допустимые: {list(parsers)}"
        )

    df_out = parsers[source_type](path)

    # Страховка контракта: добавляем пустые колонки, если парсер что-то не вернул
    for col in UNIFIED_COLUMNS:
        if col not in df_out.columns:
            df_out[col] = None

    df_out = df_out[UNIFIED_COLUMNS]
    df_out = normalize_timestamp(df_out)
    df_out["source"] = source_type
    return df_out
