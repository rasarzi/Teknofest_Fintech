import os
import json
from datetime import datetime, timedelta
from google import genai
from google.genai import types

def generate_llm_insight(input_file, output_file):
    print(f"Loading {input_file} for P13 AI Agent Integration...")
    
    # 1. Load the engineered features
    with open(input_file, 'r') as f:
        features = json.load(f)
        
    dates = sorted(list(features.keys()))
    latest_date_str = dates[-1]
    current_data = features[latest_date_str]
    
    # 2. Filter data for the last 5 years
    latest_date_obj = datetime.strptime(latest_date_str, '%Y-%m-%d')
    five_years_ago = latest_date_obj - timedelta(days=5*365)
    
    five_year_data = {}
    for d in dates:
        if datetime.strptime(d, '%Y-%m-%d') >= five_years_ago:
            five_year_data[d] = features[d]

    print("Data filtered. Connecting to Gemini API...")
    
    # 3. Setup Gemini API Client 
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("Set GEMINI_API_KEY before generating AI insights.")
    client = genai.Client(api_key=api_key)
    
    # 4. Evidence-grounded summary prompt; the model must not invent missing data.
    prompt = f"""
    You are a financial data analyst preparing a cautious descriptive summary.
    Summarize observable macroeconomic trends in the supplied indicators, including
    regions only where evidence exists. Distinguish inflation indices from inflation
    rates and avoid comparing different units directly. Mention incomplete coverage,
    stale observations, methodological limitations and uncertainty. Do not invent
    statistics, price forecasts, recommendations, allocations or investment advice.
    Provide a short, neutral overview in no more than three paragraphs.

    Historical records (up to five years; JSON):
    {json.dumps(five_year_data, separators=(',', ':'))}
    """

    # 5. Call the Gemini API with Temperature = 0.0 (Zero Creativity)
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0, 
            )
        )
        ai_analysis_text = response.text
        print("\nGemini Analysis Generated Successfully!\n")
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        ai_analysis_text = "Failed to generate AI insight."

    # 6. Save the final payload 
    insight_payload = {
        "analysis_date": latest_date_str,
        "ai_generated_analysis": ai_analysis_text
    }
    
    with open(output_file, 'w') as f:
        json.dump(insight_payload, f, indent=4, ensure_ascii=False)
        
    print(f"Task P13 Complete. Saved AI insights to {output_file}")

if __name__ == "__main__":
    generate_llm_insight('macro_features.json', 'macro_insight.json')