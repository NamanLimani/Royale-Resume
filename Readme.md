These commands are incredibly important, and including them in the README is a massive help for anyone (including future you) trying to set this up on a Mac! 

* `brew install poppler tesseract` installs the system-level engines required to read and perform OCR on complex PDFs.
* `brew install --cask mactex-no-gui` installs the lightweight version of the LaTeX compiler so you don't download 5GB of useless GUI apps.
* `eval "$(/usr/libexec/path_helper)"` is a brilliant addition. It instantly refreshes the Mac terminal's PATH variable so Python can find `pdflatex` without forcing the user to close and reopen their terminal.

Here is the fully updated `README.md` file with those system dependencies integrated perfectly into the setup instructions.

***

```markdown
# 👑 Resume Royale & Auto-Hunter

**An intelligent, multi-agent AI pipeline that scrapes live job boards, analyzes your fit, and orchestrates a "Battle Royale" between top LLMs to generate the perfect, mathematically-optimized, single-page LaTeX resume.**

---

## 📖 The "No-Code" Explanation: How It Works
Resume Royale is designed to solve the two biggest problems in the modern job hunt: finding fresh jobs before thousands of others apply, and tailoring your resume to beat Applicant Tracking Systems (ATS) without spending hours formatting. 

Here is exactly how the system works from the user's perspective:

### 1. The "Data Lake" (Document Ingestion)
Instead of typing out your profile, you simply upload your Master Resume and a detailed PDF of your deep-dive LinkedIn projects into the sidebar. The system reads these documents and stores them in its memory as a "Data Lake." 
* *Transparency Feature:* You can click an "X-Ray" view to see exactly what the AI sees.

### 2. The Auto-Hunter (Live Job Scraper)
You enter your desired job titles (e.g., "Machine Learning, Software Engineer"), location, and experience level (e.g., "Entry Level"), and select a time window (e.g., "Posted in the last 15 mins"). 
* The system reaches out to real-world job boards via SerpApi and fetches jobs that were posted moments ago. 
* With one click, an AI analyzes the job description against your "Data Lake", gives you a **Match Score**, identifies **Skill Gaps**, predicts **Visa Sponsorship**, and writes a custom **Cold Email** to the recruiter.

### 3. The Battle Royale (Resume Generation)
When you find a job you want, you paste the Job Description into the Generator. This triggers a 3-Phase orchestration pipeline:
* **Phase 1: Generation.** Multiple AI models (Groq and Gemini) compete concurrently to write LaTeX code for a resume. Using **"Authorized Synthesis" (RAG for Resumes)**, they don't just copy-paste your old bullet points; they read your deep project history and actively write *brand new* sentences tailored to the employer's exact keywords.
* **Phase 2: Compilation Test.** LLMs are notorious for writing broken code. The system takes the raw LaTeX from the models and runs a background `pdflatex` compiler. Any AI that forgot to escape a special character (like `\&`) crashes and is instantly disqualified.
* **Phase 3: The Judge.** A designated "Judge" AI evaluates the surviving PDFs. It checks for hallucinations (invented skills), enforces strict formatting rules (e.g., exactly 5 projects, perfectly dense 11-14 word bullet points that never wrap to a second line), and selects the winner. 
* **The Output:** You get a 1-click download of the winning `.tex` file, mathematically guaranteed to fit on a single page.

---

## 🧠 Core Engineering Achievements

* **Model-Specific Prompt Routing:** LLMs have different weaknesses. Groq (Llama 3) is obedient but literal; Gemini is creative but bad at LaTeX syntax. The system routes uniquely tailored prompts to each model's API, forcing Groq to adhere to strict word counts and forcing Gemini to strictly escape LaTeX characters.
* **RAG for Resumes (Authorized Synthesis):** Overcame the "AI Lobotomy" problem. Instead of strict copy-pasting, the system uses Retrieval-Augmented Generation principles, authorizing the AI to synthesize new achievements from a deep-dive knowledge base without hallucinating fake metrics or cloud platforms.
* **UI State Safety:** Implemented dynamic enumeration for Streamlit widgets to gracefully handle messy, missing, or identical Job IDs from the Google Jobs API without crashing the frontend.

---

## 🚀 Getting Started

### 1. System Dependencies & Prerequisites
To run this project locally, you need Python 3.9+, a LaTeX compiler (for compiling the resumes in Phase 2), and PDF processing tools (for reading your master resumes).

**For macOS (Recommended Setup):**
Run the following commands in your terminal to install the necessary LaTeX compiler and OCR tools via Homebrew:
```bash
# Install PDF extraction and OCR dependencies
brew install poppler tesseract

# Install the LaTeX compiler (MacTeX without the heavy GUI tools)
brew install --cask mactex-no-gui

# Refresh your terminal's PATH so Python can immediately find the pdflatex command
eval "$(/usr/libexec/path_helper)"
```

**For Windows / Linux:**
* **LaTeX:** Install [MiKTeX](https://miktex.org/) (Windows) or run `sudo apt-get install texlive-full` (Linux).
* **OCR Tools:** Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and [Poppler](https://poppler.freedesktop.org/) using your respective package managers.

### 2. Get Your API Keys
This project utilizes several world-class LLM and Search APIs. You will need to create free accounts and generate API keys for the services you wish to use:

| Service | Purpose | API Key Link |
| :--- | :--- | :--- |
| **Groq** | Lightning-fast Llama 3 inference | [Get Groq Key](https://console.groq.com/keys) |
| **Google Gemini** | Advanced synthesis & reasoning | [Get Gemini Key](https://aistudio.google.com/app/apikey) |
| **SerpApi** | Live Google Jobs scraping | [Get SerpApi Key](https://serpapi.com/manage-api-key) |
| **OpenRouter** | Access to rotating free-tier models | [Get OpenRouter Key](https://openrouter.ai/keys) |
| **DeepSeek** | Highly capable coding model | [Get DeepSeek Key](https://platform.deepseek.com/api_keys) |
| **Cohere** | Enterprise NLP model | [Get Cohere Key](https://dashboard.cohere.com/api-keys) |

### 3. Installation

**Clone the repository:**
```bash
git clone [https://github.com/YourUsername/Resume-Royale.git](https://github.com/YourUsername/Resume-Royale.git)
cd Resume-Royale
```

**Create and activate a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Set up your Environment Variables:**
Create a `.env` file in the root directory and add your API keys:
```env
GROQ_API_KEY=your_groq_key_here
GEMINI_API_KEY=your_gemini_key_here
SERPAPI_API_KEY=your_serpapi_key_here
# Optional keys depending on which clients you activate in generator.py
# DEEPSEEK_API_KEY=your_deepseek_key_here
# OPENROUTER_API_KEY=your_openrouter_key_here
# COHERE_API_KEY=your_cohere_key_here
```

### 4. Running the Application

Once your environment is set up and your LaTeX compiler is installed, simply run:
```bash
streamlit run app.py
```
The application will open in your default web browser at `http://localhost:8501`.

---

## 📁 Project Structure

```text
resume_royale_project/
├── app.py                              # Main Streamlit UI and application loop
├── config/
│   └── prompts.py                      # Model-Specific Prompts & LaTeX templates
├── data/
│   └── daily_logs/                     # Locally stored logs of generated applications
├── src/
│   ├── document_processing/
│   │   └── extractor.py                # PyPDF2/pdfplumber text extraction
│   ├── job_fetching/
│   │   ├── analyzer.py                 # Groq-powered AI fit analysis & cold emails
│   │   └── fetcher.py                  # SerpApi Google Jobs integration
│   ├── orchestration/
│   │   ├── generator.py                # ThreadPool orchestrator & prompt routing
│   │   ├── judge.py                    # Final evaluation and source tracking
│   │   └── latex_tester.py             # Subprocess pdflatex compilation tester
│   ├── tracking/
│   │   └── logger.py                   # File I/O for saving winning .tex outputs
│   └── llm_clients/                    # Individual API integration wrappers
│       ├── groq_client.py
│       ├── gemini_client.py
│       └── ...
├── .env                                # Environment variables (ignored in Git)
├── requirements.txt                    # Python dependencies
└── README.md                           # You are here
```

---
*Built by [Naman Limani](https://www.linkedin.com/in/naman-limani) — Merging AI Architecture with Career Engineering.*
```