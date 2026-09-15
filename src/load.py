from pathlib import Path
import os

import pandas as pd
from sqlalchemy import create_engine, text


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MART_PATH = (
    PROJECT_ROOT
    / "data"
    / "mart"
    / "variant_02"
    / "mart_daily_weather.csv"
)

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "weather_db")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

TABLE_NAME = "mart_variant_02_daily_weather"


def main():
    if not MART_PATH.exists():
        raise FileNotFoundError(f"Mart not found: {MART_PATH}")

    df = pd.read_csv(MART_PATH)

    print(f"Mart path: {MART_PATH}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print("Dtypes:")
    print(df.dtypes)

    engine = create_engine(DATABASE_URL)

    with engine.begin() as conn:
        df.to_sql(
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

    print(f"Loaded rows: {count}")
    print(f"Table: public.{TABLE_NAME}")


if __name__ == "__main__":
    main()
