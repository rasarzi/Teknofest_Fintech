import json
import pandas as pd

def create_insights(input_file, output_file):
    print(f"Loading {input_file} for P19 Insight Generation...")
    
    with open(input_file, 'r') as f:
        features = json.load(f)

    df = pd.DataFrame(features)
    df['date'] = pd.to_datetime(df['date'])

    insights = {}
    
    # Grab the most recent day's data for each ticker
    for ticker, group in df.groupby('ticker'):
        latest_row = group.loc[group['date'].idxmax()].to_dict()
        latest_row['date'] = latest_row['date'].strftime('%Y-%m-%d')

        # Logic for LLM Translation
        rsi = latest_row.get('rsi_14')
        trend = "Bullish" if latest_row['close'] > latest_row.get('sma_50', 0) else "Bearish"
        momentum = latest_row.get('momentum_20d')
        drawdown = latest_row.get('drawdown')
        fmt = lambda x, factor=1: f'{x * factor:.2f}' if x is not None and pd.notna(x) else 'N/A'

        insight_text = (
            f"As of {latest_row['date']}, {ticker} is in a {trend} trend based on its 50-day SMA. "
            f"The 14-day RSI is {fmt(rsi)}. "
            f"Recent 20-day momentum is {fmt(momentum, 100)}% "
            f"with a current drawdown of {fmt(drawdown, 100)}% from its peak."
        )

        insights[ticker] = {
            "analysis_date": latest_row['date'],
            "llm_system_context": insight_text,
            "raw_metrics_snapshot": latest_row
        }

    with open(output_file, 'w') as f:
        json.dump(insights, f, indent=4)
        
    print(f"Task P19 Complete. Saved LLM insights to {output_file}")

if __name__ == "__main__":
    create_insights('stock_features.json', 'stock_insight.json')