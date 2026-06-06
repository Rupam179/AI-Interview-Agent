"""
database/db.py
Database initialization and connection management for AI Interview Agent.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "interview_agent.db")


def get_connection():
    """Return a new SQLite connection."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            email       TEXT    NOT NULL UNIQUE,
            password    TEXT    NOT NULL,
            created_at  TEXT    DEFAULT (datetime('now')),
            last_login  TEXT
        );

        -- Resumes table
        CREATE TABLE IF NOT EXISTS resumes (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            filename        TEXT    NOT NULL,
            extracted_text  TEXT,
            skills          TEXT,
            missing_skills  TEXT,
            ats_score       REAL,
            suggestions     TEXT,
            uploaded_at     TEXT DEFAULT (datetime('now'))
        );

        -- Interviews table
        CREATE TABLE IF NOT EXISTS interviews (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            resume_id       INTEGER REFERENCES resumes(id),
            job_role        TEXT    NOT NULL,
            difficulty      TEXT    NOT NULL,
            interview_type  TEXT    NOT NULL DEFAULT 'text',
            questions       TEXT,
            answers         TEXT,
            started_at      TEXT DEFAULT (datetime('now')),
            completed_at    TEXT
        );

        -- Scores table
        CREATE TABLE IF NOT EXISTS scores (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            interview_id        INTEGER NOT NULL REFERENCES interviews(id) ON DELETE CASCADE,
            user_id             INTEGER NOT NULL REFERENCES users(id),
            overall_score       REAL,
            technical_score     REAL,
            communication_score REAL,
            confidence_score    REAL,
            evaluated_at        TEXT DEFAULT (datetime('now'))
        );

        -- Feedback table
        CREATE TABLE IF NOT EXISTS feedback (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            interview_id    INTEGER NOT NULL REFERENCES interviews(id) ON DELETE CASCADE,
            user_id         INTEGER NOT NULL REFERENCES users(id),
            strengths       TEXT,
            weaknesses      TEXT,
            improvements    TEXT,
            learning_path   TEXT,
            career_advice   TEXT,
            created_at      TEXT DEFAULT (datetime('now'))
        );
    """)

    conn.commit()
    conn.close()


# ─── User Operations ─────────────────────────────────────────────────────────

def create_user(name: str, email: str, hashed_password: str) -> int:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed_password),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_user_by_email(email: str):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cursor.fetchone()
    finally:
        conn.close()


def get_user_by_id(user_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()
    finally:
        conn.close()


def update_last_login(user_id: int):
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE users SET last_login = datetime('now') WHERE id = ?", (user_id,)
        )
        conn.commit()
    finally:
        conn.close()


# ─── Resume Operations ────────────────────────────────────────────────────────

def save_resume(user_id, filename, text, skills, missing_skills, ats_score, suggestions) -> int:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO resumes
               (user_id, filename, extracted_text, skills, missing_skills, ats_score, suggestions)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_id, filename, text, skills, missing_skills, ats_score, suggestions),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_resumes_by_user(user_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM resumes WHERE user_id = ? ORDER BY uploaded_at DESC", (user_id,)
        )
        return cursor.fetchall()
    finally:
        conn.close()


def get_latest_resume(user_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM resumes WHERE user_id = ? ORDER BY uploaded_at DESC LIMIT 1",
            (user_id,),
        )
        return cursor.fetchone()
    finally:
        conn.close()


# ─── Interview Operations ─────────────────────────────────────────────────────

def create_interview(user_id, resume_id, job_role, difficulty, interview_type, questions) -> int:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO interviews
               (user_id, resume_id, job_role, difficulty, interview_type, questions)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, resume_id, job_role, difficulty, interview_type, questions),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def update_interview_answers(interview_id: int, answers: str):
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE interviews SET answers = ?, completed_at = datetime('now') WHERE id = ?",
            (answers, interview_id),
        )
        conn.commit()
    finally:
        conn.close()


def get_interviews_by_user(user_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM interviews WHERE user_id = ? ORDER BY started_at DESC", (user_id,)
        )
        return cursor.fetchall()
    finally:
        conn.close()


def get_interview_by_id(interview_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM interviews WHERE id = ?", (interview_id,))
        return cursor.fetchone()
    finally:
        conn.close()


# ─── Score Operations ─────────────────────────────────────────────────────────

def save_scores(interview_id, user_id, overall, technical, communication, confidence) -> int:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO scores
               (interview_id, user_id, overall_score, technical_score, communication_score, confidence_score)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (interview_id, user_id, overall, technical, communication, confidence),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_scores_by_user(user_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT s.*, i.job_role, i.difficulty, i.started_at
               FROM scores s JOIN interviews i ON s.interview_id = i.id
               WHERE s.user_id = ? ORDER BY s.evaluated_at DESC""",
            (user_id,),
        )
        return cursor.fetchall()
    finally:
        conn.close()


def get_score_by_interview(interview_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scores WHERE interview_id = ?", (interview_id,))
        return cursor.fetchone()
    finally:
        conn.close()


# ─── Feedback Operations ──────────────────────────────────────────────────────

def save_feedback(interview_id, user_id, strengths, weaknesses, improvements, learning_path, career_advice) -> int:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO feedback
               (interview_id, user_id, strengths, weaknesses, improvements, learning_path, career_advice)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (interview_id, user_id, strengths, weaknesses, improvements, learning_path, career_advice),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_feedback_by_interview(interview_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM feedback WHERE interview_id = ?", (interview_id,))
        return cursor.fetchone()
    finally:
        conn.close()


def get_latest_feedback(user_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM feedback WHERE user_id = ? ORDER BY created_at DESC LIMIT 1",
            (user_id,),
        )
        return cursor.fetchone()
    finally:
        conn.close()
