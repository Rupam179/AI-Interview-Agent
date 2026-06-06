# Viva Questions and Answers
## AI Interview Preparation Agent

---

### SECTION 1: Project Overview

**Q1. What is the AI Interview Agent and what problem does it solve?**

A: The AI Interview Agent is a web-based platform built using Python, Streamlit, and Google Gemini AI that helps students and job seekers prepare for technical and HR interviews. It solves the problem of unequal access to quality interview preparation — specifically: (a) the lack of personalised, resume-aware practice, (b) the high cost of coaching, (c) no real-time AI feedback, and (d) poor ATS awareness among candidates.

---

**Q2. Which UN Sustainable Development Goals does your project align with?**

A: The project aligns with two SDGs:
- **SDG 8 — Decent Work and Economic Growth** (Primary): By improving interview success rates and employability, it contributes to productive employment and economic growth, particularly for youth.
- **SDG 4 — Quality Education** (Secondary): By delivering personalised, adaptive learning experiences and recommending learning resources, it contributes to quality education and lifelong learning.

---

**Q3. What makes your project unique compared to existing solutions like LeetCode or InterviewBit?**

A: Three key differentiators:
1. **Resume-aware personalisation** — questions are generated from the candidate's actual resume, not a generic question bank
2. **End-to-end integration** — ATS analysis, interview, evaluation, feedback, and career advice all in one platform
3. **Voice interview with AI evaluation** — no existing free platform evaluates spoken answers with AI scoring across technical, communication, and confidence dimensions

---

### SECTION 2: Technical Architecture

**Q4. Explain the system architecture of your project.**

A: The system follows a layered architecture with four layers:
1. **Presentation Layer** — Streamlit pages (home, login, dashboard, resume analyzer, mock interview, voice interview, career advisor, about)
2. **Application Layer** — `app.py` handles routing via `session_state`; pages call services and utils
3. **Service Layer** — `ai_service.py` (all Gemini API calls) and `voice_service.py` (speech recognition)
4. **Data Layer** — `database/db.py` manages a SQLite database with five tables: users, resumes, interviews, scores, feedback

External services: Google Gemini 1.5 Flash API and Google Speech-to-Text API.

---

**Q5. Why did you choose Streamlit over Flask or Django?**

A: For this project, Streamlit was the optimal choice because:
- **Rapid development** — interactive UI in pure Python, no HTML/CSS/JS needed
- **Built-in state management** — `session_state` handles auth and page routing
- **Native Plotly integration** — charts render with one line of code
- **File uploader widget** — handles PDF/DOCX upload natively
- **Cloud deployment** — Streamlit Cloud provides free one-click deployment

Flask/Django would be better for a production multi-user API-first architecture, which I've noted as a future scope item.

---

**Q6. Why SQLite and not MySQL or PostgreSQL?**

A: SQLite was chosen because:
- **Zero configuration** — no server to install or maintain
- **Portable** — single `.db` file, version-controllable
- **Built-in Python support** — `sqlite3` module requires no additional install
- **Sufficient for scope** — the project is a single-user/demo application

For production deployment with concurrent users, I would migrate to PostgreSQL, which I've documented in the future scope.

---

**Q7. How does the authentication system work?**

A: 
1. **Registration:** Password is hashed using `bcrypt.hashpw()` with a random salt before storage. The salt is embedded in the hash, so we never store the plain text.
2. **Login:** `bcrypt.checkpw()` verifies the provided password against the stored hash — the function internally extracts the salt from the hash and reapplies it.
3. **Sessions:** On successful login, the user dict is stored in Streamlit's `session_state`. The `is_logged_in()` function checks if this key exists.
4. **Logout:** Clears all relevant session keys and triggers a page rerun.

---

### SECTION 3: AI & Machine Learning

**Q8. How do you use the Gemini API in your project?**

A: I use Gemini 1.5 Flash for four AI tasks:
1. **Resume Analysis** — structured prompt requesting JSON with skills, missing_skills, ats_score, suggestions, summary
2. **Question Generation** — prompt with role, difficulty, resume text; returns JSON array of questions with type and expected keywords
3. **Answer Evaluation** — prompt with all Q&A pairs; returns scores and per-question feedback in JSON
4. **Career Advice** — prompt with skills and resume summary; returns career paths, certifications, courses, technologies

All prompts explicitly request JSON-only responses with no markdown, and I use a `_safe_json()` helper to strip any accidentally included markdown fences before parsing.

---

**Q9. What is ATS and how do you compute the ATS score?**

A: ATS stands for Applicant Tracking System — software used by companies to filter resumes before human review. My ATS score is computed by the Gemini model based on factors like:
- Keyword density for the target role
- Presence of quantified achievements
- Standard section headings (Education, Experience, Skills)
- Formatting compatibility (no complex tables or graphics)
- Length and readability

The score is returned as an integer 0–100 in the AI's JSON response. This is an AI-estimated ATS score, not a real commercial ATS parsing tool.

---

**Q10. How does the voice interview work technically?**

A: 
1. The `SpeechRecognition` library accesses the system microphone via `PyAudio`
2. `recognizer.adjust_for_ambient_noise()` calibrates to background noise for 0.5 seconds
3. `recognizer.listen()` captures audio with a 10-second timeout and 30-second phrase limit
4. The audio is sent to **Google's free Speech-to-Text API** via `recognizer.recognize_google()`
5. The transcribed text is then evaluated by Gemini exactly like a typed text answer

Three exception types are handled: `WaitTimeoutError`, `UnknownValueError`, and `RequestError`. A text fallback input is always available.

---

**Q11. How does the evaluation engine score answers?**

A: All question-answer pairs from the interview are assembled into a numbered list and sent to Gemini with the job role and difficulty as context. The prompt requests:
- **Technical Score (0–100):** Correctness, depth, and accuracy of technical content
- **Communication Score (0–100):** Clarity, structure, and vocabulary quality
- **Confidence Score (0–100):** Inferred from completeness and directness of responses
- **Overall Score (0–100):** Weighted aggregate
- **Per-question feedback:** Score out of 10 + one-sentence comment

The evaluation uses the Gemini model's language understanding capabilities to judge semantic quality, not just keyword matching.

---

### SECTION 4: Database & Data Design

**Q12. Describe your database schema.**

A: The database has five normalised tables:
1. **users** — id, name, email (unique), password (bcrypt hash), timestamps
2. **resumes** — id, user_id (FK), filename, extracted_text, skills (JSON), missing_skills (JSON), ats_score, suggestions (JSON)
3. **interviews** — id, user_id (FK), resume_id (FK), job_role, difficulty, interview_type, questions (JSON), answers (JSON), timestamps
4. **scores** — id, interview_id (FK), user_id (FK), overall/technical/communication/confidence scores
5. **feedback** — id, interview_id (FK), user_id (FK), strengths/weaknesses/improvements/learning_path (all JSON)

JSON arrays are stored as TEXT in SQLite (standard practice for SQLite when column cardinality is low).

---

**Q13. Why do you store JSON arrays in SQLite TEXT columns?**

A: SQLite doesn't have a native array or JSON column type (unlike PostgreSQL's JSONB). Storing as TEXT is standard practice for SQLite when:
- The data is always read/written as a unit (never queried element-by-element at the SQL level)
- The Python layer handles all array operations via `json.loads()`/`json.dumps()`

This is appropriate here since we always retrieve the full skills list or learning path as a unit. For a production system with PostgreSQL, I would use JSONB columns or a separate junction table.

---

### SECTION 5: UI/UX Design

**Q14. How did you implement the glassmorphism dark-mode UI?**

A: Using Streamlit's `st.markdown(..., unsafe_allow_html=True)` to inject custom CSS. Key CSS techniques:
- **Dark background:** `background: #0d0f1a` with radial gradient overlays for depth
- **Glass cards:** `background: rgba(255,255,255,0.05)` with `backdrop-filter: blur(16px)` and subtle white borders
- **Gradient text:** `background: linear-gradient(135deg, #6c63ff, #00d4ff)` with `-webkit-background-clip: text`
- **Gradient buttons:** Linear gradient background with box-shadow glow on hover
- **Score badges:** Conditional CSS classes (`score-high`, `score-mid`, `score-low`) based on score thresholds

All CSS is centralised in `utils/styles.py` and injected via an `inject_css()` function called at the top of each page.

---

### SECTION 6: Testing & Quality

**Q15. How did you test your project?**

A: Three levels of testing:
1. **Unit Tests** (`tests/test_auth.py`): Test password hashing, verification, edge cases using Python's `unittest` framework
2. **Integration Tests** (`tests/test_database.py`): Test all CRUD operations against a temporary SQLite test database (using `tempfile.NamedTemporaryFile`)
3. **Manual Test Cases** (`tests/test_cases.md`): 37 documented end-to-end test cases covering all 8 modules

Total: 56 test cases, 100% pass rate.

---

**Q16. What security vulnerabilities did you address?**

A: 
- **SQL Injection:** All database queries use parameterized statements (`cursor.execute("... WHERE id = ?", (user_id,))`) — never string concatenation
- **Password Security:** bcrypt with random salts — plain text never stored; rainbow table attacks ineffective
- **Session Security:** User data stored only in server-side `session_state`, not in cookies or URLs
- **Route Protection:** Every authenticated page checks `is_logged_in()` before rendering; unauthenticated access redirects to login
- **Data Isolation:** All queries filter by `user_id`, so users cannot access each other's data

---

### SECTION 7: Deployment

**Q17. How do you deploy this project?**

A: Three deployment options:
1. **Local:** Clone repo → create venv → `pip install -r requirements.txt` → add `.env` file → `streamlit run app.py`
2. **Streamlit Cloud (Free):** Push to GitHub → connect at share.streamlit.io → set secrets in UI → deploy in ~2 minutes
3. **Docker:** Build with the provided Dockerfile → run with `docker run -p 8501:8501 --env-file .env`

For production scale, I would deploy on a VPS (AWS EC2/GCP) with PostgreSQL replacing SQLite and nginx as a reverse proxy.

---

**Q18. What would you change to make this production-ready?**

A:
1. Replace SQLite with **PostgreSQL** for concurrent access
2. Add **rate limiting** to prevent API abuse
3. Implement **email verification** during registration
4. Add **HTTPS** via Let's Encrypt / Cloudflare
5. Use **environment variable management** with a secrets manager (AWS Secrets Manager)
6. Implement **logging** with structured log aggregation
7. Add **Celery + Redis** for async Gemini API calls (currently blocking)
8. Set up **CI/CD** pipeline with GitHub Actions

---

### SECTION 8: Conceptual Questions

**Q19. What is a Large Language Model (LLM)?**

A: An LLM is a type of neural network trained on massive text datasets using transformer architecture and self-supervised learning. It learns statistical patterns of language at scale, enabling it to generate coherent, contextually appropriate text. Google Gemini is built on the transformer architecture with multi-head attention mechanisms. LLMs are used in this project for tasks requiring language understanding and generation: question creation, answer evaluation, and career advice.

---

**Q20. What is prompt engineering and how did you use it?**

A: Prompt engineering is the practice of designing input text (prompts) to guide an LLM toward producing specific, desired outputs. In this project, I used several techniques:
- **Role assignment:** "You are a senior Software Engineer interviewer" — sets the model's persona
- **Format specification:** "Respond ONLY with valid JSON, no markdown" — ensures parseable output
- **Context injection:** Including the resume text as context for personalisation
- **Output schema:** Providing the exact JSON structure expected, which the model fills in
- **Constraint specification:** "60% technical, 40% HR questions" — controls output distribution

---

**Q21. What is bcrypt and why is it better than MD5 or SHA-256 for passwords?**

A: bcrypt is a password hashing algorithm designed specifically for password storage. It is better than MD5/SHA-256 because:
1. **Salt:** bcrypt automatically generates a random salt for each hash, making identical passwords produce different hashes and defeating rainbow tables
2. **Work factor:** bcrypt has a configurable "cost factor" that makes hashing computationally expensive, slowing down brute-force attacks
3. **MD5/SHA-256** are fast cryptographic hash functions — good for data integrity, but their speed makes them vulnerable to GPU-accelerated brute-force attacks
4. bcrypt is specifically designed for slow, secure password hashing with the `$2b$` format storing salt and cost factor in the hash string itself

---

**Q22. How does speech recognition work in your system?**

A: The process has four steps:
1. **Audio capture:** `PyAudio` accesses the microphone at the OS level and captures raw PCM audio
2. **Preprocessing:** The `SpeechRecognition` library applies noise adjustment and formats the audio as a WAV stream
3. **API call:** The WAV data is sent via HTTPS to Google's Speech-to-Text API, which uses a deep learning acoustic model trained on millions of hours of speech
4. **Response:** The API returns the most probable transcript as a text string, which we use as the interview answer

The system uses the free tier of Google Speech-to-Text, which supports English at no cost for reasonable usage.

---

*End of Viva Q&A — AI Interview Agent*
*Rupam Mukherjee | Techno India University | 2023–2024*
