import os
import requests

def fetch_jobs(query: str, location: str, time_window_mins: int) -> list:
    """
    Fetches LIVE jobs from Google Jobs via SerpApi and filters them by recent posting times.
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        print("[Error] SERPAPI_API_KEY is missing from your .env file.")
        return []

    print(f"[Info] Reaching out to real job boards for '{query}' in '{location}'...")

    # We ask SerpApi for the Google Jobs engine, passing your specific search terms
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "hl": "en",
        "api_key": api_key,
        "chips": "date_posted:today" # Forces the API to only return jobs posted in the last 24 hours
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status() # Catcher for 404 or 401 Unauthorized errors
        data = response.json()

        jobs_results = data.get("jobs_results", [])
        
        formatted_jobs = []
        for job in jobs_results:
            # Google Jobs nests the posting time inside "detected_extensions"
            posted_time_str = job.get("detected_extensions", {}).get("posted_at", "").lower()
            
            # --- The Smarter Time Filter Logic ---
            minutes_ago = 0 # Default assumption
            
            try:
                # Extract the actual number from the string (e.g., "2" from "2 hours ago")
                num_str = ''.join(filter(str.isdigit, posted_time_str))
                if num_str:
                    num = int(num_str)
                    
                    # Convert everything to minutes so we can compare it cleanly
                    if "minute" in posted_time_str:
                        minutes_ago = num
                    elif "hour" in posted_time_str:
                        minutes_ago = num * 60
                    elif "day" in posted_time_str:
                        minutes_ago = num * 1440
            except ValueError:
                pass # If it says something weird without numbers like "Just now", keep it
                
            # Now we do one clean mathematical check!
            if minutes_ago > time_window_mins:
                continue # Skip this job if it's older than our limit
            
            apply_options = job.get("apply_options", [])
            job_url = apply_options[0].get("link") if apply_options else job.get("share_link", "#")
            
            # If it survived the filter, add it to our list
            formatted_jobs.append({
                "id": job.get("job_id", "unknown_id"),
                "title": job.get("title", "Unknown Title"),
                "company": job.get("company_name", "Unknown Company"),
                "location": job.get("location", location),
                "posted_at": posted_time_str,
                "description": job.get("description", "No description provided.") ,
                "link" : job_url
            })

        print(f"[Success] Found {len(formatted_jobs)} real job postings matching your time window.")
        return formatted_jobs

    except Exception as e:
        print(f"[Error] Failed to fetch real jobs: {e}")
        return []