"""Integration Testing Flask app"""

# To run tests.py from anywhere, if in parent directory and want to run python tests/tests.py
# and import modules from parent directory, i.e. server
import os
import sys

current_file_path = os.path.realpath(__file__)
current_dir = os.path.dirname(current_file_path)
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from unittest import TestCase
from server import app
from model import *

# To test:
# python tests/tests.py

# Coverage:
# coverage run --omit=env/* tests/tests.py
# coverage run --source=. tests/tests.py

# For coverage report:
# coverage report -m


class FlaskIntegrationTests(TestCase):
    """Flask integration tests, ensuring that components work together."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn("The ultimate social media network for foodies", result.data)

    def test_login(self):
        """Test login page."""

        result = self.client.get("/login")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Login", result.data)
        self.assertIn("Don't have an account?", result.data)

    def test_signup(self):
        """Test signup page."""

        result = self.client.get("/signup")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Sign up", result.data)
        self.assertIn("First Name", result.data)
        self.assertNotIn("Don't have an account?", result.data)


class FlaskDatabaseTests(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                 data={"login_email": "ashley@test.com", "login_password": "ashley"},
                                 follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("You have successfully logged in.", result.data)
        self.assertIn("<h3>Recent Trail</h3>", result.data)


#     def test_departments_list(self):
#         """Test departments page."""

#         result = self.client.get("/departments")
#         self.assertIn("Legal", result.data)


#     def test_departments_details(self):
#         """Test departments page."""

#         result = self.client.get("/department/fin")
#         self.assertIn("Phone: 555-1000", result.data)


#     def test_login(self):
#         """Test login page."""

#         result = self.client.post("/login",
#                                   data={"user_id": "rachel", "password": "123"},
#                                   follow_redirects=True)
#         self.assertIn("You are a valued user", result.data)


# class FlaskTestsLoggedIn(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = 'key'
#         self.client = app.test_client()

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['user_id'] = 1

#     def test_important_page(self):
#         """Test important page."""

#         result = self.client.get("/important")
#         self.assertIn("You are a valued user", result.data)


# class FlaskTestsLoggedOut(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         self.client = app.test_client()

#     def test_important_page(self):
#         """Test that user can't see important page when logged out."""

#         result = self.client.get("/important", follow_redirects=True)
#         self.assertNotIn("You are a valued user", result.data)
#         self.assertIn("You must be logged in", result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
