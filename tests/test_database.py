"""
tests/test_database.py
Integration tests for database operations using a temporary test DB.
"""

import sys
import os
import unittest
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Point DB to a temp file for tests
_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp.close()
import database.db as db_module
db_module.DB_PATH = _tmp.name

from database.db import (
    init_db, create_user, get_user_by_email, get_user_by_id,
    save_resume, get_resumes_by_user, get_latest_resume,
    create_interview, update_interview_answers, get_interviews_by_user,
    save_scores, get_scores_by_user, get_score_by_interview,
    save_feedback, get_feedback_by_interview,
)


class TestUserOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

    def test_create_and_retrieve_user(self):
        uid = create_user("Test User", "test@example.com", "hashed_pw_abc")
        self.assertIsNotNone(uid)
        user = get_user_by_email("test@example.com")
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], "Test User")

    def test_get_user_by_id(self):
        uid = create_user("ID User", "iduser@example.com", "hashed_pw_xyz")
        user = get_user_by_id(uid)
        self.assertIsNotNone(user)
        self.assertEqual(user["email"], "iduser@example.com")

    def test_duplicate_email_raises(self):
        create_user("Original", "dup@example.com", "pw1")
        with self.assertRaises(Exception):
            create_user("Duplicate", "dup@example.com", "pw2")

    def test_nonexistent_user_returns_none(self):
        user = get_user_by_email("nobody@nowhere.com")
        self.assertIsNone(user)


class TestResumeOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()
        cls.user_id = create_user("Resume User", "resume@test.com", "pw")

    def test_save_and_retrieve_resume(self):
        rid = save_resume(
            user_id=self.user_id,
            filename="cv.pdf",
            text="Python developer with 2 years experience.",
            skills='["Python", "SQL"]',
            missing_skills='["Docker"]',
            ats_score=72.5,
            suggestions='["Add more keywords"]',
        )
        self.assertIsNotNone(rid)
        resumes = get_resumes_by_user(self.user_id)
        self.assertGreater(len(resumes), 0)
        self.assertEqual(resumes[0]["filename"], "cv.pdf")

    def test_latest_resume(self):
        latest = get_latest_resume(self.user_id)
        self.assertIsNotNone(latest)
        self.assertIn("ats_score", latest.keys())


class TestInterviewOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()
        cls.user_id = create_user("Interview User", "iv@test.com", "pw")

    def test_create_and_retrieve_interview(self):
        iid = create_interview(
            user_id=self.user_id,
            resume_id=None,
            job_role="Software Engineer",
            difficulty="Intermediate",
            interview_type="text",
            questions='[{"question":"What is OOP?","type":"technical"}]',
        )
        self.assertIsNotNone(iid)
        interviews = get_interviews_by_user(self.user_id)
        self.assertGreater(len(interviews), 0)

    def test_update_answers(self):
        iid = create_interview(
            user_id=self.user_id,
            resume_id=None,
            job_role="Data Analyst",
            difficulty="Beginner",
            interview_type="text",
            questions='[]',
        )
        update_interview_answers(iid, '["Answer 1", "Answer 2"]')
        from database.db import get_interview_by_id
        iv = get_interview_by_id(iid)
        self.assertIsNotNone(iv["completed_at"])


class TestScoreOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()
        cls.user_id = create_user("Score User", "score@test.com", "pw")
        cls.interview_id = create_interview(
            user_id=cls.user_id,
            resume_id=None,
            job_role="AI Engineer",
            difficulty="Advanced",
            interview_type="text",
            questions="[]",
        )

    def test_save_and_retrieve_scores(self):
        sid = save_scores(
            interview_id=self.interview_id,
            user_id=self.user_id,
            overall=82.0,
            technical=78.0,
            communication=85.0,
            confidence=80.0,
        )
        self.assertIsNotNone(sid)
        score = get_score_by_interview(self.interview_id)
        self.assertEqual(score["overall_score"], 82.0)

    def test_scores_by_user(self):
        scores = get_scores_by_user(self.user_id)
        self.assertGreater(len(scores), 0)


class TestFeedbackOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()
        cls.user_id = create_user("Feedback User", "fb@test.com", "pw")
        cls.interview_id = create_interview(
            user_id=cls.user_id,
            resume_id=None,
            job_role="Backend Developer",
            difficulty="Intermediate",
            interview_type="voice",
            questions="[]",
        )

    def test_save_and_retrieve_feedback(self):
        fid = save_feedback(
            interview_id=self.interview_id,
            user_id=self.user_id,
            strengths='["Good communication"]',
            weaknesses='["Needs deeper technical knowledge"]',
            improvements='["Practice DSA problems"]',
            learning_path='[{"topic":"System Design","resource":"Grokking the System Design Interview"}]',
            career_advice="Focus on backend fundamentals.",
        )
        self.assertIsNotNone(fid)
        fb = get_feedback_by_interview(self.interview_id)
        self.assertIsNotNone(fb)
        self.assertIn("Good communication", fb["strengths"])


if __name__ == "__main__":
    unittest.main()
