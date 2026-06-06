"""
pages/dashboard.py
User dashboard with interview history, score charts, and ATS overview.
"""

import streamlit as st
from utils.auth import is_logged_in, get_current_user
from utils.styles import page_header
from utils.charts import trend_line_chart, score_bar_chart, ats_gauge
from database.db import (
    get_scores_by_user, get_resumes_by_user,
    get_interviews_by_user, get_latest_resume,
)


def render():
    if not is_logged_in():
        st.warning("Please login to view your dashboard.")
        if st.button("Go to Login"):
            st.session_state["page"] = "login"
            st.rerun()
        return

    user = get_current_user()
    page_header(f"Hello, {user['name']} 👋", "Here's your interview preparation overview.")

    # ── Top KPI cards ─────────────────────────────────────────────────────────
    scores_data  = get_scores_by_user(user["id"])
    interviews   = get_interviews_by_user(user["id"])
    resumes      = get_resumes_by_user(user["id"])
    latest_resume = get_latest_resume(user["id"])

    total_interviews  = len(interviews)
    completed_interviews = sum(1 for i in interviews if i["completed_at"])
    avg_score = (
        round(sum(s["overall_score"] for s in scores_data) / len(scores_data), 1)
        if scores_data else 0
    )
    ats = latest_resume["ats_score"] if latest_resume and latest_resume["ats_score"] else 0

    c1, c2, c3, c4 = st.columns(4)
    kpis = [
        ("📝", "Total Interviews", total_interviews),
        ("✅", "Completed", completed_interviews),
        ("⭐", "Avg Score", f"{avg_score}/100"),
        ("📄", "ATS Score", f"{ats}/100"),
    ]
    for col, (icon, label, val) in zip([c1, c2, c3, c4], kpis):
        with col:
            st.markdown(
                f"""<div class="metric-card">
                    <div style="font-size:1.6rem;margin-bottom:6px;">{icon}</div>
                    <div class="label">{label}</div>
                    <div class="value" style="font-size:1.8rem;">{val}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row ────────────────────────────────────────────────────────────
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("#### 📈 Score Improvement Trend")
        history = [
            {
                "date": s["evaluated_at"][:10],
                "overall_score": s["overall_score"],
            }
            for s in reversed(list(scores_data))
        ]
        st.plotly_chart(trend_line_chart(history), use_container_width=True)

    with col_right:
        st.markdown("#### 🎯 ATS Score")
        if latest_resume:
            st.plotly_chart(ats_gauge(float(ats)), use_container_width=True)
        else:
            st.info("No resume uploaded yet. Go to Resume Analyzer to upload.")
            if st.button("Upload Resume"):
                st.session_state["page"] = "resume"
                st.rerun()

    st.markdown("---")

    # ── Score breakdown of latest interview ──────────────────────────────────
    if scores_data:
        latest = scores_data[0]
        st.markdown("#### 🏆 Latest Interview Score Breakdown")
        breakdown = {
            "Technical":      latest["technical_score"],
            "Communication":  latest["communication_score"],
            "Confidence":     latest["confidence_score"],
            "Overall":        latest["overall_score"],
        }
        st.plotly_chart(score_bar_chart(breakdown), use_container_width=True)

    # ── Interview history table ───────────────────────────────────────────────
    st.markdown("#### 📋 Interview History")
    if not interviews:
        st.info("No interviews yet. Start your first mock interview!")
        if st.button("Start Mock Interview"):
            st.session_state["page"] = "mock"
            st.rerun()
    else:
        import pandas as pd
        rows = []
        score_map = {s["interview_id"]: s for s in scores_data}
        for iv in interviews:
            sc = score_map.get(iv["id"])
            rows.append({
                "Date":       iv["started_at"][:10],
                "Role":       iv["job_role"],
                "Difficulty": iv["difficulty"],
                "Type":       iv["interview_type"],
                "Status":     "✅ Completed" if iv["completed_at"] else "🔄 In Progress",
                "Score":      f"{sc['overall_score']}/100" if sc else "—",
            })
        df = pd.DataFrame(rows)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

    # ── Quick actions ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### ⚡ Quick Actions")
    qa1, qa2, qa3, qa4 = st.columns(4)
    actions = [
        ("📄 Analyze Resume", "resume"),
        ("💬 Mock Interview", "mock"),
        ("🎙️ Voice Interview", "voice"),
        ("🧭 Career Advisor", "career"),
    ]
    for col, (label, page) in zip([qa1, qa2, qa3, qa4], actions):
        with col:
            if st.button(label, use_container_width=True):
                st.session_state["page"] = page
                st.rerun()
