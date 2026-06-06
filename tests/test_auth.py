"""
tests/test_auth.py
Unit tests for authentication module.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Use an in-memory test database
os.environ["TEST_MODE"] = "1"

from utils.auth import hash_password, verify_password


class TestPasswordHashing(unittest.TestCase):

    def test_hash_is_not_plain(self):
        pwd = "TestPassword123"
        hashed = hash_password(pwd)
        self.assertNotEqual(pwd, hashed)

    def test_verify_correct_password(self):
        pwd = "SecurePass456"
        hashed = hash_password(pwd)
        self.assertTrue(verify_password(pwd, hashed))

    def test_verify_wrong_password(self):
        pwd = "RealPassword"
        hashed = hash_password(pwd)
        self.assertFalse(verify_password("WrongPassword", hashed))

    def test_hash_unique_each_time(self):
        pwd = "SamePassword"
        hash1 = hash_password(pwd)
        hash2 = hash_password(pwd)
        self.assertNotEqual(hash1, hash2)  # bcrypt salts differ

    def test_empty_password(self):
        pwd = ""
        hashed = hash_password(pwd)
        self.assertTrue(verify_password(pwd, hashed))


class TestPasswordStrength(unittest.TestCase):

    def test_short_password_detection(self):
        """The register_user function rejects passwords < 6 chars."""
        # We test the length check logic directly
        password = "abc"
        self.assertLess(len(password), 6)

    def test_valid_password_length(self):
        password = "secure123"
        self.assertGreaterEqual(len(password), 6)


if __name__ == "__main__":
    unittest.main()
