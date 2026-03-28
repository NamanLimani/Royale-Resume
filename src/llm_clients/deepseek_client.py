import os
from openai import OpenAI

def generate_resume(system_prompt : str , user_prompt : str) -> str :
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role" : "system" , "content" : system_prompt},
            {"role" : "user" , "content" : user_prompt}
        ]
    )

    return response.choices[0].message.content