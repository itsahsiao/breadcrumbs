"""Selenium Testing"""

import os
import sys

current_file_path = os.path.realpath(__file__)
current_dir = os.path.dirname(current_file_path)
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumTests(TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        """Test title of homepage."""

        self.browser.get('http://localhost:5000/')
        self.assertEqual(self.browser.title, "Breadcrumbs || Homepage")

    def test_signup_link(self):
        """Test signup links on homepage."""

        self.browser.get('http://localhost:5000/')
        link = self.browser.find_element_by_link_text("Sign up")

        link.click()
        wait = WebDriverWait(self.browser, 10)
        signup_page = wait.until(EC.title_contains("Sign Up"))

    def test_login_link(self):

        self.browser.get('http://localhost:5000/')
        link = self.browser.find_element_by_link_text("Login")

        link.click()
        wait = WebDriverWait(self.browser, 10)
        login_page = wait.until(EC.title_contains("Login"))




if __name__ == "__main__":
    import unittest

    unittest.main()
