import json

def generate_llm_insight(input_file, output_file):
    print(f"Loading {input_file} for P13 Insight Generation...")
    
    with open(input_file, 'r') as f:
        features = json.load(f)
        
    # Grab the very last day of data (the most current snapshot)
    latest_date = list(features.keys())[-1]
    current_data = features[latest_date]
    
    # Construct a structured prompt/insight for an LLM
    insight_payload = {
        "analysis_date": latest_date,
        "current_regime": current_data.get('macro_regime', 'Unknown'),
        "llm_system_context": (
            f"As of {latest_date}, the macroeconomic regime is classified as '{current_data.get('macro_regime')}'. "
            f"Inflation is currently {current_data.get('inflation_direction')} and interest rates are {current_data.get('rate_direction')}. "
            f"The yield spread is {round(current_data.get('yield_spread', 0), 2)}. "
            f"Use this context to adjust risk models and asset allocation weightings."
        ),
        "raw_metrics_snapshot": current_data
    }
    
    with open(output_file, 'w') as f:
        json.dump(insight_payload, f, indent=4)
        
    print(f"Task P13 Complete. Saved LLM insights to {output_file}")

if __name__ == "__main__":
    generate_llm_insight('macro_features.json', 'macro_insight.json')