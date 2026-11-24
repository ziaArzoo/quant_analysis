"""Validation and preprocessing for OHLCV market data."""

import pandas as pd


REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def validate_ohlcv(data: pd.DataFrame) -> list[str]:
    """Validate a market-data frame and return a list of warnings."""
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    warnings: list[str] = []
    if data.index.has_duplicates:
        warnings.append("Duplicate dates found")

    numeric = data.loc[:, REQUIRED_COLUMNS].apply(pd.to_numeric, errors="coerce")
    if numeric.isna().any().any():
        missing_counts = numeric.isna().sum()
        warnings.append(
            "Missing values found: "
            + ", ".join(
                f"{column}={count}"
                for column, count in missing_counts.items()
                if count
            )
        )

    invalid_ohlc = (
        (numeric["High"] < numeric["Low"])
        | (numeric["High"] < numeric["Open"])
        | (numeric["High"] < numeric["Close"])
        | (numeric["Low"] > numeric["Open"])
        | (numeric["Low"] > numeric["Close"])
    )
    if invalid_ohlc.any():
        raise ValueError("Invalid OHLC relationships found")

    if numeric["Volume"].isna().all():
        warnings.append(
            "Volume is unavailable; S&P 500 index volume is unsuitable "
            "for trade-volume analysis"
        )

    return warnings


def preprocess_ohlcv(data: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Sort, de-duplicate, and clean OHLCV observations."""
    if not isinstance(data.index, pd.DatetimeIndex):
        data = data.copy()
        data.index = pd.to_datetime(data.index)

    result = data.copy()
    result = result[~result.index.duplicated(keep="last")]
    result = result.sort_index()
    result = result.loc[:, REQUIRED_COLUMNS].apply(pd.to_numeric, errors="coerce")

    warnings = validate_ohlcv(result)
    if result.index.duplicated().any():
        raise ValueError("Duplicate dates remain after preprocessing")

    # Preserve missing market prices: do not forward-fill or interpolate prices.
    return result, warnings
