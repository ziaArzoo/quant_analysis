"""Load market data from local CSV files."""

from pathlib import Path

import pandas as pd


def load_csv(path: str | Path) -> pd.DataFrame:
    """Load a market-data CSV using its date index."""
    input_path = Path(path)
    if not input_path.is_file():
        raise FileNotFoundError(f"Market data file not found: {input_path}")

    data = pd.read_csv(input_path, index_col=0, parse_dates=True)
    data.index.name = "Date"
    return data
