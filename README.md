# 🤖 AI Interview Agent

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Google_Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![SDG](https://img.shields.io/badge/SDG-8%20%7C%204-orange?style=for-the-badge)

**An AI-powered Interview Preparation Platform for students and job seekers.**  
Built with Google Gemini · Streamlit · Python · SQLite

[🚀 Live Demo](#deployment) · [📖 Documentation](#installation) · [🐛 Issues](../../issues) · [⭐ Star this repo](#)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [SDG Mapping](#sdg-mapping)
- [Future Scope](#future-scope)
- [Author](#author)
- [License](#license)

---

## 🌟 Overview

**AI Interview Agent** is a fully functional, production-grade interview preparation platform powered by **Google Gemini AI**. It helps students and job seekers prepare for technical and HR interviews through:

- 🔍 Intelligent resume analysis with ATS scoring
- 💬 AI-generated interview questions tailored to your profile
- 🎙️ Voice-based interview with real-time speech recognition
- 📊 Performance evaluation with detailed scoring
- 💡 Personalized feedback and learning roadmaps
- 🧭 AI career advisor with job path recommendations

This project was built as a **Semester 6 Final Year Project** for the Entrepreneurship & Skill Development (ESD) course at **Techno India University**, B.Tech CSE (AI & ML).

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **Auth System** | Register, login, logout with bcrypt password encryption |
| 📄 **Resume Analyzer** | Upload PDF/DOCX → ATS score, skill extraction, gap analysis |
| 💬 **Mock Interview** | AI generates 5–15 questions for 7 roles × 3 difficulty levels |
| 🎙️ **Voice Interview** | Speak answers, real-time speech-to-text, AI evaluation |
| 📊 **Evaluation Engine** | Scores for Technical, Communication, Confidence (0–100) |
| 💡 **Feedback System** | Strengths, weaknesses, improvements, learning path |
| 📈 **Dashboard** | Score trends, radar charts, ATS gauge, interview history |
| 🧭 **Career Advisor** | Career paths, certifications, courses, tech recommendations |

### Supported Job Roles
`Software Engineer` · `Data Analyst` · `Data Scientist` · `AI Engineer` · `Frontend Developer` · `Backend Developer` · `Full Stack Developer`

### Difficulty Levels
`Beginner` · `Intermediate` · `Advanced`

---

## 🏗️ Architecture

```
User → Streamlit UI
         ↓
    app.py (router)
         ↓
   ┌─────┴──────┐
   │   pages/   │  ← home, login, dashboard, resume_analyzer,
   │            │     mock_interview, voice_interview,
   └─────┬──────┘     career_advisor, about
         ↓
   ┌─────┴──────┐
   │  services/ │  ← ai_service.py (Gemini API)
   │            │     voice_service.py (SpeechRecognition)
   └─────┬──────┘
         ↓
   ┌─────┴──────┐
   │   utils/   │  ← auth.py, resume_parser.py, charts.py, styles.py
   └─────┬──────┘
         ↓
   ┌─────┴──────┐
   │ database/  │  ← db.py (SQLite: users, resumes, interviews, scores, feedback)
   └────────────┘
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Streamlit 1.35 |
| **Backend** | Python 3.10+ |
| **AI Engine** | Google Gemini 1.5 Flash |
| **Database** | SQLite 3 |
| **PDF Parsing** | pdfplumber + PyPDF2 |
| **DOCX Parsing** | python-docx |
| **Voice** | SpeechRecognition + Google Speech API |
| **Charts** | Plotly |
| **Auth** | bcrypt |
| **Env Config** | python-dotenv |

---

## 🛠️ Installation

### Prerequisites

- Python 3.10 or higher
- pip
- A Google Gemini API key ([Get one free](https://makersuite.google.com/app/apikey))
- (Optional) Microphone for voice interview

### Step 1 — Clone the repository

```bash
git clone https://github.com/rupammukherjee/AI-Interview-Agent.git
cd AI-Interview-Agent
```

### Step 2 — Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

> **Note for Linux/Mac:** PyAudio requires PortAudio.
> ```bash
> # Ubuntu/Debian
> sudo apt-get install portaudio19-dev
> # macOS
> brew install portaudio
> ```

### Step 4 — Configure environment

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=any_random_string_here
```

### Step 5 — Run the app

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## ⚙️ Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | ✅ Yes |
| `SECRET_KEY` | Session security key | ✅ Yes |

Get your free Gemini API key at: https://makersuite.google.com/app/apikey

---

## 🚀 Usage

### 1. Register & Login
- Create an account with your email and password
- Login to access all features

### 2. Upload Resume
- Go to **Resume Analyzer**
- Upload your PDF or DOCX resume
- Select target job role
- Click **Analyze Resume** — get ATS score, skills, gaps, and suggestions

### 3. Mock Interview
- Go to **Mock Interview**
- Select job role, difficulty, number of questions
- Answer AI-generated questions in text
- Submit for AI evaluation and feedback

### 4. Voice Interview
- Go to **Voice Interview**
- Connect a microphone
- Click **Record Answer** for each question
- Speak your answer (up to 30 seconds)
- Submit for evaluation

### 5. Career Advisor
- Go to **Career Advisor** (requires uploaded resume)
- Get personalized career paths, certifications, courses, and tech stack recommendations

---

## 📁 Project Structure

```
AI-Interview-Agent/
│
├── app.py                      # Main entry point + navigation router
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
│
├── assets/                     # Static assets (images, icons)
├── docs/                       # Documentation files
├── ppt/                        # Presentation files
├── reports/                    # Project report
├── screenshots/                # App screenshots
│
├── database/
│   ├── __init__.py
│   └── db.py                   # SQLite schema + all CRUD operations
│
├── pages/
│   ├── __init__.py
│   ├── home.py                 # Landing page
│   ├── login.py                # Login page
│   ├── register.py             # Registration page
│   ├── dashboard.py            # User dashboard with charts
│   ├── resume_analyzer.py      # Resume upload + ATS analysis
│   ├── mock_interview.py       # Text-based mock interview
│   ├── voice_interview.py      # Voice-based interview
│   ├── career_advisor.py       # AI career advice
│   └── about.py                # About / project info
│
├── services/
│   ├── __init__.py
│   ├── ai_service.py           # All Gemini API calls
│   └── voice_service.py        # SpeechRecognition helpers
│
├── utils/
│   ├── __init__.py
│   ├── auth.py                 # Auth: hashing, sessions, login/register
│   ├── resume_parser.py        # PDF + DOCX text extraction
│   ├── charts.py               # Plotly chart helpers
│   └── styles.py               # Global CSS (glassmorphism dark theme)
│
├── models/
│   └── __init__.py
│
└── tests/
    ├── __init__.py
    ├── test_auth.py             # Auth unit tests
    ├── test_resume_parser.py    # Resume parser unit tests
    ├── test_database.py         # Database integration tests
    └── test_cases.md            # Manual test case documentation
```

---

## 🌍 SDG Mapping

### SDG 8 — Decent Work and Economic Growth
This platform directly contributes to SDG 8 by:
- Bridging the skill gap between education and the job market
- Providing free AI-powered interview preparation accessible to all
- Increasing employment outcomes for fresh graduates and job seekers
- Supporting youth skill development aligned with industry needs

### SDG 4 — Quality Education
This platform contributes to SDG 4 by:
- Delivering personalized, adaptive learning experiences
- Providing structured feedback and curated learning paths
- Democratizing access to quality interview coaching
- Recommending courses, certifications, and resources for upskilling

---

## 🔭 Future Scope

- [ ] **Multi-language support** — Hindi, Bengali, Tamil, and other regional languages
- [ ] **Real-time video interview** — Facial expression and posture analysis via webcam
- [ ] **Company-specific prep** — Google, Amazon, Microsoft interview tracks
- [ ] **Peer mock interviews** — Match users for live practice sessions
- [ ] **Mobile app** — React Native / Flutter client
- [ ] **Resume builder** — AI-assisted resume creation and formatting
- [ ] **Job board integration** — Direct job application from the platform
- [ ] **LMS integration** — Link with Coursera, Udemy, NPTEL APIs
- [ ] **Interview recording** — Save voice sessions for self-review
- [ ] **Competitive leaderboard** — Gamified preparation with peer rankings

---

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_auth.py -v
python -m pytest tests/test_database.py -v
python -m pytest tests/test_resume_parser.py -v
```

---

## ☁️ Deployment

### Streamlit Cloud (Free)

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → connect your GitHub repo
4. Set **Main file path**: `app.py`
5. Under **Advanced settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   SECRET_KEY = "your_secret_key"
   ```
6. Click **Deploy** — your app will be live in ~2 minutes

### Local with Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

```bash
docker build -t ai-interview-agent .
docker run -p 8501:8501 --env-file .env ai-interview-agent
```

---

## 👨‍💻 Author

<div align="center">

**Rupam Mukherjee**

B.Tech CSE (AI & ML) · Techno India University

*Semester 6 — Entrepreneurship & Skill Development (ESD) Project*

[![GitHub](https://img.shields.io/badge/GitHub-@rupammukherjee-181717?style=flat-square&logo=github)](https://github.com/rupam179)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/rupam-mukherjee-647a092b0)

</div>

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ using Python · Streamlit · Google Gemini AI

⭐ Star this repository if you found it helpful!

</div>
