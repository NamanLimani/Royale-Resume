import concurrent.futures

# 1. We ONLY import the custom prompts now, NO MORE GENERATOR_SYSTEM_PROMPT
from config.prompts import GROQ_SYSTEM_PROMPT, GEMINI_SYSTEM_PROMPT

# Import the base client functions and rename them so we don't confuse Python
from src.llm_clients.gemini_client import generate_resume as generate_gemini_client
from src.llm_clients.groq_client import generate_resume as generate_groq_client


# --- OUR NEW MODEL-SPECIFIC WRAPPERS ---
def generate_gemini(master_text: str, job_description: str) -> str:
    try:
        # Passes the Gemini-specific prompt
        full_user_prompt = f"User's Master Profile:\n{master_text}\n\nJob Description:\n{job_description}"
        return generate_gemini_client(GEMINI_SYSTEM_PROMPT, full_user_prompt)
    except Exception as e:
        print(f"[Error] Gemini generated an exception: {e}")
        return ""

def generate_groq(master_text: str, job_description: str) -> str:
    try:
        # Passes the Groq-specific prompt
        full_user_prompt = f"User's Master Profile:\n{master_text}\n\nJob Description:\n{job_description}"
        return generate_groq_client(GROQ_SYSTEM_PROMPT, full_user_prompt)
    except Exception as e:
        print(f"[Error] Groq generated an exception: {e}")
        return ""


# --- THE MAIN ORCHESTRATOR ---
def generate_all_variants(parsed_profile: str, job_description: str) -> dict:
    """
    Fires off requests to all active LLMs concurrently and returns a dictionary of their LaTeX outputs.
    """
    # 2. Map our keys to the NEW local wrapper functions we defined above!
    models = {
        "Variant 1 (Gemini)": generate_gemini,
        "Variant 2 (Groq)": generate_groq,
        # "Variant 3 (Deepseek)" : generate_deepseek,
        # "Variant 4 (OpenRouter)" : generate_openrouter,
        # "Variant 5 (Cohere)" : generate_cohere
    }

    result = {}

    print("[Info] Starting the LLM Battle Royale. Generating resumes concurrently ...")

    # Open a thread pool with 2 workers (since we only have 2 active models right now)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        
        # 3. Submit the tasks. Notice we only pass TWO arguments now!
        future_to_model = {
            executor.submit(func, parsed_profile, job_description): name
            for name, func in models.items()
        }

        # Collect the results as soon as each thread finishes
        for future in concurrent.futures.as_completed(future_to_model):
            model_name = future_to_model[future]
            try:
                latex_code = future.result()
                result[model_name] = latex_code
                print(f"[Success] {model_name} finished generating.")
            except Exception as exec:
                print(f"[Error] {model_name} generated an exception: {exec}")
                result[model_name] = None

    return result


