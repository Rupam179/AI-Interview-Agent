"""
services/ai_service.py
All Gemini AI calls: resume analysis, question generation, evaluation, feedback, career advice.
"""

import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

_model = None


def _get_model():
    global _model
    if _model is None:
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set. Please add it to your .env file.")
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel("gemini-2.0-flash-lite")
    return _model


def _safe_json(text: str) -> dict | list:
    """Strip markdown fences and parse JSON safely."""
    clean = re.sub(r"```(?:json)?|```", "", text).strip()
    return json.loads(clean)


# ─── Resume Analysis ──────────────────────────────────────────────────────────

def analyze_resume(resume_text: str, job_role: str = "Software Engineer") -> dict:
    prompt = f"""
You are an expert ATS (Applicant Tracking System) and career coach.

Analyze the following resume for a {job_role} position and respond ONLY with valid JSON (no markdown, no extra text):

{{
  "skills": ["list of identified technical and soft skills"],
  "missing_skills": ["important skills missing for a {job_role}"],
  "ats_score": <integer 0-100>,
  "suggestions": ["actionable improvement suggestion 1", "suggestion 2", "suggestion 3", "suggestion 4", "suggestion 5"],
  "summary": "2-3 sentence professional summary of the candidate"
}}

Resume:
{resume_text[:3000]}
"""
    model = _get_model()
    response = model.generate_content(prompt)
    try:
        return _safe_json(response.text)
    except Exception:
        return {
            "skills": ["Could not parse skills"],
            "missing_skills": [],
            "ats_score": 50,
            "suggestions": ["Please check resume format"],
            "summary": response.text[:300],
        }


# ─── Question Generation ──────────────────────────────────────────────────────

def generate_questions(
    resume_text: str,
    job_role: str,
    difficulty: str,
    num_questions: int = 10,
) -> list[dict]:
    prompt = f"""
You are a senior {job_role} interviewer.

Generate {num_questions} interview questions for a {difficulty}-level {job_role} candidate.
Base the questions on the resume below. Mix technical questions (~60%) and HR/behavioral questions (~40%).

Respond ONLY with a valid JSON array (no markdown):
[
  {{
    "question": "...",
    "type": "technical" or "hr" or "behavioral",
    "expected_keywords": ["keyword1", "keyword2", "keyword3"]
  }},
  ...
]

Resume:
{resume_text[:2000]}
"""
    model = _get_model()
    response = model.generate_content(prompt)
    try:
        return _safe_json(response.text)
    except Exception:
        return [{"question": q, "type": "technical", "expected_keywords": []}
                for q in response.text.split("\n") if q.strip()]


# ─── Answer Evaluation ────────────────────────────────────────────────────────

def evaluate_answers(questions_and_answers: list[dict], job_role: str, difficulty: str) -> dict:
    qa_text = "\n\n".join(
        [f"Q{i+1} [{qa['type']}]: {qa['question']}\nA{i+1}: {qa.get('answer','(no answer provided)')}"
         for i, qa in enumerate(questions_and_answers)]
    )

    prompt = f"""
You are an expert {job_role} interview evaluator.

Evaluate the following interview responses for a {difficulty}-level {job_role} position.
Be constructive but honest.

Respond ONLY with valid JSON (no markdown):
{{
  "overall_score": <integer 0-100>,
  "technical_score": <integer 0-100>,
  "communication_score": <integer 0-100>,
  "confidence_score": <integer 0-100>,
  "per_question": [
    {{"question": "...", "score": <0-10>, "comment": "brief feedback"}}
  ],
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "weaknesses": ["weakness 1", "weakness 2"],
  "improvements": ["what to improve 1", "what to improve 2", "what to improve 3"],
  "learning_path": [
    {{"topic": "...", "resource": "course/book/platform name"}}
  ]
}}

Interview Q&A:
{qa_text[:4000]}
"""
    model = _get_model()
    response = model.generate_content(prompt)
    try:
        return _safe_json(response.text)
    except Exception:
        return {
            "overall_score": 60,
            "technical_score": 60,
            "communication_score": 60,
            "confidence_score": 60,
            "per_question": [],
            "strengths": ["Attempted all questions"],
            "weaknesses": ["Needs more detail"],
            "improvements": ["Practice more", "Study core concepts"],
            "learning_path": [{"topic": "Core concepts", "resource": "LeetCode, Coursera"}],
        }


# ─── Career Advisor ───────────────────────────────────────────────────────────

def get_career_advice(resume_text: str, skills: list[str]) -> dict:
    skills_str = ", ".join(skills) if skills else "general software skills"
    prompt = f"""
You are an expert career advisor for tech professionals.

Based on the candidate's skills ({skills_str}) and resume, provide personalized career advice.

Respond ONLY with valid JSON (no markdown):
{{
  "career_paths": [
    {{"title": "...", "description": "...", "salary_range": "...", "growth": "..."}}
  ],
  "certifications": [
    {{"name": "...", "provider": "...", "relevance": "..."}}
  ],
  "courses": [
    {{"title": "...", "platform": "...", "duration": "..."}}
  ],
  "technologies": [
    {{"name": "...", "reason": "..."}}
  ],
  "roadmap": "A concise 6-12 month personalized learning roadmap paragraph"
}}

Resume summary:
{resume_text[:1500]}
"""
    model = _get_model()
    response = model.generate_content(prompt)
    try:
        return _safe_json(response.text)
    except Exception:
        return {
            "career_paths": [{"title": "Software Engineer", "description": "Build software products",
                              "salary_range": "6-20 LPA", "growth": "High"}],
            "certifications": [{"name": "AWS Certified Developer", "provider": "Amazon",
                                "relevance": "Cloud skills"}],
            "courses": [{"title": "Full Stack Web Development", "platform": "Coursera",
                         "duration": "6 months"}],
            "technologies": [{"name": "Docker", "reason": "DevOps foundation"}],
            "roadmap": "Focus on strengthening your core skills over the next 6 months.",
        }