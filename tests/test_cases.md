# Test Cases — AI Interview Agent

## TC-01: User Registration

| # | Test Case | Input | Expected Output | Status |
|---|-----------|-------|-----------------|--------|
| 1 | Valid registration | Name, unique email, password ≥6 chars | Account created, redirect to login | PASS |
| 2 | Duplicate email | Already registered email | Error: "Email already registered" | PASS |
| 3 | Short password | Password with 3 chars | Error: "Password must be at least 6 characters" | PASS |
| 4 | Mismatched passwords | password ≠ confirm | Error: "Passwords do not match" | PASS |
| 5 | Empty fields | Any field blank | Error: "Please fill in all fields" | PASS |

---

## TC-02: User Login

| # | Test Case | Input | Expected Output | Status |
|---|-----------|-------|-----------------|--------|
| 1 | Valid credentials | Correct email + password | Login success, redirect to dashboard | PASS |
| 2 | Wrong password | Correct email, wrong password | Error: "Invalid email or password" | PASS |
| 3 | Non-existent email | Unknown email | Error: "Invalid email or password" | PASS |
| 4 | Empty email | Blank email field | Error: "Please fill in all fields" | PASS |

---

## TC-03: Resume Upload & Analysis

| # | Test Case | Input | Expected Output | Status |
|---|-----------|-------|-----------------|--------|
| 1 | Valid PDF upload | .pdf file | Text extracted, ATS score displayed | PASS |
| 2 | Valid DOCX upload | .docx file | Text extracted, skills identified | PASS |
| 3 | Unsupported format | .txt file | Blocked by Streamlit file uploader | PASS |
| 4 | Empty PDF | Corrupt/empty PDF | Error message returned gracefully | PASS |
| 5 | ATS score range | Any resume | Score between 0–100 | PASS |
| 6 | Skills identified | Resume with skills | List of skills returned | PASS |
| 7 | Missing skills | Resume missing common skills | Missing skills highlighted | PASS |
| 8 | Suggestions returned | Any resume | ≥1 AI suggestion displayed | PASS |

---

## TC-04: Mock Interview

| # | Test Case | Input | Expected Output | Status |
|---|-----------|-------|-----------------|--------|
| 1 | Question generation | Job role + difficulty | N questions generated | PASS |
| 2 | Correct question count | num_q = 10 | Exactly 10 questions shown | PASS |
| 3 | Question navigation | Click Next / Previous | Moves between questions | PASS |
| 4 | Answer saving | Type answer + click Next | Answer preserved on return | PASS |
| 5 | Submit all answers | Click Submit | Evaluation triggered | PASS |
| 6 | Score returned | Submit answers | Scores 0–100 for all categories | PASS |
| 7 | Feedback generated | Evaluation complete | Strengths, weaknesses, improvements shown | PASS |
| 8 | Learning path | After evaluation | ≥1 learning path item shown | PASS |
| 9 | Interview saved to DB | Complete interview | Row in interviews + scores tables | PASS |

---

## TC-05: Voice Interview

| # | Test Case | Input | Expected Output | Status |
|---|-----------|-------|-----------------|--------|
| 1 | Microphone detection | With mic connected | Mic list displayed | PASS |
| 2 | No microphone | Without mic | Error: "No microphone found" | PASS |
| 3 | Speech recognition | Speak clearly | Answer transcribed to text | PASS |
| 4 | Unrecognized speech | Background noise | Error: "Could not understand audio" | PASS |
| 5 | Text fallback | Type in fallback box | Answer saved as typed text | PASS |
| 6 | Voice interview evaluation | Submit voice answers | Scores and feedback generated | PASS |

---

## TC-06: Dashboard

| # | Test Case | Input | Expected Output | Status |
|---|-----------|-------|-----------------|--------|
| 1 | KPI cards display | After login | Total interviews, avg score, ATS shown | PASS |
| 2 | Score trend chart | After interviews | Line chart rendered | PASS |
| 3 | ATS gauge | After resume upload | Gauge chart with correct score | PASS |
| 4 | Interview history table | After interviews | Table with date, role, score | PASS |
| 5 | No data state | New user | Info messages, no crashes | PASS |

---

## TC-07: Career Advisor

| # | Test Case | Input | Expected Output | Status |
|---|-----------|-------|-----------------|--------|
| 1 | No resume state | No resume uploaded | Prompt to upload resume | PASS |
| 2 | Career paths | Resume uploaded | ≥1 career path with salary | PASS |
| 3 | Certifications | Resume uploaded | ≥1 certification with provider | PASS |
| 4 | Courses | Resume uploaded | ≥1 course with platform | PASS |
| 5 | Technologies | Resume uploaded | ≥1 technology with reason | PASS |
| 6 | Roadmap | Resume uploaded | 6–12 month roadmap paragraph | PASS |

---

## TC-08: Security

| # | Test Case | Input | Expected Output | Status |
|---|-----------|-------|-----------------|--------|
| 1 | Password hashing | Plain text password | bcrypt hash stored, not plain text | PASS |
| 2 | Protected routes | Unauthenticated access | Redirect to login page | PASS |
| 3 | Session isolation | Two users | Each user sees only their own data | PASS |
| 4 | SQL injection attempt | Malicious SQL in input | SQLite parameterized queries block it | PASS |
