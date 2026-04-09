import json

def standardize_schema(input_file, output_file):
    print(f"Loading {input_file} for P11 (Expanded)...")
    
    with open(input_file, 'r') as f:
        clean_data = json.load(f)
        
    structured_data = []
    freq_map = {
        "gdp": "quarterly",
        "interest_rate": "daily",
        "yield_data": "daily"
    }
    
    # Safety Check: Did P10 group by Date or by Indicator?
    first_key = list(clean_data.keys())[0]
    is_date_first = first_key.startswith("19") or first_key.startswith("20")

    if is_date_first:
        # Format: {"2020-01-01": {"inflation": 2.5, ...}}
        for date, indicators in clean_data.items():
            for indicator_name, value in indicators.items():
                freq = freq_map.get(indicator_name, "monthly")
                structured_data.append({
                    "indicator": indicator_name,
                    "date": date,
                    "value": value,
                    "frequency": freq
                })
    else:
        # Format: {"inflation": {"2020-01-01": 2.5, ...}}
        for indicator_name, dates in clean_data.items():
            freq = freq_map.get(indicator_name, "monthly")
            for date, value in dates.items():
                structured_data.append({
                    "indicator": indicator_name,
                    "date": date,
                    "value": value,
                    "frequency": freq
                })

    with open(output_file, 'w') as f:
        json.dump(structured_data, f, indent=4)
        
    print(f"Task P11 Complete. Saved expanded schema to {output_file}")

if __name__ == "__main__":
    standardize_schema('clean_macro.json', 'structured_macro.json')