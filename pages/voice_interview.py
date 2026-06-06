"""
pages/voice_interview.py
Voice-based interview: AI asks questions, user answers by speech, converted to text and evaluated.
"""

import json
import streamlit as st
from utils.auth import is_logged_in, get_current_user
from utils.styles import page_header
from utils.charts import radar_chart, score_bar_chart
from services.ai_service import generate_questions, evaluate_answers
from services.voice_service import recognize_speech, list_microphones
from database.db import (
    get_latest_resume, create_interview,
    update_interview_answers, save_scores, save_feedback,
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
    stage = st.session_state.get("voice_stage", "setup")

    if stage == "setup":
        _render_setup(user)
    elif stage == "interview":
        _render_interview(user)
    elif stage == "results":
        _render_results(user)


# ── Setup ─────────────────────────────────────────────────────────────────────

def _render_setup(user):
    page_header("Voice Interview", "Speak your answers! AI listens, transcribes, and evaluates your responses.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Session Configuration")
        job_role   = st.selectbox("Job Role", JOB_ROLES, key="voice_role")
        difficulty = st.selectbox("Difficulty Level", DIFFICULTIES, key="voice_diff")
        num_q      = st.slider("Number of Questions", 3, 10, 5, key="voice_numq")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🎙️ Microphone Check")

        mics = list_microphones()
        if mics:
            st.success(f"✅ {len(mics)} microphone(s) detected")
            st.selectbox("Select Microphone", mics, key="voice_mic")
        else:
            st.error("❌ No microphone detected. Please connect a microphone.")

        st.markdown(
            """
            <div style="margin-top:12px;padding:12px;background:rgba(108,99,255,0.08);
                        border-radius:10px;border:1px solid rgba(108,99,255,0.2);">
                <div style="color:#8888aa;font-size:0.82rem;line-height:1.6;">
                    💡 <strong style="color:#f0f0f8;">Tips for best results:</strong><br>
                    • Speak clearly at a normal pace<br>
                    • Minimize background noise<br>
                    • Wait for the recording prompt<br>
                    • You have 30 seconds per answer
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🎙️ Start Voice Interview", use_container_width=True):
        latest = get_latest_resume(user["id"])
        resume_text = latest["extracted_text"] if latest else f"Candidate applying for {job_role}."

        with st.spinner(f"Generating {num_q} questions…"):
            questions = generate_questions(resume_text, job_role, difficulty, num_q)

        resume_id = latest["id"] if latest else None
        interview_id = create_interview(
            user_id=user["id"],
            resume_id=resume_id,
            job_role=job_role,
            difficulty=difficulty,
            interview_type="voice",
            questions=json.dumps(questions),
        )

        st.session_state.update({
            "voice_stage":       "interview",
            "voice_questions":   questions,
            "voice_answers":     [""] * len(questions),
            "voice_current_q":   0,
            "voice_interview_id": interview_id,
            "voice_job_role":    job_role,
            "voice_difficulty":  difficulty,
        })
        st.rerun()


# ── Interview ─────────────────────────────────────────────────────────────────

def _render_interview(user):
    questions = st.session_state["voice_questions"]
    answers   = st.session_state["voice_answers"]
    current   = st.session_state["voice_current_q"]
    total     = len(questions)

    page_header(
        f"Voice Interview — Q{current + 1}/{total}",
        f"{st.session_state['voice_job_role']} · {st.session_state['voice_difficulty']}",
    )

    st.progress(current / total)

    if current < total:
        q_data = questions[current]
        q_text = q_data["question"] if isinstance(q_data, dict) else q_data
        q_type = q_data.get("type", "general") if isinstance(q_data, dict) else "general"

        badge_color = {"technical": "#6c63ff", "hr": "#00d4ff", "behavioral": "#ff6584"}.get(q_type, "#888")

        # Question display
        st.markdown(
            f'<div class="glass-card" style="text-align:center;padding:32px;">'
            f'<div style="margin-bottom:16px;">'
            f'<span style="padding:4px 14px;border-radius:999px;font-size:0.75rem;font-weight:600;'
            f'background:rgba(108,99,255,0.15);border:1px solid {badge_color}55;color:{badge_color};">'
            f'{q_type.upper()}</span></div>'
            f'<div style="font-size:3rem;margin-bottom:16px;">🎙️</div>'
            f'<p style="font-family:Syne,sans-serif;font-size:1.2rem;font-weight:600;'
            f'color:#f0f0f8;line-height:1.6;max-width:700px;margin:0 auto;">{q_text}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Already has a transcription?
        if answers[current]:
            st.markdown(
                f'<div class="glass-card" style="border:1px solid rgba(0,230,118,0.3);">'
                f'<div style="color:#00e676;font-size:0.78rem;font-weight:600;'
                f'text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">📝 Transcribed Answer</div>'
                f'<p style="color:#f0f0f8;line-height:1.7;">{answers[current]}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

        # Controls
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🎤 Record Answer", use_container_width=True):
                with st.spinner("🔴 Recording… Speak now! (up to 30 seconds)"):
                    success, result = recognize_speech(timeout=10, phrase_time_limit=30)

                if success:
                    answers[current] = result
                    st.session_state["voice_answers"] = answers
                    st.success(f"✅ Transcribed: *{result[:100]}{'…' if len(result) > 100 else ''}*")
                    st.rerun()
                else:
                    st.error(f"❌ {result}")

        with col2:
            # Allow manual text fallback
            manual = st.text_area(
                "Or type your answer (fallback)",
                value=answers[current],
                height=100,
                key=f"voice_manual_{current}",
                placeholder="Type if microphone isn't working…",
            )
            if manual != answers[current]:
                answers[current] = manual
                st.session_state["voice_answers"] = answers

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if current > 0:
                if st.button("◀ Previous", use_container_width=True):
                    st.session_state["voice_current_q"] -= 1
                    st.rerun()

            if current < total - 1:
                if st.button("Next ▶", use_container_width=True):
                    st.session_state["voice_current_q"] += 1
                    st.rerun()

            if st.button("✅ Submit All", use_container_width=True):
                _submit_voice_interview(user)

        # Mini navigator
        st.markdown("---")
        nav_cols = st.columns(min(total, 10))
        for i, col in enumerate(nav_cols[:total]):
            with col:
                filled = bool(answers[i].strip())
                active = (i == current)
                bg = "#6c63ff" if active else ("#00e676" if filled else "rgba(255,255,255,0.08)")
                color = "white" if (active or filled) else "#8888aa"
                st.markdown(
                    f'<div style="text-align:center;padding:6px;border-radius:8px;'
                    f'background:{bg};color:{color};font-size:0.8rem;font-weight:600;">'
                    f'{i+1}</div>',
                    unsafe_allow_html=True,
                )


def _submit_voice_interview(user):
    questions    = st.session_state["voice_questions"]
    answers      = st.session_state["voice_answers"]
    interview_id = st.session_state["voice_interview_id"]

    with st.spinner("Saving transcripts…"):
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

    with st.spinner("AI evaluating your voice responses…"):
        evaluation = evaluate_answers(
            qa_pairs,
            st.session_state["voice_job_role"],
            st.session_state["voice_difficulty"],
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

    st.session_state["voice_evaluation"] = evaluation
    st.session_state["voice_stage"] = "results"
    st.rerun()


# ── Results ───────────────────────────────────────────────────────────────────

def _render_results(user):
    evaluation = st.session_state.get("voice_evaluation", {})
    page_header("Voice Interview Results", "Your speech was analyzed for content, communication, and confidence.")

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
                f'<span class="score-badge {cls}">/100</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)
    with col_l:
        st.plotly_chart(radar_chart(scores), use_container_width=True)
    with col_r:
        st.plotly_chart(score_bar_chart(scores), use_container_width=True)

    st.markdown("---")

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
        st.markdown('<div class="glass-card"><h4 style="color:#ffab40;">🎯 Improvements</h4>', unsafe_allow_html=True)
        for s in evaluation.get("improvements", []):
            st.markdown(f"📌 {s}")
        st.markdown("</div>", unsafe_allow_html=True)

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
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 New Voice Interview", use_container_width=True):
            for k in ["voice_stage", "voice_questions", "voice_answers",
                      "voice_current_q", "voice_interview_id", "voice_evaluation"]:
                st.session_state.pop(k, None)
            st.rerun()
    with c2:
        if st.button("📊 View Dashboard", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()
