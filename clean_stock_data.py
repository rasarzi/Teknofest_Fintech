import pandas as pd
import json

def clean_stocks(input_file, output_file):
    print(f"Loading {input_file} for P16...")
    
    with open(input_file, 'r') as f:
        raw_data = json.load(f)

    cleaned_data = {}
    
    # Process each ticker one by one
    for ticker, dates_data in raw_data.items():
        df = pd.DataFrame.from_dict(dates_data, orient='index')
        
        if not df.empty:
            # Standardize date format
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            
            # Fill missing gaps (forward fill, then backward fill just in case)
            df = df.ffill().bfill()
            
            # Revert index back to string for JSON storage
            df.index = df.index.strftime('%Y-%m-%d')
            cleaned_data[ticker] = df.to_dict(orient='index')

    with open(output_file, 'w') as f:
        json.dump(cleaned_data, f, indent=4)
        
    print(f"Task P16 Complete. Saved clean data to {output_file}")

if __name__ == "__main__":
    clean_stocks('raw_stock.json', 'clean_stock.json')