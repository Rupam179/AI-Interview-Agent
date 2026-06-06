"""
pages/register.py
Registration page.
"""

import streamlit as st
from utils.auth import register_user
from utils.styles import page_header


def render():
    page_header("Create Account", "Join thousands of candidates preparing smarter with AI.")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Register")

        name = st.text_input("Full Name", placeholder="Rupam Mukherjee", key="reg_name")
        email = st.text_input("Email Address", placeholder="you@example.com", key="reg_email")
        password = st.text_input("Password", type="password",
                                 placeholder="Min 6 characters", key="reg_pass")
        confirm = st.text_input("Confirm Password", type="password",
                                placeholder="Repeat password", key="reg_confirm")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Create Account →", use_container_width=True):
            if not name or not email or not password or not confirm:
                st.error("Please fill in all fields.")
            elif password != confirm:
                st.error("Passwords do not match.")
            else:
                ok, msg = register_user(name.strip(), email.strip().lower(), password)
                if ok:
                    st.success(msg + " Please login.")
                    st.session_state["page"] = "login"
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div style="text-align:center;color:#8888aa;font-size:0.85rem;">'
            "Already have an account?</div>",
            unsafe_allow_html=True,
        )
        if st.button("Login Instead", use_container_width=True, key="go_login"):
            st.session_state["page"] = "login"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
