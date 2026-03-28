import os
from openai import OpenAI

def generate_resume(system_prompt : str , user_prompt : str) -> str :
    client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

    response = client.chat.completions.create(
        model="microsoft/phi-3-mini-128k-instruct:free",
        messages=[
            {"role" : "system" , "content" : system_prompt},
            {"role" : "user" , "content" : user_prompt} 
        ]
    )

    return response.choices[0].message.content