import yfinance as yf
import json
import pandas as pd

def get_historical_stock_data(tickers, benchmark):
    all_symbols = tickers + [benchmark]
    final_data = {}

    for symbol in all_symbols:
        print(f"Downloading data for {symbol}...")
        ticker_obj = yf.Ticker(symbol)
        # Fetch 5 years of data
        df = ticker_obj.history(period="5y", interval="1d")
        
        if not df.empty:
            # Clean the data
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
            df.index = df.index.strftime('%Y-%m-%d')
            final_data[symbol] = df.to_dict(orient='index')
        else:
            print(f"Warning: No data found for {symbol}.")
            final_data[symbol] = {}

    return final_data

if __name__ == "__main__":
    my_tickers = ['AAPL', 'MSFT']
    my_benchmark = 'SPY'
    
    # 1. Get the data
    stock_dict = get_historical_stock_data(my_tickers, my_benchmark)
    
    # 2. Save the data to raw_stock.json
    output_filename = 'raw_stock.json'
    with open(output_filename, 'w') as f:
        json.dump(stock_dict, f, indent=4)
        
    print(f"\nSuccess! '{output_filename}' has been created.")