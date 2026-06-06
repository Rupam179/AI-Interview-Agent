# Deployment & GitHub Upload Guide
## AI Interview Agent

---

## PART 1: LOCAL SETUP (Step-by-Step)

### Prerequisites
- Python 3.10 or higher: https://python.org/downloads
- Git: https://git-scm.com
- Gemini API Key: https://makersuite.google.com/app/apikey

### Step 1: Download / Clone the Project

```bash
git clone https://github.com/rupammukherjee/AI-Interview-Agent.git
cd AI-Interview-Agent
```

Or if you have the folder already:
```bash
cd AI-Interview-Agent
```

### Step 2: Create a Virtual Environment

```bash
# Create
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — macOS / Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### If PyAudio fails on Linux:
```bash
sudo apt-get install portaudio19-dev python3-dev
pip install pyaudio
```

#### If PyAudio fails on macOS:
```bash
brew install portaudio
pip install pyaudio
```

#### If PyAudio fails on Windows (use pre-compiled wheel):
```bash
pip install pipwin
pipwin install pyaudio
```

### Step 4: Set Up Environment Variables

```bash
# Copy the template
cp .env.example .env
```

Open `.env` in any text editor and fill in:
```
GEMINI_API_KEY=AIzaSy...your_actual_key_here...
SECRET_KEY=my_super_secret_key_12345
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

✅ The app will open at: **http://localhost:8501**

---

## PART 2: GITHUB UPLOAD

### Step 1: Create GitHub Repository

1. Go to https://github.com → **New repository**
2. Name: `AI-Interview-Agent`
3. Description: `AI-powered Interview Preparation Platform using Google Gemini, Streamlit, Python`
4. Set to **Public**
5. Do NOT initialise with README (we already have one)
6. Click **Create repository**

### Step 2: Initialise Git Locally

```bash
cd AI-Interview-Agent
git init
git add .
git commit -m "🚀 Initial commit: AI Interview Agent v1.0"
```

### Step 3: Connect and Push

```bash
git remote add origin https://github.com/YOUR_USERNAME/AI-Interview-Agent.git
git branch -M main
git push -u origin main
```

### Step 4: Verify Upload

Visit `https://github.com/YOUR_USERNAME/AI-Interview-Agent`

✅ All files should be visible including the README with badges.

### Step 5: Add Topics (for discoverability)

On GitHub repo page → Click ⚙️ (gear icon) next to **About**
Add topics: `python`, `streamlit`, `gemini-ai`, `interview-prep`, `nlp`, `speech-recognition`, `final-year-project`, `sdg8`

---

## PART 3: STREAMLIT CLOUD DEPLOYMENT (Free)

### Step 1: Push to GitHub (done above)

### Step 2: Sign Up / Login to Streamlit Cloud

Go to: https://share.streamlit.io
Sign in with GitHub.

### Step 3: Deploy

1. Click **New app**
2. Repository: `YOUR_USERNAME/AI-Interview-Agent`
3. Branch: `main`
4. Main file path: `app.py`
5. Click **Advanced settings**

### Step 4: Add Secrets

In **Secrets** section, add:
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
SECRET_KEY = "your_secret_key_here"
```

6. Click **Deploy!**

⏱️ Wait ~2 minutes for build

✅ Your app will be live at:
`https://YOUR_USERNAME-ai-interview-agent-app-XXXXX.streamlit.app`

### Step 5: Share Your App

Copy the public URL and add it to:
- GitHub README "Live Demo" badge
- LinkedIn profile
- Resume

---

## PART 4: DOCKER DEPLOYMENT

### Dockerfile (create in project root)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0"]
```

### Build and Run

```bash
docker build -t ai-interview-agent .
docker run -p 8501:8501 --env-file .env ai-interview-agent
```

✅ App at: **http://localhost:8501**

---

## PART 5: RUNNING TESTS

```bash
# Install pytest if not already installed
pip install pytest

# Run all tests
python -m pytest tests/ -v

# Run specific test files
python -m pytest tests/test_auth.py -v
python -m pytest tests/test_database.py -v
python -m pytest tests/test_resume_parser.py -v
```

Expected output:
```
tests/test_auth.py::TestPasswordHashing::test_hash_is_not_plain PASSED
tests/test_auth.py::TestPasswordHashing::test_verify_correct_password PASSED
...
tests/test_database.py::TestUserOperations::test_create_and_retrieve_user PASSED
...
========== 19 passed in 1.23s ==========
```

---

## TROUBLESHOOTING

### Issue: `GEMINI_API_KEY not set`
**Fix:** Ensure `.env` file exists in the project root with a valid key

### Issue: PyAudio installation fails
**Fix:** Install PortAudio system dependency first (see Step 3 above)

### Issue: `ModuleNotFoundError`
**Fix:** Ensure virtual environment is activated before running

### Issue: Database errors
**Fix:** Delete `database/interview_agent.db` and re-run — the app will recreate it

### Issue: Speech recognition fails
**Fix:** Check microphone permissions in OS settings; try the text fallback input

---

*Guide version 1.0 — AI Interview Agent*
*Rupam Mukherjee | Techno India University*
