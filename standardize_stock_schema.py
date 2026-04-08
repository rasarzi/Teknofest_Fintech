import json

def standardize_schema(input_file, output_file):
    print(f"Loading {input_file} for P17...")
    
    with open(input_file, 'r') as f:
        clean_data = json.load(f)

    structured_data = []
    
    for ticker, dates_data in clean_data.items():
        for date, metrics in dates_data.items():
            record = {
                "ticker": ticker,
                "date": date,
                "open": metrics.get("Open"),
                "high": metrics.get("High"),
                "low": metrics.get("Low"),
                "close": metrics.get("Close"),
                "volume": metrics.get("Volume")
            }
            structured_data.append(record)

    with open(output_file, 'w') as f:
        json.dump(structured_data, f, indent=4)
        
    print(f"Task P17 Complete. Saved standardized schema to {output_file}")

if __name__ == "__main__":
    standardize_schema('clean_stock.json', 'structured_stock.json')