"""
utils/auth.py
Authentication helpers: password hashing, session management.
"""

import bcrypt
import streamlit as st
from database.db import get_user_by_email, create_user, update_last_login, get_user_by_id


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def login_user(email: str, password: str) -> dict | None:
    user = get_user_by_email(email)
    if user and verify_password(password, user["password"]):
        update_last_login(user["id"])
        return dict(user)
    return None


def register_user(name: str, email: str, password: str) -> tuple[bool, str]:
    if get_user_by_email(email):
        return False, "Email already registered."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    hashed = hash_password(password)
    create_user(name, email, hashed)
    return True, "Registration successful!"


def is_logged_in() -> bool:
    return "user" in st.session_state and st.session_state["user"] is not None


def get_current_user() -> dict | None:
    return st.session_state.get("user")


def logout():
    for key in ["user", "interview_id", "questions", "answers", "current_q"]:
        st.session_state.pop(key, None)
    st.rerun()
