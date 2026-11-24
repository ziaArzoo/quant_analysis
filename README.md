# quant_analysis

S&P 500 volatility strategy research system.

## Setup

```bash
uv sync
```

Configure the research parameters in `config/settings.yaml`, then run:

```bash
uv run python main.py
```

The application downloads S&P 500 daily OHLCV data when processed data is not
present. Set `start_date` and `end_date` in the configuration to use an explicit
date range; otherwise, the default 10-year period is downloaded.

Volatility research modules are organized below
`src/quant_analysis/volatility_research/`. Future research areas should be added
as separate subpackages below `src/quant_analysis/` rather than beside the
top-level package.
