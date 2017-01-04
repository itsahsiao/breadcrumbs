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


class FlaskTestsBasic(TestCase):
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


class FlaskTestsDatabase(TestCase):
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
                                 data={"login_email": "ashley@test.com",
                                       "login_password": "ashley"},
                                 follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("You have successfully logged in.", result.data)
        self.assertIn("<h3>Recent Trail</h3>", result.data)

    def test_signup_existing_user(self):

        result = self.client.post("/signup",
                                  data={"signup_email": "ashley@test.com",
                                        "signup_password": "ashley",
                                        "first_name": "Ashley",
                                        "last_name": "Test",
                                        "city": "Vancouver"},
                                 follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertNotIn("You have succesfully signed up for an account, and you are now logged in.", result.data)
        self.assertIn("An account already exists with this email address. Please login.", result.data)

    def test_signup_new_user(self):

        result = self.client.post("/signup",
                                  data={"signup_email": "doug@test.com",
                                        "signup_password": "doug",
                                        "first_name": "Doug",
                                        "last_name": "Test",
                                        "city": "Vancouver"},
                                 follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("You have succesfully signed up for an account, and you are now logged in.", result.data)
        self.assertIn("<h3>Recent Trail</h3>", result.data)
        self.assertNotIn("An account already exists with this email address. Please login.", result.data)

    def test_restaurants_list(self):

        result = self.client.get("/restaurants")
        self.assertIn("Chambar", result.data)

    def test_restaurants_search(self):

        result = self.client.get("/restaurants/search",
                                 data={"user_input": "cham"},
                                 follow_redirects=True)
        self.assertIn("Chambar", result.data)


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged into session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["current_user"] = {
                    "first_name": "Ashley",
                    "user_id": 1,
                    "num_received_requests": 2,
                    "num_sent_requests": 1,
                    "num_total_requests": 3
                }

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


    #
    # def test_important_page(self):
    #     """Test important page."""
    #
    #     result = self.client.get("/important")
    #     self.assertIn("You are a valued user", result.data)


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
