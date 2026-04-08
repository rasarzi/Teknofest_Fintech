import json

def standardize_schema(input_file, output_file):
    print(f"Loading {input_file} for P11 (Expanded)...")
    
    with open(input_file, 'r') as f:
        clean_data = json.load(f)
        
    structured_data = []
    
    # Map the specific frequencies for the new indicators
    freq_map = {
        "gdp": "quarterly",
        "interest_rate": "daily",
        "yield_data": "daily"
    }
    
    for date, indicators in clean_data.items():
        for indicator_name, value in indicators.items():
            # If it's not in the map above, default to monthly
            freq = freq_map.get(indicator_name, "monthly")
            
            record = {
                "indicator": indicator_name,
                "date": date,
                "value": value,
                "frequency": freq
            }
            structured_data.append(record)
            
    with open(output_file, 'w') as f:
        json.dump(structured_data, f, indent=4)
        
    print(f"Task P11 Complete. Saved expanded schema to {output_file}")

if __name__ == "__main__":
    standardize_schema('clean_macro.json', 'structured_macro.json')