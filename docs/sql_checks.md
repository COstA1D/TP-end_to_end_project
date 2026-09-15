# SQL-проверки Week 5

Таблица:
`public.mart_variant_02_daily_weather`

## 1. Количество строк

```sql
SELECT COUNT(*) AS row_count
FROM public.mart_variant_02_daily_weather;
```

Ожидаемый результат: 7.

## 2. Диапазон дат

```sql
SELECT MIN(time), MAX(time)
FROM public.mart_variant_02_daily_weather;
```

Ожидаемый период: 2026-09-15 — 2026-09-21.

## 3. Проверка NULL

```sql
SELECT COUNT(*) AS null_rows
FROM public.mart_variant_02_daily_weather
WHERE time IS NULL
   OR temperature_avg IS NULL
   OR precipitation_total IS NULL
   OR observation_count IS NULL;
```

Ожидаемый результат: 0.

## 4. Проверка дублей

```sql
SELECT time, city_name, COUNT(*) AS duplicate_count
FROM public.mart_variant_02_daily_weather
GROUP BY time, city_name
HAVING COUNT(*) > 1;
```

Ожидаемый результат: пустой набор.

## 5. Проверка KPI

```sql
SELECT
    ROUND(AVG(temperature_avg)::numeric, 2) AS avg_temperature,
    ROUND(SUM(precipitation_total)::numeric, 2) AS total_precipitation,
    ROUND(MAX(wind_speed_max)::numeric, 2) AS max_wind
FROM public.mart_variant_02_daily_weather;
```

## 6. Проверка отрицательных значений

```sql
SELECT COUNT(*) AS invalid_rows
FROM public.mart_variant_02_daily_weather
WHERE precipitation_total < 0
   OR observation_count <= 0;
```

Ожидаемый результат: 0.

## 7. Проверка повторной загрузки

После повторного запуска `src/load.py`:

```sql
SELECT COUNT(*)
FROM public.mart_variant_02_daily_weather;
```

Ожидаемый результат: 7.