# Implementation Plan

## Week 1 goals
- Install Anaconda and verify that `conda` works.
- Create reproducible environment setup with `scripts/setup_env.bat`.
- Create base repository structure for the end-to-end data project.
- Add initial project documentation.

## Notes
Using `python -m pip install ...` is safer than plain `pip install`, because plain `pip` may point to another Python interpreter in the system PATH.

## Week 2 — Часть 0: наблюдения

Исходный файл `broken_requests.py` был запущен без таймаута,
проверки HTTP-статуса, обработки сетевых исключений и проверки JSON.

Наблюдаемый результат:
- запрос завершился успешно;
- программа вывела URL, полученный от API;
- программа ожидала ответ от задержанного endpoint;
- без timeout программа может долго блокироваться в ожидании сетевого ответа;
- без проверки JSON вызов `response.json()` может завершиться ошибкой.

Вывод:
HTTP-запросы должны использовать timeout, обработку сетевых ошибок,
проверку HTTP-статуса и безопасный разбор JSON.
