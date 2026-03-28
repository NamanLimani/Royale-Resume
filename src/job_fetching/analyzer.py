import json
from src.llm_clients.groq_client import generate_resume as generate_text

# We force the LLM to output pure JSON so Python can parse it easily
ANALYZER_PROMPT = """

You are an elite technical recruiter AI evaluating a candidate's fit for a specific job. 
Analyze the provided Job Description against the Candidate's Resume.

You MUST output a raw JSON object with exactly these four keys:
{
    "sponsorship_available": boolean (true if STEM-OPT/H1B is explicitly mentioned or implied, false if it says US Citizen/Green Card only),
    "match_score": integer (0 to 100 representing how well the resume skills match the JD),
    "skill_gap": string (One short, brutal sentence warning the candidate about missing mandatory skills),
    "cold_email": string (A professional, 3-sentence email draft to the recruiter highlighting the candidate's matching skills)
}

DO NOT output markdown blocks (like ```json). DO NOT output any conversational text. ONLY output the raw JSON string.

"""

def analyze_job(job_description : str , parsed_resume : str) -> dict :
    """
    Passes the JD and Resume to an LLM to extract sponsorship, match score, skill gaps, and a cold email.
    """

    user_prompt = f"Candidate Resume: \n{parsed_resume}\n\nJob Description: \n{job_description}"

    try :
        print("[Info] Analyzing job fit and extracting insights ...")
        
        # Call our fast Groq model
        response_text = generate_text(ANALYZER_PROMPT , user_prompt)

        # Strip out markdown backticks just in case the LLM disobeys the prompt
        clean_json = response_text.replace("```json" , "").replace("```" , "").strip()

        # Convert the string into a Python dictionary
        analysis = json.loads(clean_json)

        return analysis
    
    except json.JSONDecodeError :
        print("[Error] The LLM did not return valid JSON")
        return None

    except Exception as e :
        print(f"[Error] Failed to analyse job: {e}")
        return None

