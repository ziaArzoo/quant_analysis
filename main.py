"""Entry point for the volatility research pipeline."""

from pathlib import Path

import yaml

from quant_analysis.volatility_research.data.downloader import (
    download_market_data,
    save_raw_data,
)
from quant_analysis.volatility_research.data.loader import load_csv
from quant_analysis.volatility_research.data.preprocessing import preprocess_ohlcv
from quant_analysis.volatility_research.utils.logger import get_logger
from quant_analysis.volatility_research.utils.validation import validate_settings


def load_config(path: str | Path = "config/settings.yaml") -> dict:
    """Load YAML application settings."""
    with Path(path).open("r", encoding="utf-8") as config_file:
        settings = yaml.safe_load(config_file)
    if not isinstance(settings, dict):
        raise ValueError("Configuration must contain a YAML mapping")
    validate_settings(settings)
    return settings


def main() -> None:
    """Execute the Phase 1 data pipeline."""
    logger = get_logger()
    settings = load_config()

    raw_path = Path(settings["raw_data_path"])
    processed_path = Path(settings["processed_data_path"])

    if processed_path.is_file():
        logger.info("Loading existing processed data from %s", processed_path)
        market_data = load_csv(processed_path)
    else:
        logger.info("Downloading %s data", settings["ticker"])
        market_data = download_market_data(
            ticker=str(settings["ticker"]),
            start_date=settings.get("start_date"),
            end_date=settings.get("end_date"),
            period=str(settings["period"]),
            interval=str(settings["interval"]),
        )
        save_raw_data(market_data, raw_path)
        market_data, warnings = preprocess_ohlcv(market_data)
        processed_path.parent.mkdir(parents=True, exist_ok=True)
        market_data.to_csv(processed_path)
        for warning in warnings:
            logger.warning(warning)

    logger.info("Loaded %d observations", len(market_data))


if __name__ == "__main__":
    main()
