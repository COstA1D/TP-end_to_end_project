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

## Week 3 — Часть 0: диагностика Pandas

В исходной версии `broken_pandas_read.py` не был указан разделитель CSV.

Файл использовал разделитель `;`, а `pandas.read_csv()` по умолчанию ожидал запятую. В результате весь CSV был прочитан как один столбец, поэтому обращение к `df["value"]` завершилось ошибкой `KeyError`.

После добавления `sep=";"`:
- таблица стала состоять из двух столбцов: `id` и `value`;
- значения были распознаны как числовые;
- среднее значение `value` составило `20.0`;
- пропуск в `value` был представлен как `NaN`;
- среднее рассчитывалось без учёта пропущенного значения.

Вывод: после чтения данных необходимо проверять `head()`, `columns`, `dtypes` и `shape`.
