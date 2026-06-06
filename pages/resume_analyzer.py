"""
pages/resume_analyzer.py
Resume upload, ATS scoring, skill extraction, and AI suggestions.
"""

import json
import streamlit as st
from utils.auth import is_logged_in, get_current_user
from utils.styles import page_header
from utils.resume_parser import extract_text
from utils.charts import ats_gauge
from services.ai_service import analyze_resume
from database.db import save_resume, get_resumes_by_user

JOB_ROLES = [
    "Software Engineer", "Data Analyst", "Data Scientist",
    "AI Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer",
]


def render():
    if not is_logged_in():
        st.warning("Please login first.")
        if st.button("Go to Login"):
            st.session_state["page"] = "login"
            st.rerun()
        return

    user = get_current_user()
    page_header("Resume Analyzer", "Upload your resume for AI-powered ATS analysis and skill gap detection.")

    tab1, tab2 = st.tabs(["📤 Upload & Analyze", "📋 Previous Resumes"])

    with tab1:
        col1, col2 = st.columns([2, 1])
        with col1:
            uploaded = st.file_uploader(
                "Upload Resume (PDF or DOCX)",
                type=["pdf", "docx"],
                help="Your resume will be analyzed by AI. Max 10 MB.",
            )
        with col2:
            job_role = st.selectbox("Target Job Role", JOB_ROLES)

        if uploaded:
            st.markdown(
                f'<div class="glass-card" style="padding:12px 20px;">'
                f'📎 <strong style="color:#f0f0f8;">{uploaded.name}</strong>'
                f' &nbsp;·&nbsp; <span style="color:#8888aa;">'
                f'{round(uploaded.size/1024,1)} KB</span></div>',
                unsafe_allow_html=True,
            )

            if st.button("🔍 Analyze Resume", use_container_width=False):
                with st.spinner("Extracting text from your resume…"):
                    file_bytes = uploaded.read()
                    resume_text = extract_text(file_bytes, uploaded.name)

                if resume_text.startswith("[Error"):
                    st.error(resume_text)
                    return

                with st.spinner("AI is analyzing your resume… this may take 10–20 seconds."):
                    analysis = analyze_resume(resume_text, job_role)

                # Save to DB
                save_resume(
                    user_id=user["id"],
                    filename=uploaded.name,
                    text=resume_text,
                    skills=json.dumps(analysis.get("skills", [])),
                    missing_skills=json.dumps(analysis.get("missing_skills", [])),
                    ats_score=analysis.get("ats_score", 0),
                    suggestions=json.dumps(analysis.get("suggestions", [])),
                )

                st.session_state["last_analysis"] = analysis
                st.session_state["last_resume_text"] = resume_text
                st.success("✅ Analysis complete!")
                st.rerun()

        # Show last analysis result
        if "last_analysis" in st.session_state:
            analysis = st.session_state["last_analysis"]
            _render_analysis(analysis)

    with tab2:
        resumes = get_resumes_by_user(user["id"])
        if not resumes:
            st.info("No resumes uploaded yet.")
        else:
            for r in resumes:
                with st.expander(f"📄 {r['filename']}  —  {r['uploaded_at'][:10]}  |  ATS: {r['ats_score']}/100"):
                    skills = json.loads(r["skills"]) if r["skills"] else []
                    missing = json.loads(r["missing_skills"]) if r["missing_skills"] else []
                    suggestions = json.loads(r["suggestions"]) if r["suggestions"] else []

                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("**✅ Identified Skills**")
                        for s in skills:
                            st.markdown(f"- {s}")
                    with c2:
                        st.markdown("**⚠️ Missing Skills**")
                        for s in missing:
                            st.markdown(f"- {s}")
                    if suggestions:
                        st.markdown("**💡 Suggestions**")
                        for s in suggestions:
                            st.markdown(f"- {s}")


def _render_analysis(analysis: dict):
    st.markdown("---")
    st.markdown("### 📊 Analysis Results")

    # ATS gauge + summary
    col1, col2 = st.columns([1, 2])
    with col1:
        st.plotly_chart(
            ats_gauge(float(analysis.get("ats_score", 0))),
            use_container_width=True,
        )
    with col2:
        st.markdown(
            f'<div class="glass-card">'
            f'<div style="font-size:0.78rem;color:#8888aa;text-transform:uppercase;'
            f'letter-spacing:1px;margin-bottom:8px;">AI Summary</div>'
            f'<p style="color:#f0f0f8;line-height:1.7;">'
            f'{analysis.get("summary","")}</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Skills columns
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            '<div class="glass-card"><h4 style="color:#00e676;margin-bottom:12px;">✅ Identified Skills</h4>',
            unsafe_allow_html=True,
        )
        skills = analysis.get("skills", [])
        if skills:
            chips = " ".join(
                f'<span style="display:inline-block;padding:4px 12px;margin:4px 2px;'
                f'border-radius:999px;background:rgba(0,230,118,0.12);'
                f'border:1px solid rgba(0,230,118,0.25);color:#00e676;'
                f'font-size:0.82rem;">{s}</span>'
                for s in skills
            )
            st.markdown(chips + "</div>", unsafe_allow_html=True)
        else:
            st.markdown("No skills detected.</div>", unsafe_allow_html=True)

    with c2:
        st.markdown(
            '<div class="glass-card"><h4 style="color:#ff5252;margin-bottom:12px;">⚠️ Missing Skills</h4>',
            unsafe_allow_html=True,
        )
        missing = analysis.get("missing_skills", [])
        if missing:
            chips = " ".join(
                f'<span style="display:inline-block;padding:4px 12px;margin:4px 2px;'
                f'border-radius:999px;background:rgba(255,82,82,0.12);'
                f'border:1px solid rgba(255,82,82,0.25);color:#ff5252;'
                f'font-size:0.82rem;">{s}</span>'
                for s in missing
            )
            st.markdown(chips + "</div>", unsafe_allow_html=True)
        else:
            st.markdown("No major gaps found!</div>", unsafe_allow_html=True)

    # Suggestions
    suggestions = analysis.get("suggestions", [])
    if suggestions:
        st.markdown("### 💡 AI Improvement Suggestions")
        for i, s in enumerate(suggestions, 1):
            st.markdown(
                f'<div class="glass-card" style="padding:12px 20px;">'
                f'<span style="color:#6c63ff;font-weight:700;">{i}.</span> '
                f'<span style="color:#f0f0f8;">{s}</span></div>',
                unsafe_allow_html=True,
            )

    # CTA
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💬 Start Mock Interview", use_container_width=True):
            st.session_state["page"] = "mock"
            st.rerun()
    with c2:
        if st.button("🧭 Get Career Advice", use_container_width=True):
            st.session_state["page"] = "career"
            st.rerun()
