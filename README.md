Teknofest Fintech — Financial Data & Market Insights Pipeline
A Python-based financial data processing prototype that gathers macroeconomic indicators and historical stock prices, cleans and standardizes the datasets, engineers quantitative features, and produces machine-readable summaries for downstream market analysis. The macroeconomic branch includes an experimental Google Gemini text-generation step.
Status: This repository contains individual data pipeline scripts and example JSON outputs. It is not a complete trading platform, trained price-prediction model, or validated investment recommendation system.

What It Does
The project has two workflows:

Macroeconomic analysis
- Pulls economic series from the Federal Reserve Economic Data (FRED) API, including US indicators and selected China, India, and euro-area series.
- Cleans, aligns, and standardizes time-series data.
- Computes rolling trends and heuristic macro-regime descriptions.
- Optionally generates a narrative briefing using the Gemini API.
Stock-market analysis
- Downloads five years of daily OHLCV data for AAPL, MSFT, and the SPY benchmark via yfinance (these are the tickers configured in the current script).
- Cleans and restructures price data into per-date records.
- Derives technical indicators: 20-day and 50-day simple moving averages, 20-day rolling volatility, 20-day momentum, 14-day RSI, and drawdown from the running peak.
- Creates per-ticker text summaries and metric snapshots in JSON.
Technology
- Python (the archive includes a Python 3.9 virtual environment, but it should not be reused)
- pandas, NumPy — time-series transformation and technical features
- requests — FRED API requests
- yfinance — historical stock-market prices
- google-genai — Gemini API integration
- JSON — intermediate datasets and output artifacts
Pipeline Architecture
FRED API
  └── build_fred_extractor.py  → raw_macro.json
      └── clean_macro_data.py → clean_macro.json
          └── standardize_macro_schema.py → structured_macro.json
              └── build_macro_features.py → macro_features.json
                  └── create_macro_insight.py → macro_insight.json

yfinance (AAPL, MSFT, SPY)
  └── raw_stock.py → raw_stock.json
      └── clean_stock_data.py → clean_stock.json
          └── standardize_stock_schema.py → structured_stock.json
              └── compute_technical_features.py → stock_features.json
                  └── create_stock_insight.py → stock_insight.json
build_structure.py also creates project_structure/{raw,clean,structured,feature,insight}/ placeholder directories, though the actual pipeline scripts currently write JSON files to the repository root.
Getting Started
1. Create a clean Python environment
Run the following commands in the project directory (do not depend on the bundled .venv, which contains platform-specific binaries):
python -m venv .venv
Activate it:
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
Install the packages imported by the scripts:
python -m pip install pandas numpy requests yfinance google-genai
The archive does not contain a maintained requirements.txt or pyproject.toml, so these dependencies are inferred directly from imports.
2. Protect and configure credentials
Security action required before publishing or using this repository: Both build_fred_extractor.py and create_macro_insight.py contain API keys directly embedded in source code. Revoke/rotate those exposed keys, remove them from code and Git history as appropriate, and replace them with environment variables.

For example, update the FRED script to use:
import os
API_KEY = os.environ["FRED_API_KEY"]
And the Gemini script to use:
import os
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
Set FRED_API_KEY and GEMINI_API_KEY in your environment before running the corresponding scripts. These replacements are recommended edits; the supplied scripts do not yet read environment variables.
3. Run the stock workflow
From the project root:
python raw_stock.py
python clean_stock_data.py
python standardize_stock_schema.py
python compute_technical_features.py
python create_stock_insight.py
The resulting stock_insight.json contains the latest analyzed date, a text summary, and raw technical metrics for each ticker.
4. Run the macro workflow
After configuring and rotating the required API credentials:
python build_fred_extractor.py
python clean_macro_data.py
python standardize_macro_schema.py
python build_macro_features.py
python create_macro_insight.py
The final macro step calls an external Gemini model and may incur API charges or fail if the configured model is unavailable.
Existing Outputs
The uploaded archive includes example JSON files for all main data stages, including raw_macro.json, macro_features.json, macro_insight.json, raw_stock.json, stock_features.json, and stock_insight.json. These are saved outputs, not evidence that the entire pipeline has been executed successfully in a clean environment.
Known Limitations
- Macro indicator naming mismatch: The FRED extractor produces keys such as us_inflation and us_interest_rate, whereas some macro feature logic checks for the unprefixed names inflation, interest_rate, and yield_data. Consequently, certain spread, direction, and regime features may not be computed as intended without a consistent naming/mapping strategy.
- Mixed-frequency series: The pipeline forward/backward fills observations from different reporting frequencies; results should be interpreted carefully, especially around early dates and releases.
- Backfilling rolling indicators: The technical-feature script uses backfill after rolling calculations, which can introduce future-data leakage into historical feature rows. Avoid this in backtesting or predictive models.
- Stock summaries are rule-based: create_stock_insight.py builds text from indicator values; it does not call an LLM despite naming one field llm_system_context.
- Macro narrative is prompt-dependent: The Gemini prompt includes a strongly prescriptive sample narrative. Generated commentary should not be assumed to reflect neutral, independently validated investment analysis.
- No application UI, portfolio execution, tests, CI checks, or end-to-end model evaluation appears in the supplied project source.
- The archived .venv should be removed from version control and recreated locally.
Responsible Use
This repository is an educational/prototype financial analytics workflow. Market data can be incomplete or revised; computed indicators and generated narratives are not financial advice. Verify sources, timestamps, feature integrity, and backtest methodology before using results for decisions.
License
No license file was included in the supplied archive. Confirm permissions and third-party API terms before redistributing or deploying the project.
