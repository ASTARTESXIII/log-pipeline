# log-pipeline — парсинг логов ИБ в единую схему

Командная часть ДЗ к лекции «Pandas для анализа логов: от простого к продвинутому».

## Состав команды и роли

| Роль | Участник | Артефакт |
|---|---|---|
| JSON-лид | Каиров Д.А. | `parsers/json_parser.py`, `tests/test_json.py`, сборка пайплайна |
| Syslog | Ольков А.В. | `parsers/syslog_parser.py`, `tests/test_syslog.py` |
| EVTX | Шняк О.И. | `parsers/evtx_parser.py`, `tests/test_evtx.py` |

## Установка

```bash
pip install -r requirements.txt
```

## Запуск тестов

```bash
pytest tests/ -v
```
*(На текущий момент все 18 тестов проходят успешно).*

## Использование пайплайна

```python
from pipeline import run_pipeline

df = run_pipeline("data/cloudtrail.json", "json")
print(df.shape, df.dtypes)
```

Все парсеры возвращают единый контракт колонок:

| Колонка | Что содержит |
|---|---|
| `timestamp` | Время события (UTC, timezone-aware) |
| `source` | Тип источника: `"json"`, `"syslog"`, `"evtx"` |
| `user` | Пользователь (если есть) |
| `event_type` | Тип события |
| `severity` | Важность |
| `raw` | Исходная строка (для отладки) |

## Источники данных

- **EVTX** — [sbousseaden/EVTX-ATTACK-SAMPLES](https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES) (Meterpreter, `Exec_sysmon_meterpreter_reversetcp_msipackage.evtx`)
- **Syslog** — [SoftManiaTech/sample_log_files](https://github.com/SoftManiaTech/sample_log_files) (Linux / OpenSSH) или `/var/log/syslog`
- **JSON** — [splunk/attack_data](https://github.com/splunk/attack_data) `T1110.003/aws_multiple_login_fail_per_user/cloudtrail.json` или [Suricata eve.json](https://github.com/FrankHassanabad/suricata-sample-data)

Подробнее — в `data/README.md`.

## Пример вывода на трёх реальных файлах

### JSON (CloudTrail)
```
[json] разобрано 28, пропущено 0
shape: (28, 6)
timestamp                  source  user                        event_type     severity  raw
2022-10-19 20:33:38+00:00  json    HIDDEN_DUE_TO_SECURITY...   ConsoleLogin   ""        {"eventVersion":...
...
```

### Syslog (RFC 5424)
```
[syslog] разобрано 2, пропущено 1
shape: (2, 6)
timestamp                  source  user  event_type  severity  raw
2025-01-02 03:04:05.123+00:00 syslog      sshd        34        <34>1 ...
2025-01-02 03:04:06.200+00:00 syslog      sshd        34        <34>1 ...
```

### EVTX (Security.evtx)
```
shape: (8, 6)
timestamp                        source  user  event_type     severity  raw
2019-04-30 22:48:58.901474+00:00  evtx          EventID_2                <Event xmlns="...
2019-04-30 22:48:59.260851+00:00  evtx          EventID_1                <Event xmlns="...
...
```

## Известные ограничения

- Syslog RFC 3164: год в timestamp отсутствует — `normalize_timestamp` поставит `NaT`.
- EVTX: бинарные типы, которые `python-evtx` не умеет обрабатывать, пропускаются.
- `raw` для EVTX обрезается до 500 символов (экономия памяти).

## Запуск demo.ipynb

```bash
jupyter notebook demo.ipynb
```

Ноутбук прогоняется сверху вниз без ошибок: скачивает демо-данные, показывает блоки 1.1–1.3, прогоняет пайплайн на трёх файлах, запускает контрольный пример и юнит-тесты.