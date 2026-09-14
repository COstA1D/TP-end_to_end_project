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

Наблюдаемые результаты:
- запрос к медленному endpoint был ограничен таймаутом в исправленной версии;
- HTTP-ответ со статусом 404 был обработан без аварийного завершения;
- HTML-ответ был распознан как невалидный JSON;
- корректный JSON был успешно прочитан;
- в исправленной версии программа выводит понятные сообщения вместо traceback.

Вывод:

HTTP-запросы должны использовать timeout, обработку сетевых ошибок,
проверку HTTP-статуса и безопасный разбор JSON.
