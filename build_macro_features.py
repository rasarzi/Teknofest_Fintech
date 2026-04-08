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
    df = df.ffill().bfill()

    # 1. Spreads
    if 'yield_data' in df.columns and 'interest_rate' in df.columns:
        df['yield_spread'] = df['yield_data'] - df['interest_rate']
    
    # 2. Dynamic Trends (Automatically calculates 30-day moving average for ALL indicators)
    for col in df.columns:
        if col != 'yield_spread':
            df[f'{col}_trend_30d'] = df[col].rolling(window=30).mean()

    # 3. Directions
    if 'interest_rate' in df.columns:
        df['rate_direction'] = df['interest_rate'].diff(periods=30).apply(
            lambda x: "Rising" if x > 0 else ("Falling" if x < 0 else "Flat")
        )
    if 'inflation' in df.columns:
        df['inflation_direction'] = df['inflation'].diff(periods=30).apply(
            lambda x: "Rising" if x > 0 else ("Falling" if x < 0 else "Flat")
        )

    # 4. Regime Signals
    def determine_regime(row):
        rate = row.get('rate_direction', 'Flat')
        infl = row.get('inflation_direction', 'Flat')
        if rate == "Rising" and infl == "Rising": return "Overheating / Tightening"
        if rate == "Falling" and infl == "Falling": return "Cooling / Easing"
        if rate == "Rising" and infl == "Falling": return "Restrictive"
        return "Transitional"

    df['macro_regime'] = df.apply(determine_regime, axis=1)

    # Clean up NaNs and save
    df = df.bfill().ffill()
    df.index = df.index.strftime('%Y-%m-%d')
    features_dict = df.to_dict(orient='index')

    with open(output_file, 'w') as f:
        json.dump(features_dict, f, indent=4)
        
    print(f"Task P12 Complete. Saved engineered features to {output_file}")

if __name__ == "__main__":
    build_features('structured_macro.json', 'macro_features.json')