"""Volatility calculations for financial return series."""

from math import isfinite, log, sqrt
from statistics import stdev
from typing import Iterable, Sequence


def _finite_values(values: Iterable[float]) -> list[float]:
    result = list(values)
    if not result:
        raise ValueError("At least one value is required")
    if not all(isfinite(value) for value in result):
        raise ValueError("Values must be finite")
    return result


def simple_returns(prices: Sequence[float]) -> list[float]:
    """Calculate simple percentage returns from a sequence of prices."""
    prices = _finite_values(prices)
    if len(prices) < 2:
        raise ValueError("At least two prices are required")
    if any(price <= 0 for price in prices):
        raise ValueError("Prices must be positive")

    return [
        (current / previous) - 1.0
        for previous, current in zip(prices, prices[1:])
    ]


def log_returns(prices: Sequence[float]) -> list[float]:
    """Calculate continuously compounded returns from a sequence of prices."""
    prices = _finite_values(prices)
    if len(prices) < 2:
        raise ValueError("At least two prices are required")
    if any(price <= 0 for price in prices):
        raise ValueError("Prices must be positive")

    return [
        log(current / previous)
        for previous, current in zip(prices, prices[1:])
    ]


def annualized_volatility(
    returns: Sequence[float],
    periods_per_year: int = 252,
) -> float:
    """Calculate sample volatility annualized over a full year."""
    returns = _finite_values(returns)
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive")
    if len(returns) < 2:
        raise ValueError("At least two returns are required")

    return stdev(returns) * sqrt(periods_per_year)


def rolling_volatility(
    returns: Sequence[float],
    window: int = 20,
    periods_per_year: int = 252,
) -> list[float | None]:
    """Calculate annualized sample volatility over each rolling return window."""
    returns = _finite_values(returns)
    if window < 2:
        raise ValueError("window must be at least 2")
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive")

    result: list[float | None] = [None] * (window - 1)
    for end in range(window, len(returns) + 1):
        sample = returns[end - window:end]
        result.append(stdev(sample) * sqrt(periods_per_year))
    return result
