"""Пакет парсеров логов в унифицированную схему события ИБ."""
from .json_parser import parse_json_line
from .syslog_parser import parse_syslog_5424, parse_syslog_3164
from .evtx_parser import parse_evtx

__all__ = [
    "parse_json_line",
    "parse_syslog_5424",
    "parse_syslog_3164",
    "parse_evtx",
]
