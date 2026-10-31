# Данные

Файлы данных не коммитятся в репозиторий (кроме demo-файлов) — качаются скриптом в `demo.ipynb`.

## JSON — CloudTrail (password spraying)

- Источник: https://github.com/splunk/attack_data
- Путь: `datasets/attack_techniques/T1110.003/aws_multiple_login_fail_per_user/cloudtrail.json`
- Формат: JSON Lines, вложенный `userIdentity.userName`.

## Syslog — RFC 5424

- Источник 1: https://github.com/SoftManiaTech/sample_log_files (раздел Linux / OpenSSH)
- Источник 2: `/var/log/syslog` на любой Linux-машине / WSL
- Формат: строки RFC 5424 (`<34>1 2025-01-02T03:04:05Z host1 sshd ...`).

## EVTX — Windows Event Log

- Источник: https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES
- Файл: `Execution/Exec_sysmon_meterpreter_reversetcp_msipackage.evtx`
- Формат: бинарный .evtx, разбирается через `python-evtx`.
