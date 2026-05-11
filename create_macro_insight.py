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
    client = genai.Client(api_key="AIzaSyBYdmMC62oUTmHHJdOagec4E-5jmySGMzY")
    
    # 4. The Strict Template Prompt
    prompt = f"""
    You are an expert financial AI Investment Assistant.
    
    Task:
    Write an executive investment briefing based on the provided macroeconomic data.
    
    CRITICAL CONSTRAINT - STRICT TEMPLATE MATCHING:
    You must output your analysis to match the exact tone, phrasing, and structure of the Template below. You are forbidden from adding Wall Street jargon. Keep it exactly to these two paragraphs.
    
    [START TEMPLATE]
    To assess the global economy, we are focusing on exactly two indicators: Inflation and Stock Market Performance, using the United States as our baseline. In the United States, inflation has finally leveled out while the stock market continues to climb, meaning investors are seeing real, positive growth. Europe is in a weaker position; their inflation remains uncomfortably high, but their stock market has remained relatively flat, making it hard for investors there to keep up. India is currently the strongest performer, with a skyrocketing stock market that is easily outpacing its slightly higher inflation rate. Meanwhile, China is experiencing the opposite problem: they are dealing with falling prices, but their stock market continues to struggle and lose value as consumer confidence remains low.

    Based on these trends, investors should put the largest portion of their money into India and the United States, as both regions offer strong stock market growth that easily beats inflation. You should keep a much smaller, cautious amount invested in Europe, sticking only to highly reliable companies that can survive a flat market. Finally, you should avoid investing in China for now, keeping your money out of that region until their stock market shows clear signs of recovering from their current economic downturn.
    [END TEMPLATE]
    
    Data (Last 5 Years):
    {json.dumps(five_year_data, indent=2)}
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