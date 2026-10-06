import os
import json
from openai import OpenAI

# Initialize client using environment variable for security
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY") 
)

def parse_with_llm(raw_text: str) -> dict:
    """
    Uses an LLM to extract structured entities from messy unstructured text.
    Simulates cleaning scraped HTML content for AI training datasets.
    """
    prompt = f"""
    You are a data extraction assistant. Extract the following fields from the text below 
    and return ONLY valid JSON:
    - title (string)
    - date (YYYY-MM-DD format or null)
    - summary (max 50 words)
    - sentiment (positive/negative/neutral)
    
    Text: {raw_text}
    """
    
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct:free",  # Free tier model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        # Parse JSON response safely
        content = response.choices[0].message.content.strip()
        # Remove markdown code blocks if present
        content = content.replace("```json", "").replace("```", "")
        return json.loads(content)
        
    except Exception as e:
        return {"error": str(e), "raw_input": raw_text[:100]}

if __name__ == "__main__":
    sample_text = "BREAKING: On October 7th, 2026, Mindrift announced a major expansion in AI data services. The company expressed great optimism about future growth despite market challenges."
    result = parse_with_llm(sample_text)
    print(json.dumps(result, indent=2))