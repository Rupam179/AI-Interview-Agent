# AI Interview Agent — 15-Slide PowerPoint Content

---

## SLIDE 1: TITLE SLIDE

**Title:** AI Interview Preparation Agent
**Subtitle:** An AI-Powered Platform for Smart Interview Preparation

**Presented by:** Rupam Mukherjee
**Programme:** B.Tech CSE (AI & ML) — Semester 6
**Institution:** Techno India University, West Bengal
**Year:** 2023–2024

**Bottom tag:** Powered by Google Gemini AI · SDG 8 & SDG 4

---

## SLIDE 2: INTRODUCTION

**Heading:** What is AI Interview Agent?

**Key Points:**
- A fully functional AI-powered web platform for interview preparation
- Built with Python, Streamlit, and Google Gemini 1.5 Flash
- Helps students and job seekers prepare for technical & HR interviews
- Supports 7 job roles × 3 difficulty levels
- Voice and text interview modes
- Free, personalised, and data-driven

**Visual:** Central diagram showing Resume → AI → Interview → Feedback → Job

---

## SLIDE 3: PROBLEM STATEMENT

**Heading:** The Problem We're Solving

**Statistics Box:**
- 70% of candidates fail interviews due to poor preparation (NACE, 2022)
- 1.5 Million engineering graduates enter India's job market annually
- 72% of resumes rejected by ATS before human review (Mainak Pal, 2022)
- Professional coaching costs ₹5,000–₹50,000 per program

**Challenges:**
1. No personalised, resume-aware practice
2. High cost of quality coaching
3. No real-time AI feedback
4. No ATS optimisation awareness
5. No voice practice with AI evaluation

---

## SLIDE 4: OBJECTIVES

**Heading:** Project Objectives

**8 Objectives:**
1. Develop a fully functional AI interview preparation platform
2. Implement resume parsing with ATS scoring and skill gap analysis
3. Generate personalised questions using Google Gemini LLM
4. Enable voice interviews with real-time speech recognition
5. Create a multi-dimensional AI evaluation engine
6. Provide personalised feedback with learning roadmaps
7. Build a career advisor for path guidance
8. Design a modern, production-grade UI

---

## SLIDE 5: SDG MAPPING

**Heading:** Aligned with UN Sustainable Development Goals

**SDG 8 — Decent Work & Economic Growth (PRIMARY)**
- Bridges skill gap between education and employment
- Provides free AI coaching to all students
- Increases interview success rates
- Supports youth employment and skill development

**SDG 4 — Quality Education (SECONDARY)**
- Personalized adaptive learning
- Structured feedback and learning paths
- Democratizes access to quality preparation
- Recommends curated courses and certifications

**Visual:** SDG 8 orange badge and SDG 4 red badge with icons

---

## SLIDE 6: EXISTING SYSTEM — LIMITATIONS

**Heading:** Why Existing Tools Fall Short

| Platform | What It Does | Key Limitation |
|----------|-------------|----------------|
| InterviewBit | Question banks | No resume personalisation |
| Pramp | Peer interviews | Needs another user |
| LeetCode | Coding practice | Technical only |
| HireVue | Video interviews | Expensive, B2B |
| ChatGPT | Q&A | No structured workflow |

**Common Gaps:**
- No end-to-end integrated pipeline
- No resume-to-question linkage
- No ATS + interview in one platform
- No free, AI-evaluated voice mode

---

## SLIDE 7: PROPOSED SYSTEM

**Heading:** Our Solution — AI Interview Agent

**End-to-End Pipeline:**
```
Upload Resume → ATS Analysis → Generate Questions
      → Text / Voice Interview → AI Evaluation
            → Personalized Feedback → Career Roadmap
```

**Unique Value Propositions:**
✅ Resume-aware question generation
✅ Voice interview with speech-to-text
✅ 4-dimensional scoring (Technical, Communication, Confidence, Overall)
✅ Persistent progress dashboard
✅ Free, open-source, no subscription needed

---

## SLIDE 8: SYSTEM ARCHITECTURE

**Heading:** Technical Architecture

**3-Layer Diagram:**

```
[STREAMLIT UI LAYER]
 Home | Login | Dashboard | Resume | Mock | Voice | Career

        ↓ session_state routing ↓

[APPLICATION LAYER]
 AI Service (Gemini)  |  Voice Service (SpeechRecognition)
 Auth Utils           |  Resume Parser  |  Chart Builder

        ↓ CRUD operations ↓

[DATA LAYER]
 SQLite Database
 users · resumes · interviews · scores · feedback
```

**External APIs:** Google Gemini 1.5 Flash · Google Speech-to-Text

---

## SLIDE 9: KEY FEATURES

**Heading:** Platform Features at a Glance

**8 Feature Cards:**

🔐 **Authentication** — Secure register/login/logout with bcrypt hashing

📄 **Resume Analyzer** — Upload PDF/DOCX → ATS score, skill extraction, gap analysis, suggestions

💬 **Mock Interview** — AI generates 5–15 personalised questions per session

🎙️ **Voice Interview** — Speak answers, real-time transcription, same AI evaluation

📊 **Evaluation Engine** — Scores: Technical / Communication / Confidence / Overall (0–100)

💡 **Feedback System** — Strengths, weaknesses, improvements, learning path

📈 **Dashboard** — Score trends, radar chart, ATS gauge, interview history

🧭 **Career Advisor** — Career paths, certifications, courses, tech recommendations

---

## SLIDE 10: TECHNOLOGY STACK

**Heading:** Technologies Used

**Two-column layout:**

| Category | Technology | Version |
|----------|-----------|---------|
| Frontend | Streamlit | 1.35 |
| AI Engine | Google Gemini 1.5 Flash | — |
| Database | SQLite 3 | Built-in |
| PDF Parse | pdfplumber + PyPDF2 | Latest |
| DOCX Parse | python-docx | 1.1.2 |
| Voice | SpeechRecognition | 3.10.4 |
| Charts | Plotly | 5.22.0 |
| Auth | bcrypt | 4.1.3 |
| Env | python-dotenv | 1.0.1 |
| Language | Python | 3.10+ |

---

## SLIDE 11: WORKFLOW DIAGRAMS

**Heading:** How It Works

**Interview Flow:**
1. 🔐 Register / Login
2. 📄 Upload Resume → AI Analysis
3. ⚙️ Select: Job Role + Difficulty + Mode
4. 🤖 AI Generates Personalised Questions
5. 🗣️ Answer: Type or Speak
6. 📊 AI Evaluates All Answers
7. 💾 Save to Database
8. 📈 View Results + Feedback
9. 🧭 Get Career Guidance

**Gemini Prompt Design (simplified):**
> "You are a [role] interviewer. Generate [N] [difficulty]-level questions based on this resume. Return JSON."

---

## SLIDE 12: SCREENSHOTS / UI DEMO

**Heading:** Application Screenshots

*(In actual PPT — add screenshots here)*

**Screenshot Descriptions:**
1. **Home Page** — Hero section with feature cards and SDG badges (dark glassmorphism)
2. **Dashboard** — KPI cards + score trend line chart + ATS gauge
3. **Resume Analyzer** — File upload + ATS gauge + skill chips (green/red)
4. **Mock Interview** — Question card with type badge + answer textarea + navigator
5. **Voice Interview** — Record button + transcription display
6. **Results Page** — Radar chart + bar chart + per-question feedback
7. **Career Advisor** — Career path cards + certifications/courses/tech tabs

---

## SLIDE 13: RESULTS & ACHIEVEMENTS

**Heading:** Project Results

**Feature Completion:** 15/15 features fully implemented ✅

**Performance:**
| Metric | Value |
|--------|-------|
| Question generation | 8–12 seconds |
| AI evaluation (10 Q) | 15–25 seconds |
| Resume analysis | 10–18 seconds |
| Voice recognition | <3 seconds |
| Test pass rate | 56/56 (100%) |

**Test Coverage:**
- 56 test cases across unit + integration + manual tests
- All 56 passed ✅

---

## SLIDE 14: FUTURE SCOPE

**Heading:** What's Next?

**Near-Term (6 months):**
- 🌐 Multi-language support (Hindi, Bengali, Tamil)
- 📱 Mobile app (React Native)
- 🎥 Video interview with facial expression analysis
- 🏢 Company-specific tracks (FAANG, unicorns)

**Mid-Term (1 year):**
- 👥 Peer practice matching
- 📝 AI-powered resume builder
- 💼 Job board integration (Naukri, LinkedIn)
- 🎮 Gamification (badges, streaks, leaderboard)

**Long-Term:**
- 🏗️ PostgreSQL migration for production scale
- 🤝 B2B HR screening edition
- 📡 API-first architecture for third-party integration

---

## SLIDE 15: THANK YOU

**Heading:** Thank You!

**Center text:**
AI Interview Agent — Bridging the Gap Between Learning and Earning

**Author Block:**
Rupam Mukherjee
B.Tech CSE (AI & ML) | Techno India University
[GitHub Link] | [LinkedIn Link]

**Mentor:**
[Faculty Guide Name]
Department of CSE, Techno India University

**Footer:**
🌍 SDG 8: Decent Work & Economic Growth | SDG 4: Quality Education

**GitHub Repository:** github.com/rupammukherjee/AI-Interview-Agent

---
*End of PPT Content*
