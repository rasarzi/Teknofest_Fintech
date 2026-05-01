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
    client = genai.Client(api_key="AIzaSyBYdmMC62oUTmHHJdOagec4E-5jmySGMzY")
    
    # 4. The True Global Industrial & Strategy Prompt
    prompt = f"""
    You are an expert financial AI Investment Assistant.
    
    I am providing you with the last 5 years of macroeconomic data covering key industry-level indicators for the US, China, India, and the Eurozone.
    
    Context Snapshot: As of {latest_date_str}, the US macroeconomic regime is classified as '{current_data.get('macro_regime', 'Unknown')}'. 
    
    Task:
    Write a highly analytical, 2-paragraph investment briefing.
    
    Paragraph 1 (Global Industrial Assessment): Explicitly state that your analysis is based on the trends from the last five years of global data. Analyze the industrial output, manufacturing health, and supply chain dynamics of the US, China, India, and the Eurozone simultaneously. You MUST use the specific, direct data provided for each of these respective regions to assess the global industrial landscape as a whole, treating each region as a primary data point rather than just a reaction to the US.
    
    Paragraph 2 (Comprehensive Investment Strategy): Detail a specific, actionable investment strategy based on this global assessment. Your strategy MUST explicitly cover asset allocation or sector recommendations across these four markets. Explain how an investor should position themselves to capitalize on the distinct economic realities of the US, China, India, and the Eurozone.
    
    Constraints:
    - Do NOT define any macroeconomic terms.
    - Keep the tone highly professional and suitable for an institutional investor.
    - You MUST explicitly mention and analyze the US, China, India, and the Eurozone in BOTH paragraphs based on their actual provided data.
    
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

    # 6. Save the final payload 
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