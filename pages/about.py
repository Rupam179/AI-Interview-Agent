"""
pages/about.py
About page: project info, SDG mapping, tech stack, author.
"""

import streamlit as st
from utils.styles import page_header


def render():
    page_header("About This Project", "AI Interview Agent — Final Year Project by Rupam Mukherjee")

    # Project description
    st.markdown(
        """
        <div class="glass-card">
            <h3 style="font-family:Syne,sans-serif;color:#f0f0f8;">🤖 Project Overview</h3>
            <p style="color:#c0c0d8;line-height:1.8;">
                <strong style="color:#f0f0f8;">AI Interview Agent</strong> is a fully functional, 
                AI-powered Interview Preparation Platform built as a Final Year Project for 
                B.Tech CSE (AI & ML) at Techno India University. The platform leverages 
                <strong style="color:#6c63ff;">Google Gemini AI</strong> to help students and job 
                seekers prepare for technical and HR interviews through intelligent question 
                generation, resume analysis, voice interviews, and personalized feedback.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # SDG section
    st.markdown("### 🌍 UN Sustainable Development Goals Alignment")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            <div class="glass-card" style="border:1px solid rgba(108,99,255,0.3);">
                <div style="font-size:2rem;margin-bottom:10px;">💼</div>
                <div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;
                            color:#6c63ff;margin-bottom:8px;">SDG 8 — Decent Work & Economic Growth</div>
                <ul style="color:#c0c0d8;line-height:2;font-size:0.88rem;padding-left:20px;">
                    <li>Bridges the skills gap between education and employment</li>
                    <li>Increases interview success rates for job seekers</li>
                    <li>Provides free AI-powered career coaching to all</li>
                    <li>Supports youth employment and entrepreneurship</li>
                    <li>Promotes equal access to high-quality interview prep</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="glass-card" style="border:1px solid rgba(0,212,255,0.3);">
                <div style="font-size:2rem;margin-bottom:10px;">📚</div>
                <div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;
                            color:#00d4ff;margin-bottom:8px;">SDG 4 — Quality Education</div>
                <ul style="color:#c0c0d8;line-height:2;font-size:0.88rem;padding-left:20px;">
                    <li>Delivers personalized, AI-driven learning experiences</li>
                    <li>Generates adaptive questions based on skill level</li>
                    <li>Provides structured feedback and learning paths</li>
                    <li>Democratizes access to interview preparation resources</li>
                    <li>Recommends curated courses and certifications</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Tech stack
    st.markdown("### ⚙️ Technology Stack")
    tech_items = [
        ("🎨", "Frontend",    "Streamlit 1.35 — Python web UI framework"),
        ("🧠", "AI Engine",   "Google Gemini 1.5 Flash — LLM for Q&A, evaluation, advice"),
        ("🗄️", "Database",    "SQLite 3 — Lightweight relational database"),
        ("📄", "PDF Parsing", "pdfplumber + PyPDF2 — Resume text extraction"),
        ("📝", "DOCX Parsing","python-docx — Word document processing"),
        ("🎙️", "Voice",       "SpeechRecognition + Google Speech API"),
        ("📊", "Charts",      "Plotly — Interactive visualizations"),
        ("🔐", "Auth",        "bcrypt — Password hashing & session management"),
    ]
    cols = st.columns(2)
    for i, (icon, label, desc) in enumerate(tech_items):
        with cols[i % 2]:
            st.markdown(
                f'<div class="glass-card" style="padding:14px 18px;margin-bottom:10px;">'
                f'<span style="font-size:1.3rem;">{icon}</span>'
                f' <strong style="color:#f0f0f8;">{label}</strong>'
                f'<div style="color:#8888aa;font-size:0.82rem;margin-top:4px;">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # Features summary
    st.markdown("### ✨ Feature Summary")
    features = [
        "✅ User Registration, Login, Logout with bcrypt password encryption",
        "✅ Resume Upload (PDF/DOCX) with AI-powered ATS scoring",
        "✅ Skill extraction, gap analysis, and improvement suggestions",
        "✅ AI Mock Interview with 7 job roles and 3 difficulty levels",
        "✅ Voice Interview with real-time speech recognition",
        "✅ AI Evaluation: Technical, Communication, Confidence scores",
        "✅ Personalized feedback with strengths, weaknesses, learning path",
        "✅ Career Advisor: paths, certifications, courses, technologies",
        "✅ Dashboard with charts: trend, radar, ATS gauge, bar charts",
        "✅ Glassmorphism dark-mode UI with corporate design",
    ]
    for f in features:
        st.markdown(f'<div style="color:#c0c0d8;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.04);">{f}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Author card
    st.markdown(
        """
        <div class="glass-card" style="text-align:center;padding:32px;
             border:1px solid rgba(108,99,255,0.25);">
            <div style="font-size:3rem;margin-bottom:12px;">👨‍💻</div>
            <div style="font-family:Syne,sans-serif;font-size:1.3rem;font-weight:700;
                        color:#f0f0f8;margin-bottom:4px;">Rupam Mukherjee</div>
            <div style="color:#6c63ff;font-size:0.9rem;margin-bottom:4px;">
                B.Tech CSE (AI & ML) · Techno India University
            </div>
            <div style="color:#8888aa;font-size:0.82rem;margin-bottom:16px;">
                Semester 6 — Entrepreneurship & Skill Development (ESD) Project
            </div>
            <div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap;">
                <span style="padding:6px 16px;border-radius:999px;font-size:0.8rem;
                             background:rgba(108,99,255,0.15);border:1px solid rgba(108,99,255,0.3);
                             color:#6c63ff;">GitHub Portfolio</span>
                <span style="padding:6px 16px;border-radius:999px;font-size:0.8rem;
                             background:rgba(0,212,255,0.10);border:1px solid rgba(0,212,255,0.25);
                             color:#00d4ff;">LinkedIn</span>
                <span style="padding:6px 16px;border-radius:999px;font-size:0.8rem;
                             background:rgba(0,230,118,0.10);border:1px solid rgba(0,230,118,0.25);
                             color:#00e676;">Resume</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="text-align:center;color:#444466;font-size:0.75rem;margin-top:24px;">'
        'AI Interview Agent v1.0 · Built with ❤️ using Python, Streamlit & Google Gemini'
        '</div>',
        unsafe_allow_html=True,
    )
