import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_config(config_path: Path) -> dict[str, Any]:
    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError("Configuration must contain a YAML mapping.")

    return config


def build_request(config: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
    api = config["api"]
    method = str(api["method"]).upper()
    base_url = str(api["base_url"])
    request_template = str(api.get("request_template", ""))

    url = f"{base_url}{request_template}"
    params = api.get("params", {})

    if not isinstance(params, dict):
        raise ValueError("api.params must be a mapping.")

    return method, url, params


def save_raw_json(data: Any, variant_id: str) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = PROJECT_ROOT / "data" / "raw" / f"variant_{variant_id}"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{timestamp}.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    return output_path


def extract(config_path: Path, timeout_sec: int = 10) -> Path:
    config = load_config(config_path)

    variant_id = str(config["variant_id"])
    source_type = str(config["source_type"])
    method, url, params = build_request(config)

    if method != "GET":
        raise ValueError(f"Week 2 supports GET requests only, received: {method}")

    try:
        response = requests.get(
            url,
            params=params,
            timeout=timeout_sec,
        )
    except requests.exceptions.Timeout as error:
        raise RuntimeError(
            f"Request timed out after {timeout_sec} seconds."
        ) from error
    except requests.exceptions.RequestException as error:
        raise RuntimeError(f"Network request failed: {error}") from error

    if not response.ok:
        raise RuntimeError(
            f"HTTP request failed: status_code={response.status_code}, "
            f"url={response.url}"
        )

    try:
        data = response.json()
    except ValueError as error:
        raise RuntimeError(
            f"API response is not valid JSON: {response.url}"
        ) from error

    output_path = save_raw_json(data, variant_id)

    if isinstance(data, dict):
        data_size = len(data)
    elif isinstance(data, list):
        data_size = len(data)
    else:
        data_size = 1

    print(f"[INFO] Variant: {variant_id}")
    print(f"[INFO] Source: {source_type}")
    print(f"[INFO] URL: {response.url}")
    print(f"[INFO] Status: {response.status_code}")
    print(f"[INFO] Saved to: {output_path}")
    print(f"[INFO] Top-level data size: {data_size}")

    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract raw JSON data from the configured API."
    )
    parser.add_argument(
        "--config",
        default="configs/variant_02.yml",
        help="Path to YAML configuration.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="HTTP timeout in seconds.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = PROJECT_ROOT / args.config

    try:
        extract(config_path=config_path, timeout_sec=args.timeout)
    except (OSError, KeyError, TypeError, ValueError, RuntimeError) as error:
        print(f"[ERROR] {error}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
