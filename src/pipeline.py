from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import os

import pandas as pd
from sqlalchemy import URL, create_engine, text


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "variant_02"
    / "2026-09-15_03-46-15.json"
)

TABLE_NAME = "mart_variant_02_daily_weather"
STATE_PATH = PROJECT_ROOT / "data" / "state.json"


def extract():
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Raw file not found: {RAW_PATH}")

    print(f"[extract] raw: {RAW_PATH}")
    return RAW_PATH


def transform():
    with RAW_PATH.open("r", encoding="utf-8") as file:
        raw = json.load(file)

    df = pd.DataFrame(raw["hourly"])
    df["time"] = pd.to_datetime(df["time"])

    normalized_dir = PROJECT_ROOT / "data" / "normalized"
    normalized_dir.mkdir(parents=True, exist_ok=True)

    normalized_path = normalized_dir / "weather_hourly_normalized.csv"
    df.to_csv(normalized_path, index=False, encoding="utf-8")

    df["city_id"] = "variant_02_location"
    df["city_name"] = "Исходная локация"
    df["source_type"] = "open-meteo"

    mart = (
        df.set_index("time")
        .resample("D")
        .agg(
            city_name=("city_name", "first"),
            source_type=("source_type", "first"),
            temperature_avg=("temperature_2m", "mean"),
            temperature_min=("temperature_2m", "min"),
            temperature_max=("temperature_2m", "max"),
            precipitation_total=("precipitation", "sum"),
            humidity_avg=("relative_humidity_2m", "mean"),
            wind_speed_avg=("wind_speed_10m", "mean"),
            wind_speed_max=("wind_speed_10m", "max"),
            observation_count=("temperature_2m", "count")
        )
        .reset_index()
    )

    mart["temperature_avg_3d_rolling"] = (
        mart["temperature_avg"]
        .rolling(3, min_periods=1)
        .mean()
    )

    mart["precipitation_3d_rolling"] = (
        mart["precipitation_total"]
        .rolling(3, min_periods=1)
        .sum()
    )

    numeric_columns = mart.select_dtypes(include="number").columns
    mart[numeric_columns] = mart[numeric_columns].round(2)

    mart_dir = PROJECT_ROOT / "data" / "mart" / "variant_02"
    mart_dir.mkdir(parents=True, exist_ok=True)

    mart_path = mart_dir / "mart_daily_weather.csv"
    mart.to_csv(mart_path, index=False, encoding="utf-8")

    print(f"[transform] normalized: {len(df)} rows")
    print(f"[transform] mart: {len(mart)} rows")

    return mart


def load(mart):
    db_user = os.getenv("POSTGRES_USER", "postgres")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = int(os.getenv("POSTGRES_PORT", "5432"))
    db_name = os.getenv("POSTGRES_DB", "weather_db")

    if not db_password:
        raise RuntimeError(
            "POSTGRES_PASSWORD is not set"
        )

    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_name
    )

    engine = create_engine(database_url)

    with engine.begin() as conn:
        mart.to_sql(
            TABLE_NAME,
            con=conn,
            schema="public",
            if_exists="replace",
            index=False,
            method="multi"
        )

        count = conn.execute(
            text(f'SELECT COUNT(*) FROM public."{TABLE_NAME}"')
        ).scalar_one()

    print(f"[load] rows: {count}")
    return count


def write_state(mode, mart):
    state = {
        "variant": "variant_02",
        "source_type": "open-meteo",
        "mode": mode,
        "watermark": str(mart["time"].max().date()),
        "last_raw_file": str(RAW_PATH.relative_to(PROJECT_ROOT)),
        "last_successful_run_utc": datetime.now(
            timezone.utc
        ).isoformat()
    }

    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with STATE_PATH.open("w", encoding="utf-8") as file:
        json.dump(state, file, ensure_ascii=False, indent=2)

    print(f"[state] watermark: {state['watermark']}")


def main():
    parser = argparse.ArgumentParser(
        description="Week 6 ETL pipeline"
    )

    parser.add_argument(
        "--mode",
        choices=["full", "incremental"],
        required=True
    )

    args = parser.parse_args()

    print(f"Pipeline started, mode={args.mode}")

    extract()
    mart = transform()
    row_count = load(mart)

    if row_count > 0:
        write_state(args.mode, mart)

    print("Pipeline completed successfully")


if __name__ == "__main__":
    main()
