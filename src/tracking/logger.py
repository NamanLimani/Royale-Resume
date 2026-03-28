import os
from pathlib import Path
from datetime import datetime

def log_application(company_name : str , job_title : str , latex_code : str , log_dir : str = "data/daily_logs") -> str :
    """
    Appends the details of a job application and the tailored LaTeX code 
    to a daily summary text file.
    """

    # Ensure the daily_logs directory exists
    Path(log_dir).mkdir(parents=True , exist_ok=True)

    # Get today's date in YYYY-MM-DD format
    today_str = datetime.now().strftime("%Y-%m-%d")

    # Create the dynamic file name
    log_file_path = os.path.join(log_dir , f"applications_{today_str}.txt")

    # Get the exact time the application was processed
    timestamp = datetime.now().strftime("%H:-%M:-%S")

    # Format the entry block
    entry = (
        f"==================================================\n"
        f"Time : {timestamp}\n"
        f"Company : {company_name}\n"
        f"Position : {job_title}\n"
        f"==================================================\n"
        f"--- Tailored Latex Code ---\n"
        f"{latex_code}\n\n"
    )

    try :
        # Open the file in "a" (append) mode to add to the end of the file
        with open(log_file_path , "a" , encoding="utf-8") as file :
            file.write(entry)
        print(f"[Success] Application logged to {log_file_path}")
        return log_file_path
    
    except Exception as e :
        print(f"[Error] Failed to log application {e}")
        return None

