"""Download and save S&P 500 daily market data."""

from pathlib import Path

import pandas as pd
import yfinance as yf


REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def download_market_data(
    ticker: str,
    start_date: str | None = None,
    end_date: str | None = None,
    period: str = "10y",
    interval: str = "1d",
) -> pd.DataFrame:
    """Download OHLCV data and retain only the required columns."""
    if start_date:
        data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            interval=interval,
            auto_adjust=False,
            progress=False,
        )
    else:
        data = yf.download(
            ticker,
            period=period,
            interval=interval,
            auto_adjust=False,
            progress=False,
        )

    if data.empty:
        raise ValueError(f"No market data returned for ticker {ticker}")

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    missing = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing:
        raise ValueError(f"Downloaded data is missing columns: {missing}")

    return data.loc[:, REQUIRED_COLUMNS].copy()


def save_raw_data(data: pd.DataFrame, path: str | Path) -> None:
    """Save the original downloaded dataset."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path)
