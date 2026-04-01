import requests
import json

def fetch_fred_data(series_id, api_key):
    """
    Fetches historical data for a specific series from the FRED API.
    """
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json"
    }
    
    try:
        response = requests.get(url, params=params)
        # Raise an exception if the request was unsuccessful (e.g., 404, 401, 500)
        response.raise_for_status()
        
        data = response.json()
        # Extract just the date and value for a cleaner dictionary
        return {obs['date']: obs['value'] for obs in data['observations']}
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {series_id}: {e}")
        return None

def main():
    # --- INSERT YOUR API KEY HERE ---
    API_KEY = '8204151785387f51d47f6a0f1c2f4bce'
    
    # Common FRED Series IDs:
    # CPIAUCSL = Inflation (CPI)
    # FEDFUNDS = Interest Rates (Federal Funds Effective Rate)
    # UNRATE   = Unemployment Rate
    # GS10     = 10-Year Treasury Constant Maturity Rate
    
    macro_series = {
        "inflation": "CPIAUCSL",
        "interest_rates": "FEDFUNDS",
        "unemployment": "UNRATE",
        "treasury_yields": "GS10"
    }
    
    final_macro_data = {}

    for name, series_id in macro_series.items():
        print(f"Fetching {name} data...")
        data = fetch_fred_data(series_id, API_KEY)
        if data:
            final_macro_data[name] = data

    # Save the structured dictionary to a JSON file
    output_filename = 'raw_macro.json'
    with open(output_filename, 'w') as f:
        json.dump(final_macro_data, f, indent=4)

    print(f"\nSuccess! Data saved to {output_filename}")

if __name__ == "__main__":
    main()