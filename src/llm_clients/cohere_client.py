import os 
import cohere

def generate_resume(system_prompt : str , user_prompt : str) -> str:
    client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))

    # Cohere has a specific 'preamble' argument for system prompts
    response = client.chat(
        message=user_prompt,
        preamble=system_prompt,
        model="command-r-plus-08-2024"
    )

    return response.text