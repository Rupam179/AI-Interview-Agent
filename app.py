"""
app.py
Main entry point for AI Interview Preparation Agent.
Run with: streamlit run app.py
"""

import streamlit as st
from database.db import init_db
from utils.styles import inject_css
from utils.auth import is_logged_in, get_current_user, logout

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="AI Interview Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Initialize DB ─────────────────────────────────────────────────────────────
init_db()

# ── Inject global CSS ─────────────────────────────────────────────────────────
inject_css()

# ── Lazy-import pages ─────────────────────────────────────────────────────────
def load_page(name: str):
    if name == "home":
        from pages.home import render; render()
    elif name == "login":
        from pages.login import render; render()
    elif name == "register":
        from pages.register import render; render()
    elif name == "dashboard":
        from pages.dashboard import render; render()
    elif name == "resume":
        from pages.resume_analyzer import render; render()
    elif name == "mock":
        from pages.mock_interview import render; render()
    elif name == "voice":
        from pages.voice_interview import render; render()
    elif name == "career":
        from pages.career_advisor import render; render()
    elif name == "about":
        from pages.about import render; render()

# ── Session defaults ──────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state["page"] = "home"
if "user" not in st.session_state:
    st.session_state["user"] = None

# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="padding:16px 8px 24px; text-align:center;">
            <div style="font-size:2rem;">🤖</div>
            <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;
                        background:linear-gradient(135deg,#6c63ff,#00d4ff);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                AI Interview Agent
            </div>
            <div style="font-size:0.72rem;color:#8888aa;margin-top:2px;">
                Powered by Gemini
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    nav_items = [("🏠", "Home", "home"), ("ℹ️", "About", "about")]

    if is_logged_in():
        user = get_current_user()
        st.markdown(
            f'<div style="padding:8px 14px;margin-bottom:12px;border-radius:10px;'
            f'background:rgba(108,99,255,0.1);border:1px solid rgba(108,99,255,0.2);">'
            f'<div style="font-size:0.72rem;color:#8888aa;">Logged in as</div>'
            f'<div style="font-weight:600;color:#f0f0f8;font-size:0.9rem;">{user["name"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        nav_items += [
            ("📊", "Dashboard", "dashboard"),
            ("📄", "Resume Analyzer", "resume"),
            ("💬", "Mock Interview", "mock"),
            ("🎙️", "Voice Interview", "voice"),
            ("🧭", "Career Advisor", "career"),
        ]
    else:
        nav_items += [("🔑", "Login", "login"), ("📝", "Register", "register")]

    for icon, label, key in nav_items:
        active = st.session_state["page"] == key
        btn_label = f"{icon} {label}" + (" ←" if active else "")
        if st.button(btn_label, key=f"nav_{key}"):
            st.session_state["page"] = key
            st.rerun()

    if is_logged_in():
        st.markdown("---")
        if st.button("🚪 Logout"):
            logout()

    st.markdown(
        '<div style="position:fixed;bottom:16px;left:16px;font-size:0.68rem;color:#444466;">'
        'v1.0 · Rupam Mukherjee<br>Techno India University</div>',
        unsafe_allow_html=True,
    )

# ── Route to active page ──────────────────────────────────────────────────────
load_page(st.session_state["page"])
