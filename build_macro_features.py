import pandas as pd
import json

def build_features(input_file, output_file):
    print(f"Loading {input_file} for P12 Feature Engineering (Expanded)...")
    
    with open(input_file, 'r') as f:
        data = json.load(f)
        
    df = pd.DataFrame(data)
    df = df.pivot(index='date', columns='indicator', values='value')
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # Force numeric and fill gaps
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.ffill()

    # 1. Spreads
    if 'us_yield_data' in df.columns and 'us_interest_rate' in df.columns:
        df['yield_spread'] = df['us_yield_data'] - df['us_interest_rate']
    
    # 2. Dynamic Trends (Automatically calculates 30-day moving average for ALL indicators)
    for col in df.columns:
        if col != 'yield_spread':
            df[f'{col}_trend_30d'] = df[col].rolling(window=30).mean()

    # 3. Directions
    if 'us_interest_rate' in df.columns:
        diff = df['us_interest_rate'].diff(periods=30)
        df['rate_direction'] = diff.map(lambda x: 'Rising' if x > 0 else ('Falling' if x < 0 else ('Flat' if pd.notna(x) else 'Unknown')))
    if 'us_inflation' in df.columns:
        diff = df['us_inflation'].diff(periods=30)
        df['inflation_direction'] = diff.map(lambda x: 'Rising' if x > 0 else ('Falling' if x < 0 else ('Flat' if pd.notna(x) else 'Unknown')))

    # 4. Regime Signals
    def determine_regime(row):
        rate = row.get('rate_direction', 'Unknown')
        infl = row.get('inflation_direction', 'Unknown')
        if rate == "Unknown" or infl == "Unknown": return "Insufficient data"
        if rate == "Rising" and infl == "Rising": return "Overheating / Tightening"
        if rate == "Falling" and infl == "Falling": return "Cooling / Easing"
        if rate == "Rising" and infl == "Falling": return "Restrictive"
        return "Transitional"

    df['macro_regime'] = df.apply(determine_regime, axis=1)

    # Clean up NaNs and save
    df = df.ffill()
    df.index = df.index.strftime('%Y-%m-%d')
    features_dict = json.loads(df.to_json(orient='index'))

    with open(output_file, 'w') as f:
        json.dump(features_dict, f, indent=4)
        
    print(f"Task P12 Complete. Saved engineered features to {output_file}")

if __name__ == "__main__":
    build_features('structured_macro.json', 'macro_features.json')