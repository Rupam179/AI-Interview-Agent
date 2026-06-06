"""
pages/home.py
Landing / Home page.
"""

import streamlit as st


def render():
    # Hero section
    st.markdown(
        """
        <div style="text-align:center;padding:60px 20px 40px;">
            <div style="font-size:4rem;margin-bottom:12px;">🤖</div>
            <h1 style="font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;
                       background:linear-gradient(135deg,#6c63ff,#00d4ff,#ff6584);
                       -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                       margin-bottom:8px;">
                AI Interview Agent
            </h1>
            <p style="color:#8888aa;font-size:1.15rem;max-width:600px;margin:0 auto 32px;">
                Your intelligent interview preparation companion — powered by Google Gemini AI.
                Analyze your resume, practice interviews, and land your dream job.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # CTA buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🚀  Get Started — Register", use_container_width=True):
            st.session_state["page"] = "register"
            st.rerun()
    with col2:
        if st.button("🔑  Already have an account? Login", use_container_width=True):
            st.session_state["page"] = "login"
            st.rerun()
    with col3:
        if st.button("ℹ️  Learn More", use_container_width=True):
            st.session_state["page"] = "about"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature cards
    st.markdown(
        '<h2 style="font-family:Syne,sans-serif;text-align:center;margin-bottom:32px;color:#f0f0f8;">✨ Key Features</h2>',
        unsafe_allow_html=True,
    )

    features = [
        ("📄", "Resume Analyzer",
         "Upload PDF or DOCX. Get ATS score, skill gap analysis, and actionable improvements."),
        ("💬", "AI Mock Interview",
         "AI-generated questions tailored to your resume, job role, and experience level."),
        ("🎙️", "Voice Interview",
         "Speak your answers. AI converts speech-to-text and evaluates your responses."),
        ("📊", "Performance Analytics",
         "Scores for technical knowledge, communication, and confidence with trend charts."),
        ("💡", "Personalized Feedback",
         "Strengths, weaknesses, and a custom learning roadmap just for you."),
        ("🧭", "Career Advisor",
         "AI recommends career paths, certifications, and technologies to learn next."),
    ]

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="glass-card" style="height:170px;">
                    <div style="font-size:2rem;margin-bottom:10px;">{icon}</div>
                    <div style="font-family:'Syne',sans-serif;font-weight:700;
                                color:#f0f0f8;margin-bottom:8px;font-size:1rem;">{title}</div>
                    <div style="color:#8888aa;font-size:0.86rem;line-height:1.5;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # SDG Section
    st.markdown(
        """
        <div class="glass-card" style="text-align:center;">
            <h3 style="font-family:'Syne',sans-serif;color:#f0f0f8;margin-bottom:16px;">
                🌍 UN Sustainable Development Goals
            </h3>
            <div style="display:flex;justify-content:center;gap:32px;flex-wrap:wrap;">
                <div style="padding:16px 24px;border-radius:12px;
                            background:rgba(108,99,255,0.12);border:1px solid rgba(108,99,255,0.25);">
                    <div style="font-size:1.8rem;">💼</div>
                    <div style="font-weight:700;color:#6c63ff;font-size:1rem;margin:6px 0 4px;">SDG 8</div>
                    <div style="color:#8888aa;font-size:0.82rem;">Decent Work &<br>Economic Growth</div>
                </div>
                <div style="padding:16px 24px;border-radius:12px;
                            background:rgba(0,212,255,0.10);border:1px solid rgba(0,212,255,0.2);">
                    <div style="font-size:1.8rem;">📚</div>
                    <div style="font-weight:700;color:#00d4ff;font-size:1rem;margin:6px 0 4px;">SDG 4</div>
                    <div style="color:#8888aa;font-size:0.82rem;">Quality<br>Education</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Stats bar
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    stats = [("7+", "Job Roles"), ("3", "Difficulty Levels"), ("100%", "AI Powered"), ("Free", "To Use")]
    for col, (val, lbl) in zip([c1, c2, c3, c4], stats):
        with col:
            st.markdown(
                f"""<div class="metric-card">
                    <div class="label">{lbl}</div>
                    <div class="value">{val}</div>
                </div>""",
                unsafe_allow_html=True,
            )
