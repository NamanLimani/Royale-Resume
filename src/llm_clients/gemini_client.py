import os
from google import genai

def generate_resume(system_prompt: str, user_prompt: str) -> str:
    # We use genai.Client() now, no more .configure()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    full_prompt = f"{system_prompt}\n\n{user_prompt}"
    
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=full_prompt
    )
    
    return response.text