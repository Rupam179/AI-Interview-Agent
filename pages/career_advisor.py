"""
pages/career_advisor.py
AI-powered career path suggestions, certifications, courses, and tech recommendations.
"""

import json
import streamlit as st
from utils.auth import is_logged_in, get_current_user
from utils.styles import page_header
from services.ai_service import get_career_advice
from database.db import get_latest_resume


def render():
    if not is_logged_in():
        st.warning("Please login first.")
        if st.button("Go to Login"):
            st.session_state["page"] = "login"
            st.rerun()
        return

    user = get_current_user()
    page_header("Career Advisor", "AI-powered career path guidance tailored to your skills and experience.")

    latest = get_latest_resume(user["id"])

    if not latest:
        st.markdown(
            """
            <div class="glass-card" style="text-align:center;padding:48px;">
                <div style="font-size:3rem;margin-bottom:16px;">📄</div>
                <h3 style="color:#f0f0f8;">No Resume Found</h3>
                <p style="color:#8888aa;">Upload your resume first to get personalized career advice.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Upload Resume →", use_container_width=False):
            st.session_state["page"] = "resume"
            st.rerun()
        return

    # Parse skills from resume
    skills = []
    if latest["skills"]:
        try:
            skills = json.loads(latest["skills"])
        except Exception:
            skills = []

    # Show resume context
    st.markdown(
        f'<div class="glass-card" style="padding:12px 20px;">'
        f'📄 Analyzing based on: <strong style="color:#f0f0f8;">{latest["filename"]}</strong>'
        f' &nbsp;·&nbsp; ATS Score: <span style="color:#6c63ff;font-weight:700;">'
        f'{latest["ats_score"]}/100</span></div>',
        unsafe_allow_html=True,
    )

    # Generate advice
    if "career_advice" not in st.session_state:
        if st.button("🧭 Generate Career Advice", use_container_width=True):
            with st.spinner("AI Career Advisor is analyzing your profile… (15–25 seconds)"):
                advice = get_career_advice(latest["extracted_text"] or "", skills)
            st.session_state["career_advice"] = advice
            st.rerun()
        return

    advice = st.session_state["career_advice"]

    # Refresh button
    col_ref, _ = st.columns([1, 4])
    with col_ref:
        if st.button("🔄 Refresh Advice"):
            del st.session_state["career_advice"]
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Roadmap ───────────────────────────────────────────────────────────────
    roadmap = advice.get("roadmap", "")
    if roadmap:
        st.markdown(
            f'<div class="glass-card">'
            f'<h3 style="font-family:Syne,sans-serif;color:#f0f0f8;margin-bottom:12px;">'
            f'🗺️ Your 6–12 Month Roadmap</h3>'
            f'<p style="color:#c0c0d8;line-height:1.8;font-size:1rem;">{roadmap}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Career Paths ──────────────────────────────────────────────────────────
    paths = advice.get("career_paths", [])
    if paths:
        st.markdown("### 🚀 Recommended Career Paths")
        cols = st.columns(min(len(paths), 3))
        for i, path in enumerate(paths[:3]):
            with cols[i]:
                st.markdown(
                    f'<div class="glass-card" style="height:200px;">'
                    f'<div style="font-family:Syne,sans-serif;font-weight:700;'
                    f'color:#f0f0f8;font-size:1rem;margin-bottom:8px;">'
                    f'💼 {path.get("title","")}</div>'
                    f'<div style="color:#8888aa;font-size:0.83rem;line-height:1.6;margin-bottom:10px;">'
                    f'{path.get("description","")}</div>'
                    f'<div style="display:flex;gap:8px;flex-wrap:wrap;">'
                    f'<span style="padding:2px 10px;border-radius:999px;font-size:0.75rem;'
                    f'background:rgba(0,230,118,0.12);border:1px solid rgba(0,230,118,0.25);'
                    f'color:#00e676;">{path.get("salary_range","")}</span>'
                    f'<span style="padding:2px 10px;border-radius:999px;font-size:0.75rem;'
                    f'background:rgba(108,99,255,0.12);border:1px solid rgba(108,99,255,0.25);'
                    f'color:#6c63ff;">{path.get("growth","")}</span>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["🏆 Certifications", "📚 Courses", "⚡ Technologies"])

    # ── Certifications ────────────────────────────────────────────────────────
    with tab1:
        certs = advice.get("certifications", [])
        if certs:
            for cert in certs:
                st.markdown(
                    f'<div class="glass-card" style="padding:16px 20px;">'
                    f'<div style="display:flex;align-items:center;gap:12px;">'
                    f'<span style="font-size:1.5rem;">🏆</span>'
                    f'<div>'
                    f'<div style="font-weight:700;color:#f0f0f8;font-size:0.95rem;">'
                    f'{cert.get("name","")}</div>'
                    f'<div style="color:#8888aa;font-size:0.82rem;margin-top:2px;">'
                    f'Provider: {cert.get("provider","")} &nbsp;·&nbsp; '
                    f'{cert.get("relevance","")}</div>'
                    f'</div></div></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No certifications data available.")

    # ── Courses ───────────────────────────────────────────────────────────────
    with tab2:
        courses = advice.get("courses", [])
        if courses:
            for course in courses:
                st.markdown(
                    f'<div class="glass-card" style="padding:16px 20px;">'
                    f'<div style="display:flex;align-items:center;gap:12px;">'
                    f'<span style="font-size:1.5rem;">📚</span>'
                    f'<div>'
                    f'<div style="font-weight:700;color:#f0f0f8;font-size:0.95rem;">'
                    f'{course.get("title","")}</div>'
                    f'<div style="color:#8888aa;font-size:0.82rem;margin-top:2px;">'
                    f'Platform: <span style="color:#00d4ff;">{course.get("platform","")}</span>'
                    f' &nbsp;·&nbsp; Duration: {course.get("duration","")}</div>'
                    f'</div></div></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No course data available.")

    # ── Technologies ──────────────────────────────────────────────────────────
    with tab3:
        techs = advice.get("technologies", [])
        if techs:
            cols = st.columns(2)
            for i, tech in enumerate(techs):
                with cols[i % 2]:
                    st.markdown(
                        f'<div class="glass-card" style="padding:14px 18px;">'
                        f'<span style="font-size:1.3rem;">⚡</span>'
                        f' <strong style="color:#f0f0f8;">{tech.get("name","")}</strong>'
                        f'<div style="color:#8888aa;font-size:0.82rem;margin-top:4px;">'
                        f'{tech.get("reason","")}</div></div>',
                        unsafe_allow_html=True,
                    )
        else:
            st.info("No technology data available.")

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💬 Start Mock Interview", use_container_width=True):
            st.session_state["page"] = "mock"
            st.rerun()
    with c2:
        if st.button("📊 View Dashboard", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()
