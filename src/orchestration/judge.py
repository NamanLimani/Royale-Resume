import re
from config.prompts import JUDGE_SYSTEM_PROMPT
from src.llm_clients.gemini_client import generate_resume

def evaluate_and_select_winner(successful_varients: dict , job_discription : str) -> tuple :
    """
    Asks an LLM to evaluate the compiled LaTeX variants and pick the best one.
    Returns a tuple: (winner_name, winning_latex_code, judge_rationale)
    """
    if not successful_varients:
        print("[Error] No successful variants to judge")
        return None , None , "No variants compiled successfully."
    
    # If only one survived the pdflatex compilation test, it wins by default
    if len(successful_varients) == 1:
        winner_name = list(successful_varients.keys())[0]
        print(f"[Info] Only {winner_name} compiled successfully . It wins by default.")
        return winner_name , successful_varients[winner_name] , "won by default (other failed to compile.)"
    
    print("[Info] Sending Compiled variants to the Judge LLM ..")

    # Construct the User Prompt for the Judge by stacking the JD and all successful LaTeX codes
    user_prompt = f"JOB DESCRIPTION : {job_discription}\n\n"
    for variant_name , latex_code in successful_varients.items():
        user_prompt += f"--- {variant_name} ---\n{latex_code}\n\n"

    try :
        # We reuse the Gemini client. (The function is named generate_resume, but it just sends text to the API)
        judge_response = generate_resume(JUDGE_SYSTEM_PROMPT , user_prompt)

        # Use Regex to hunt for our strict output format: "WINNER: Variant 1"
        match = re.search(r"WINNER: \s*(Variant \d+)" , judge_response , re.IGNORECASE)

        if match:
            # Extract exactly what the model matched (e.g., "Variant 2")
            matched_string = match.group(1).strip()

            # Find the full key in our dictionary that contains this string (e.g., "Variant 2 (Groq)")
            winner_name = next((key for key in successful_varients.keys() if matched_string in key) , None)

            if winner_name:
                print(f"[Success] The Judge selected : {winner_name}")
                return winner_name , successful_varients[winner_name] , judge_response
            
        # Fallback: If the Judge hallucinates and doesn't output the exact string, pick the first one
        print("[Warning] Judge output format invalid. Picking the first available variant.")
        winner_name = list(successful_varients.keys())[0]
        return winner_name , successful_varients[winner_name] , judge_response
    
    except Exception as e :
        print(f"[Error] Judge LLM failed {e}")
        winner_name = list(successful_varients.keys())[0]
        return winner_name , successful_varients[winner_name] , "Judge API failed. Select Default."