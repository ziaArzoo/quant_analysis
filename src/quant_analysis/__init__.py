from .volatility_research.features.volatility import (
    annualized_volatility,
    log_returns,
    rolling_volatility,
    simple_returns,
)


def main() -> None:
    print("Hello from quant-analysis!")


__all__ = [
    "annualized_volatility",
    "log_returns",
    "rolling_volatility",
    "simple_returns",
]
