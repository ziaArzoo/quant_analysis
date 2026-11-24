"""Configuration validation helpers."""

from collections.abc import Mapping


def validate_settings(settings: Mapping[str, object]) -> None:
    """Validate required top-level Phase 1 settings."""
    required = {
        "ticker",
        "period",
        "interval",
        "raw_data_path",
        "processed_data_path",
    }
    missing = required.difference(settings)
    if missing:
        raise ValueError(f"Missing configuration keys: {sorted(missing)}")

    period = settings["period"]
    if not isinstance(period, str) or not period:
        raise ValueError("period must be a non-empty string")
