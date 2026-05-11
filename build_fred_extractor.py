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
    API_KEY = '8204151785387f51d47f6a0f1c2f4bce'  
    
    macro_series = {
        # US Baseline Indicators
        "us_inflation": "CPIAUCSL",
        "us_interest_rate": "FEDFUNDS",
        "us_unemployment": "UNRATE",
        "us_yield_data": "GS10",
        "us_gdp": "GDPC1",
        "us_m2_money_supply": "M2SL",
        "us_consumer_sentiment": "UMCSENT",
        "us_nonfarm_payrolls": "PAYEMS",
        "us_retail_sales": "RSAFS",
        "us_housing_starts": "HOUST",
        "us_stock_market": "SP500", 
        
        # China Equivalent Indicators
        "china_inflation": "CHNCPIALLMINMEI", 
        "china_interest_rate": "INTDSRCNM193N", 
        "china_stock_market": "SPASTT01CNM661N", 
        
        # India Equivalent Indicators
        "india_inflation": "INDCPIALLMINMEI", 
        "india_interest_rate": "INTDSRINM193N", 
        "india_stock_market": "SPASTT01INM661N", 
        
        # Eurozone Equivalent Indicators
        "eurozone_inflation": "CP0000EZ19M086NES", 
        "eurozone_interest_rate": "IR3TIB01EZM156N", 
        "eurozone_stock_market": "SPASTT01EZM661N" 
    }
    
    raw_macro_data = {}
    print("Starting Global Comparison & Stock Market Extraction...")
    
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

    print(f"\nExtraction Complete! Global comparison data saved to: {output_filename}")

if __name__ == "__main__":
    main()