import pandas as pd
import json

def build_features(input_file, output_file):
    print(f"Loading {input_file} for P12 Feature Engineering...")
    
    with open(input_file, 'r') as f:
        data = json.load(f)
        
    # Convert list of dicts back to a DataFrame and pivot for math operations
    df = pd.DataFrame(data)
    df = df.pivot(index='date', columns='indicator', values='value')
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # --- THE DATA FIX ---
    # Force all columns to be numeric. If it finds a '.', it turns it into NaN.
    df = df.apply(pd.to_numeric, errors='coerce')
    # Fill those new blanks with the last known valid number
    df = df.ffill().bfill()
    # --------------------

    # 1. Spreads (Yield Curve proxy: 10-Year Treasury minus Federal Funds Rate)
    if 'yield_data' in df.columns and 'interest_rate' in df.columns:
        df['yield_spread'] = df['yield_data'] - df['interest_rate']
    
    # 2. Trends (30-day moving averages)
    for col in ['inflation', 'interest_rate', 'unemployment']:
        if col in df.columns:
            df[f'{col}_trend_30d'] = df[col].rolling(window=30).mean()

    # 3. Directions (Current value minus value 30 days ago)
    if 'interest_rate' in df.columns:
        df['rate_direction'] = df['interest_rate'].diff(periods=30).apply(
            lambda x: "Rising" if x > 0 else ("Falling" if x < 0 else "Flat")
        )
        
    if 'inflation' in df.columns:
        df['inflation_direction'] = df['inflation'].diff(periods=30).apply(
            lambda x: "Rising" if x > 0 else ("Falling" if x < 0 else "Flat")
        )

    # 4. Regime Signals (Simple logic based on directions)
    def determine_regime(row):
        rate = row.get('rate_direction', 'Flat')
        infl = row.get('inflation_direction', 'Flat')
        if rate == "Rising" and infl == "Rising": return "Overheating / Tightening"
        if rate == "Falling" and infl == "Falling": return "Cooling / Easing"
        if rate == "Rising" and infl == "Falling": return "Restrictive"
        return "Transitional"

    df['macro_regime'] = df.apply(determine_regime, axis=1)

    # Clean up any NaN values created by the rolling/diff math
    df = df.bfill().ffill()

    # Convert back to JSON dictionary format
    df.index = df.index.strftime('%Y-%m-%d')
    features_dict = df.to_dict(orient='index')

    with open(output_file, 'w') as f:
        json.dump(features_dict, f, indent=4)
        
    print(f"Task P12 Complete. Saved engineered features to {output_file}")

if __name__ == "__main__":
    build_features('structured_macro.json', 'macro_features.json')