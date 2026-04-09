import json
from datetime import datetime, timedelta
from google import genai

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
    # ---> PASTE YOUR ACTUAL GEMINI API KEY BELOW (Starts with AIza...) <---
    client = genai.Client(api_key="AIzaSyBYdmMC62oUTmHHJdOagec4E-5jmySGMzY")
    
    # 4. Construct the heavily optimized prompt
    prompt = f"""
    You are an expert macroeconomic analyst briefing a retail investor.
    
    I am providing you with the last 5 years of US macroeconomic data covering 10 key indicators.
    
    Context Snapshot: As of {latest_date_str}, the macroeconomic regime is classified as '{current_data.get('macro_regime', 'Unknown')}'. 
    Inflation direction: {current_data.get('inflation_direction', 'Unknown')}. 
    Interest rate direction: {current_data.get('rate_direction', 'Unknown')}.
    
    Task:
    In 2 clear paragraphs, analyze the current US macroeconomic situation based on this data, assess the environment, and provide a high-level investment strategy.
    
    CRITICAL "ZERO JARGON" RULE:
    1. You must clearly explain what a '{current_data.get('macro_regime', 'Unknown')}' regime actually means for the broader economy.
    2. Every single time you mention an indicator (like M2, Housing Starts, or Yield Spreads) or an investment concept (like fixed income, cyclical equities, or real returns), you MUST briefly define what it means in simple, plain English right inside the sentence. Do not assume the reader knows any financial vocabulary.
    
    Constraints:
    - Base your analysis purely on the provided fundamental data.
    - Integrate definitions naturally into the flow of your writing. Do not just make a list.
    - Do not use em-dashes (—), hyphens, or complex special punctuation. Keep sentences simple and use standard commas or parentheses instead.
    
    Data (Last 5 Years):
    {json.dumps(five_year_data, indent=2)}
    """
    
    # 5. Call the Gemini API
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        ai_analysis_text = response.text
        print("\nGemini Analysis Generated Successfully!\n")
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        ai_analysis_text = "Failed to generate AI insight."

    # 6. Save the final payload (ensure_ascii=False fixes the \u2014 issue)
    insight_payload = {
        "analysis_date": latest_date_str,
        "ai_generated_analysis": ai_analysis_text,
        "raw_metrics_snapshot": current_data
    }
    
    with open(output_file, 'w') as f:
        json.dump(insight_payload, f, indent=4, ensure_ascii=False)
        
    print(f"Task P13 Complete. Saved AI insights to {output_file}")

if __name__ == "__main__":
    generate_llm_insight('macro_features.json', 'macro_insight.json')