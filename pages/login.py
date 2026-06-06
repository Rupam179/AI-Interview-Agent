"""
pages/login.py
Login page.
"""

import streamlit as st
from utils.auth import login_user
from utils.styles import page_header


def render():
    page_header("Welcome Back", "Sign in to continue your interview preparation journey.")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        st.markdown("### 🔑 Login")

        email = st.text_input("Email Address", placeholder="you@example.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Login →", use_container_width=True):
            if not email or not password:
                st.error("Please fill in all fields.")
            else:
                user = login_user(email.strip().lower(), password)
                if user:
                    st.session_state["user"] = user
                    st.session_state["page"] = "dashboard"
                    st.success(f"Welcome back, {user['name']}! 🎉")
                    st.rerun()
                else:
                    st.error("Invalid email or password. Please try again.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div style="text-align:center;color:#8888aa;font-size:0.85rem;">'
            "Don't have an account?</div>",
            unsafe_allow_html=True,
        )
        if st.button("Create Account", use_container_width=True, key="go_register"):
            st.session_state["page"] = "register"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
