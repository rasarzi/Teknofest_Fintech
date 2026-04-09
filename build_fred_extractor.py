import requests
import json

def fetch_fred_data(series_id, api_key):
    """Fetches historical observations for a given series from FRED API."""
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return {obs['date']: obs['value'] for obs in data['observations']}
    except Exception as err:
        print(f"An error occurred for {series_id}: {err}")
    return None

def main():
    # --- ENTER YOUR FRED API KEY HERE ---
    API_KEY = '8204151785387f51d47f6a0f1c2f4bce'  # Make sure to paste your real key back in!
    
    # Expanded Macro Indicators for AI Agent
    macro_series = {
        # Core Indicators (Original)
        "inflation": "CPIAUCSL",
        "interest_rate": "FEDFUNDS",
        "unemployment": "UNRATE",
        "yield_data": "GS10",
        
        # Advanced Indicators (New)
        "gdp": "GDPC1",                 # Real Gross Domestic Product (Economic Health)
        "m2_money_supply": "M2SL",      # M2 Money Supply (Market Liquidity)
        "consumer_sentiment": "UMCSENT",# Univ. of Michigan Consumer Sentiment (Psychology)
        "nonfarm_payrolls": "PAYEMS",   # Total Nonfarm Payrolls (Labor Market)
        "retail_sales": "RSAFS",        # Retail Sales (Consumer Spending)
        "housing_starts": "HOUST"       # Housing Starts (Real Estate health)
    }
    
    raw_macro_data = {}
    print("Starting Comprehensive Data Extraction for P8...")
    
    for label, series_id in macro_series.items():
        print(f"Fetching {label} ({series_id})...")
        series_data = fetch_fred_data(series_id, API_KEY)
        
        if series_data:
            raw_macro_data[label] = series_data
        else:
            print(f"Skipping {label} due to error.")

    output_filename = 'raw_macro.json'
    with open(output_filename, 'w') as f:
        json.dump(raw_macro_data, f, indent=4)

    print(f"\nTask P8 & P9 Complete. Expanded data saved to: {output_filename}")

if __name__ == "__main__":
    main()