# TEKNOFEST Fintech — Market Data & Insights Pipeline

A Python prototype for **macroeconomic and equity market data engineering**. It retrieves public time-series data, cleans and normalizes it, generates technical and macroeconomic features, and produces interpretable JSON summaries. An **optional** Gemini step provides a descriptive macro briefing.

> **Scope:** Financial analytics prototype, not a trading execution system, investment recommendation engine, or trained return-prediction model. Do not use outputs as investment advice.

## Features

- **Macroeconomic data:** US, China, India, and euro-area indicator series from the FRED API.
- **Equity data:** Five years of OHLCV daily prices for AAPL, MSFT and SPY using `yfinance`.
- **Feature engineering:** SMAs (20/50 days), 20-day close-price standard deviation, 20-day momentum, 14-day RSI, running-peak drawdown, US yield spread, indicator trends and heuristic market regimes.
- **Insights:** deterministic per-ticker summaries and an optional Gemini-generated descriptive macro narrative.
- **Security:** API keys are read from environment variables, never committed to the source code.

## Architecture

```text
FRED → raw_macro.json → clean_macro.json → structured_macro.json
     → macro_features.json → [optional Gemini] → macro_insight.json

yfinance → raw_stock.json → clean_stock.json → structured_stock.json
         → stock_features.json → stock_insight.json
```

## Quick start

Requires Python 3.10+ (recommended), internet access for live data downloads, and the packages in `requirements.txt`.

```bash
python -m venv .venv
# macOS / Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**Stock pipeline (no API key required):**

```bash
python run_pipeline.py stock
```

**Macro pipeline:** Obtain your own FRED API key and set `FRED_API_KEY` in your terminal environment (or use a local `.env` file loaded into the environment by your own tooling). Do **not** commit real `.env` files.

```bash
# macOS / Linux
export FRED_API_KEY="your-own-key"
python run_pipeline.py macro
```

For Gemini narrative generation, additionally set `GEMINI_API_KEY`, then run:

```bash
python run_pipeline.py macro --with-ai
```

Windows PowerShell environment variable example: `$env:FRED_API_KEY = "your-own-key"`. `.env.example` contains **placeholders only**. The scripts deliberately do not auto-load `.env`.

To run individual stages, inspect `run_pipeline.py` for the correct execution order. Generated JSON files are excluded from Git to keep the repository compact and avoid accidentally sharing local data.

## Project structure

| File | Purpose |
| --- | --- |
| `build_fred_extractor.py` | Fetch FRED macroeconomic series |
| `raw_stock.py` | Fetch historical prices from Yahoo Finance via yfinance |
| `clean_*_data.py` | Sort and fill missing values using past observations |
| `standardize_*_schema.py` | Convert datasets into record-oriented structures |
| `build_macro_features.py` | Compute US spread/trends and macro regimes |
| `compute_technical_features.py` | Calculate stock technical indicators |
| `create_stock_insight.py` | Build rule-based stock summaries |
| `create_macro_insight.py` | Generate an optional Gemini summary |
| `run_pipeline.py` | Run each pipeline in dependency order |
| `tests/` | Synthetic offline tests |

## Data integrity and limitations

The processing avoids **future-value backfilling** in historical features, leaves unavailable rolling-window indicators as `null`, and bases spread/regime calculations on consistent US-prefixed indicator fields. Nevertheless, the macro series contain **mixed frequencies and publication delays**: forward-filling is only a simplistic alignment and is not point-in-time release-calendar accurate. A 30-observation rolling average is not necessarily a 30-calendar-day average. `volatility_20d` represents the rolling standard deviation of **price levels**, not returns or annualized volatility.

Gemini output may be incomplete or inaccurate, and model access/costs vary. The stock insight generator is **rule-based**, not LLM-generated. No forecasting performance, trading strategy, backtest or risk-adjusted returns are claimed.

## Tests

```bash
python -m unittest discover -s tests -v
```

These tests run on synthetic local fixtures and do not require real API credentials. Live API calls are not exercised by the tests.

## Security and publishing

The uploaded source contained embedded FRED and Gemini API credentials. This version **does not include those values**; `.gitignore` excludes `.env`, local Python environments, and generated output. **Rotate/revoke the old keys even if this ZIP is clean.** If the keys were already pushed to GitHub, deleting them from a new commit does not erase them from Git history—remove them from history and treat them as compromised. Push this as a new clean repository if you cannot verify existing history.

## License

No license is included. Add a license only after confirming ownership and third-party redistribution permissions.
