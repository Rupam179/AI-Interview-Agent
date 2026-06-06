"""
pages/mock_interview.py
Text-based mock interview: question generation → answer collection → AI evaluation → feedback.
"""

import json
import streamlit as st
from utils.auth import is_logged_in, get_current_user
from utils.styles import page_header
from utils.charts import radar_chart, score_bar_chart
from services.ai_service import generate_questions, evaluate_answers
from database.db import (
    get_latest_resume, create_interview,
    update_interview_answers, save_scores, save_feedback,
    get_score_by_interview, get_feedback_by_interview,
)

JOB_ROLES = [
    "Software Engineer", "Data Analyst", "Data Scientist",
    "AI Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer",
]
DIFFICULTIES = ["Beginner", "Intermediate", "Advanced"]


def render():
    if not is_logged_in():
        st.warning("Please login first.")
        if st.button("Go to Login"):
            st.session_state["page"] = "login"
            st.rerun()
        return

    user = get_current_user()

    # State machine: setup → interview → results
    stage = st.session_state.get("mock_stage", "setup")

    if stage == "setup":
        _render_setup(user)
    elif stage == "interview":
        _render_interview(user)
    elif stage == "results":
        _render_results(user)


# ── Setup ─────────────────────────────────────────────────────────────────────

def _render_setup(user):
    page_header("Mock Interview", "Configure your interview session and let AI generate tailored questions.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Interview Configuration")
        job_role   = st.selectbox("Job Role", JOB_ROLES, key="mock_role")
        difficulty = st.selectbox("Difficulty Level", DIFFICULTIES, key="mock_diff")
        num_q      = st.slider("Number of Questions", 5, 15, 10, key="mock_numq")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📄 Resume Context")
        latest = get_latest_resume(user["id"])
        if latest:
            st.success(f"Using: **{latest['filename']}**")
            st.markdown(
                f'<div style="color:#8888aa;font-size:0.85rem;">Uploaded {latest["uploaded_at"][:10]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.warning("No resume found. Generic questions will be generated.")
            st.markdown(
                '_Tip: Upload a resume in the Resume Analyzer for personalized questions._'
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Generate Questions & Start Interview", use_container_width=True):
        resume_text = latest["extracted_text"] if latest else f"Candidate applying for {job_role}."

        with st.spinner(f"AI is crafting {num_q} {difficulty} questions for {job_role}…"):
            questions = generate_questions(resume_text, job_role, difficulty, num_q)

        resume_id = latest["id"] if latest else None
        interview_id = create_interview(
            user_id=user["id"],
            resume_id=resume_id,
            job_role=job_role,
            difficulty=difficulty,
            interview_type="text",
            questions=json.dumps(questions),
        )

        st.session_state.update({
            "mock_stage":       "interview",
            "mock_questions":   questions,
            "mock_answers":     [""] * len(questions),
            "mock_current_q":   0,
            "mock_interview_id": interview_id,
            "mock_job_role":    job_role,
            "mock_difficulty":  difficulty,
        })
        st.rerun()


# ── Interview ─────────────────────────────────────────────────────────────────

def _render_interview(user):
    questions = st.session_state["mock_questions"]
    answers   = st.session_state["mock_answers"]
    current   = st.session_state["mock_current_q"]
    total     = len(questions)

    page_header(
        f"Question {current + 1} of {total}",
        f"{st.session_state['mock_job_role']} · {st.session_state['mock_difficulty']}",
    )

    # Progress bar
    st.progress((current) / total)

    if current < total:
        q_data = questions[current]
        q_text = q_data["question"] if isinstance(q_data, dict) else q_data
        q_type = q_data.get("type", "general") if isinstance(q_data, dict) else "general"

        badge_color = {"technical": "#6c63ff", "hr": "#00d4ff", "behavioral": "#ff6584"}.get(q_type, "#888")
        st.markdown(
            f'<div class="glass-card">'
            f'<div style="margin-bottom:12px;">'
            f'<span style="padding:3px 12px;border-radius:999px;font-size:0.75rem;font-weight:600;'
            f'background:rgba(108,99,255,0.15);border:1px solid {badge_color}44;color:{badge_color};">'
            f'{q_type.upper()}</span></div>'
            f'<p style="font-family:Syne,sans-serif;font-size:1.15rem;font-weight:600;'
            f'color:#f0f0f8;line-height:1.6;margin:0;">{q_text}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

        answer = st.text_area(
            "Your Answer",
            value=answers[current],
            height=160,
            placeholder="Type your answer here… Be detailed and specific.",
            key=f"answer_{current}",
        )
        answers[current] = answer
        st.session_state["mock_answers"] = answers

        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if current > 0:
                if st.button("◀ Previous"):
                    st.session_state["mock_current_q"] -= 1
                    st.rerun()
        with col2:
            if current < total - 1:
                if st.button("Next ▶"):
                    st.session_state["mock_current_q"] += 1
                    st.rerun()
        with col3:
            if st.button("✅ Submit All Answers", use_container_width=True):
                _submit_interview(user)

        # Question navigator
        st.markdown("---")
        st.markdown(
            '<div style="color:#8888aa;font-size:0.8rem;margin-bottom:8px;">Question Navigator</div>',
            unsafe_allow_html=True,
        )
        nav_cols = st.columns(min(total, 10))
        for i, col in enumerate(nav_cols[:total]):
            with col:
                filled = bool(answers[i].strip())
                active = (i == current)
                bg = "#6c63ff" if active else ("#00e676" if filled else "rgba(255,255,255,0.08)")
                color = "white" if (active or filled) else "#8888aa"
                st.markdown(
                    f'<div style="text-align:center;padding:6px;border-radius:8px;'
                    f'background:{bg};color:{color};font-size:0.8rem;font-weight:600;'
                    f'cursor:pointer;">{i+1}</div>',
                    unsafe_allow_html=True,
                )


def _submit_interview(user):
    questions = st.session_state["mock_questions"]
    answers   = st.session_state["mock_answers"]
    interview_id = st.session_state["mock_interview_id"]

    with st.spinner("Saving answers…"):
        update_interview_answers(interview_id, json.dumps(answers))

    qa_pairs = []
    for i, q_data in enumerate(questions):
        q_text = q_data["question"] if isinstance(q_data, dict) else q_data
        q_type = q_data.get("type", "general") if isinstance(q_data, dict) else "general"
        qa_pairs.append({
            "question": q_text,
            "answer":   answers[i] if i < len(answers) else "",
            "type":     q_type,
        })

    with st.spinner("AI is evaluating your responses… this may take 20–30 seconds."):
        evaluation = evaluate_answers(
            qa_pairs,
            st.session_state["mock_job_role"],
            st.session_state["mock_difficulty"],
        )

    save_scores(
        interview_id=interview_id,
        user_id=user["id"],
        overall=evaluation.get("overall_score", 0),
        technical=evaluation.get("technical_score", 0),
        communication=evaluation.get("communication_score", 0),
        confidence=evaluation.get("confidence_score", 0),
    )

    save_feedback(
        interview_id=interview_id,
        user_id=user["id"],
        strengths=json.dumps(evaluation.get("strengths", [])),
        weaknesses=json.dumps(evaluation.get("weaknesses", [])),
        improvements=json.dumps(evaluation.get("improvements", [])),
        learning_path=json.dumps(evaluation.get("learning_path", [])),
        career_advice="",
    )

    st.session_state["mock_evaluation"] = evaluation
    st.session_state["mock_stage"] = "results"
    st.rerun()


# ── Results ───────────────────────────────────────────────────────────────────

def _render_results(user):
    evaluation = st.session_state.get("mock_evaluation", {})
    page_header("Interview Results", "Here's how you performed in your mock interview.")

    # Score cards
    overall = evaluation.get("overall_score", 0)
    scores  = {
        "Technical":     evaluation.get("technical_score", 0),
        "Communication": evaluation.get("communication_score", 0),
        "Confidence":    evaluation.get("confidence_score", 0),
        "Overall":       overall,
    }

    c1, c2, c3, c4 = st.columns(4)
    for col, (label, val) in zip([c1, c2, c3, c4], scores.items()):
        cls = "score-high" if val >= 70 else "score-mid" if val >= 50 else "score-low"
        with col:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="label">{label}</div>'
                f'<div class="value">{val}</div>'
                f'<div><span class="score-badge {cls}">/100</span></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts
    col_l, col_r = st.columns(2)
    with col_l:
        st.plotly_chart(radar_chart(scores), use_container_width=True)
    with col_r:
        st.plotly_chart(score_bar_chart(scores), use_container_width=True)

    st.markdown("---")

    # Per-question feedback
    per_q = evaluation.get("per_question", [])
    if per_q:
        st.markdown("### 📝 Question-by-Question Feedback")
        for i, item in enumerate(per_q, 1):
            q_score = item.get("score", 0)
            cls = "score-high" if q_score >= 7 else "score-mid" if q_score >= 5 else "score-low"
            with st.expander(f"Q{i}: {item.get('question','')[:80]}…  —  Score: {q_score}/10"):
                st.markdown(
                    f'<span class="score-badge {cls}">{q_score}/10</span>'
                    f'<p style="color:#f0f0f8;margin-top:10px;">{item.get("comment","")}</p>',
                    unsafe_allow_html=True,
                )

    st.markdown("---")

    # Strengths / Weaknesses / Improvements
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="glass-card"><h4 style="color:#00e676;">💪 Strengths</h4>', unsafe_allow_html=True)
        for s in evaluation.get("strengths", []):
            st.markdown(f"✅ {s}")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="glass-card"><h4 style="color:#ff5252;">🔻 Weaknesses</h4>', unsafe_allow_html=True)
        for s in evaluation.get("weaknesses", []):
            st.markdown(f"⚠️ {s}")
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="glass-card"><h4 style="color:#ffab40;">🎯 Areas to Improve</h4>', unsafe_allow_html=True)
        for s in evaluation.get("improvements", []):
            st.markdown(f"📌 {s}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Learning path
    lp = evaluation.get("learning_path", [])
    if lp:
        st.markdown("### 🗺️ Recommended Learning Path")
        for i, item in enumerate(lp, 1):
            st.markdown(
                f'<div class="glass-card" style="padding:12px 20px;">'
                f'<strong style="color:#6c63ff;">{i}. {item.get("topic","")}</strong>'
                f' &nbsp;—&nbsp; <span style="color:#8888aa;">{item.get("resource","")}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔄 New Interview", use_container_width=True):
            for k in ["mock_stage", "mock_questions", "mock_answers",
                      "mock_current_q", "mock_interview_id", "mock_evaluation"]:
                st.session_state.pop(k, None)
            st.rerun()
    with c2:
        if st.button("📊 View Dashboard", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()
    with c3:
        if st.button("🧭 Career Advisor", use_container_width=True):
            st.session_state["page"] = "career"
            st.rerun()
