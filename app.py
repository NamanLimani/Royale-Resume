import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

# Import our backend modules
from src.document_processing.extractor import process_pdf
from src.job_fetching.fetcher import fetch_jobs
from src.job_fetching.analyzer import analyze_job
from src.orchestration.generator import generate_all_variants
from src.orchestration.latex_tester import test_compilation
from src.orchestration.judge import evaluate_and_select_winner
from src.tracking.logger import log_application

load_dotenv()

# --- PAGE CONFIG ---
st.set_page_config(page_title="Resume Royale", page_icon="👑", layout="wide")
st.title("👑 Resume Royale & Auto-Hunter")

# --- SIDEBAR: Document Upload ---
with st.sidebar:
    st.header("📄 Master Profiles")
    st.write("Upload your base resumes and LinkedIn PDFs here.")
    
    uploaded_files = st.file_uploader(
        "Upload PDFs", type=["pdf"], accept_multiple_files=True
    )
    
# Process the PDFs and store the extracted text in Streamlit's session state
    if st.button("Process Documents"):
        if uploaded_files:
            master_text = ""
            for file in uploaded_files:
                # Use Python's built-in tempfile module to safely handle the PDF
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                    temp_pdf.write(file.getbuffer())
                    temp_path = temp_pdf.name
                
                try:
                    # Extract text using the safe temporary path
                    extracted = process_pdf(temp_path)
                    master_text += f"\n--- {file.name} ---\n{extracted}\n"
                finally:
                    # The 'finally' block guarantees the file is deleted even if an error happens!
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                
            st.session_state['master_profile'] = master_text
            st.success("Documents successfully parsed and loaded into memory!")

            with st.expander("🔍 View Parsed Master Profile"):
                st.write("This is exactly what the LLMs see:")
                st.text(st.session_state['master_profile'])
                
        else:
            st.warning("Please upload at least one PDF.")

# --- MAIN AREA: Tabs ---
tab1, tab2 = st.tabs(["🕵️ Job Hunter", "✍️ Manual Tailor (Battle Royale)"])

# --- TAB 1: Job Hunter ---
with tab1:
    st.header("Live Job Scraper")
    
    # Changed to 4 columns to fit the new dropdown
    col1, col2, col3, col4 = st.columns(4) 
    with col1:
        query_input = st.text_input("Job Fields (comma separated)", value="Machine Learning, Software Engineer, AI")
    with col2:
        location = st.text_input("Location", value="United States")
    with col3:
        time_window_str = st.selectbox("Posted Within:", ["5 mins", "15 mins", "30 mins", "60 mins", "24 hours"])
    with col4:
        # --- NEW EXPERIENCE DROPDOWN ---
        exp_level = st.selectbox("Experience Level:", ["Any", "Internship", "Entry Level", "Associate", "Mid Level", "Senior", "Director"])
    
    time_map = {"5 mins": 5, "15 mins": 15, "30 mins": 30, "60 mins": 60, "24 hours": 1440}
    
    # 1. THE SCAN BUTTON (Only fetches and saves to memory)
    if st.button("Scan Jobs"):
        with st.spinner("Fetching live data..."):
            minutes = time_map[time_window_str]
            queries = [q.strip() for q in query_input.split(',') if q.strip()]
            
            # Combine domains (e.g., '"Machine Learning" OR "AI"')
            base_query = " OR ".join(f'"{q}"' for q in queries)
            
            # --- THE BOOLEAN LEVEL FILTER ---
            # If they select Entry Level, the query becomes: '("Machine Learning" OR "AI") "Entry Level"'
            if exp_level != "Any":
                formatted_query = f"({base_query}) \"{exp_level}\""
            else:
                formatted_query = base_query
            
            # Save the results and the query length to Streamlit's memory
            st.session_state['fetched_jobs'] = fetch_jobs(formatted_query, location, minutes)
            st.session_state['query_count'] = len(queries)

    # 2. THE DISPLAY LOOP (Runs independently as long as jobs are in memory)
    if 'fetched_jobs' in st.session_state:
        jobs = st.session_state['fetched_jobs']
        
        if jobs:
            st.success(f"Found {len(jobs)} jobs across {st.session_state.get('query_count', 1)} domains using 1 API credit!")
            
            # 1. Add 'i, ' and 'enumerate()' to the loop
            for i, job in enumerate(jobs):
                with st.expander(f"{job['title']} at {job['company']} ({job['posted_at']})"):
                    st.write(f"**Location:** {job['location']}")
                    
                    if job.get('link') and job['link'] != "#":
                        st.markdown(f"[🔗 Click Here to Apply Original Posting]({job['link']})")
                    
                    # 2. Add '_{i}' to the end of the button key
                    if st.button(f"Analyze Fit for {job['company']}", key=f"analyze_{job['id']}_{i}"):
                        
                        if 'master_profile' not in st.session_state:
                            st.warning("⚠️ Please upload and process your Master PDFs in the sidebar first!")
                        elif job['description'] == "No description provided." or not job['description']:
                            st.error("❌ The API couldn't fetch the full description for this job. Copy the description manually and use the 'Manual Tailor' tab instead.")
                        else:
                            with st.spinner(f"Groq is analyzing your fit for {job['company']}..."):
                                analysis = analyze_job(job['description'], st.session_state['master_profile'])
                                
                                if analysis:
                                    st.markdown("### 🤖 AI Fit Analysis")
                                    col_score, col_sponsor = st.columns(2)
                                    
                                    score = analysis.get('match_score', 0)
                                    col_score.metric("Match Score", f"{score}%")
                                    
                                    sponsor_status = analysis.get('sponsorship_available', False)
                                    sponsor_text = "✅ Yes / Likely" if sponsor_status else "❌ No / Unlikely"
                                    col_sponsor.metric("Sponsorship", sponsor_text)
                                    
                                    st.warning(f"**Skill Gap:** {analysis.get('skill_gap', 'None identified.')}")
                                    
                                    st.text_area(
                                        label="Copy this to email the recruiter:", 
                                        value=analysis.get('cold_email', ''), 
                                        height=150, 
                                        # 3. Add '_{i}' to the end of the text_area key too!
                                        key=f"email_{job['id']}_{i}" 
                                    )
                                else:
                                    st.error("Analysis failed. The LLM hallucinated bad JSON. Try again.")
        else:
            st.info("No jobs found in that time window. Try expanding the search.")


# --- TAB 2: Manual Tailor ---
with tab2:
    st.header("The LLM Battle Royale")
    st.write("Paste a specific Job Description below to generate a tailored LaTeX resume.")
    
    # Input fields for logging
    col_comp, col_title = st.columns(2)
    with col_comp:
        company_name = st.text_input("Company Name (for logging):", value="Unknown Company")
    with col_title:
        job_title = st.text_input("Job Title (for logging):", value="Target Role")
        
    job_description = st.text_area("Paste Job Description Here:", height=200)
    
    if st.button("Generate Tailored Resume", type="primary"):
        # Safety Checks
        if 'master_profile' not in st.session_state or not st.session_state['master_profile'].strip():
            st.error("⚠️ Please process your master PDFs in the sidebar first!")
        elif not job_description.strip():
            st.error("⚠️ Please paste a Job Description.")
        else:
            st.info("⚔️ The Battle Royale has begun. Firing up 5 LLMs concurrently...")
            
            # --- PHASE 1: GENERATION ---
            with st.spinner("Phase 1/3: All models are writing code..."):
                raw_variants = generate_all_variants(st.session_state['master_profile'], job_description)
                
            if not raw_variants:
                st.error("❌ All models failed to generate content.")
            else:
                st.success(f"✅ Generated {len(raw_variants)} drafts.")
                
                # --- PHASE 2: COMPILATION TEST ---
                with st.spinner("Phase 2/3: Compiling LaTeX to test for fatal syntax errors..."):
                    successful_variants = test_compilation(raw_variants)
                    
                if not successful_variants:
                    st.error("❌ All models produced broken LaTeX that failed to compile.")
                else:
                    st.success(f"✅ {len(successful_variants)} models successfully compiled.")
                    
                    # --- PHASE 3: THE JUDGE ---
                    with st.spinner("Phase 3/3: The Judge is evaluating the surviving variants..."):
                        winner_name, winning_latex, judge_rationale = evaluate_and_select_winner(successful_variants, job_description)
                        
                    if winning_latex:
                        st.success(f"🏆 {winner_name} Wins!")
                        
                        # Display the Judge's reasoning
                        with st.expander("Why did this model win?"):
                            st.write(judge_rationale)
                            
                        # Log the application to your daily text file
                        log_path = log_application(company_name, job_title, winning_latex)
                        if log_path:
                            st.caption(f"📝 Application logged locally at: `{log_path}`")
                            
                        # Display the raw LaTeX for easy copying
                        st.markdown("### Winning LaTeX Code")
                        st.code(winning_latex, language="latex")
                        
                        # Provide a 1-click download button for the .tex file
                        safe_company = company_name.replace(" ", "_")
                        st.download_button(
                            label="⬇️ Download .tex File",
                            data=winning_latex,
                            file_name=f"{safe_company}_Resume.tex",
                            mime="text/plain"
                        )
                    else:
                        st.error("❌ Failed to select a winner.")