import pandas as pd
import json

def clean_macro_data(input_file, output_file):
    """
    Cleans raw macro data: standardizes dates, sets the index, 
    and handles missing values via forward-fill.
    """
    print(f"Loading {input_file}...")
    
    with open(input_file, 'r') as f:
        raw_data = json.load(f)
    
    # Convert the nested dictionary into a Pandas DataFrame
    # This aligns the dates from different series into a single table
    df = pd.DataFrame.from_dict(raw_data)
    
    # 1. Convert the index to a standardized 'YYYY-MM-DD' datetime format
    df.index = pd.to_datetime(df.index)
    
    # Sort the index to ensure data is in chronological order before filling
    df = df.sort_index()
    
    # 2. Handling missing values using forward-fill (ffill)
    # This is crucial because some data is monthly (Inflation) 
    # while others might be daily (Yields).
    df = df.ffill()
    
    # Optional: If there are still NaNs at the very beginning, use backfill
    df = df.bfill()
    
    # 3. Format the final output
    # Convert the index back to strings for JSON compatibility
    df.index = df.index.strftime('%Y-%m-%d')
    
    # Convert back to a dictionary and save
    clean_dict = df.to_dict(orient='index')
    
    with open(output_file, 'w') as f:
        json.dump(clean_dict, f, indent=4)
        
    print(f"Success! Cleaned data saved to {output_file}")

if __name__ == "__main__":
    # Task P10 configuration
    input_fn = 'raw_macro.json'
    output_fn = 'clean_macro.json'
    
    try:
        clean_macro_data(input_fn, output_fn)
    except FileNotFoundError:
        print(f"Error: Could not find {input_fn}. Did you run P8/P9 first?")