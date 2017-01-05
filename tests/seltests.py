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
from selenium.webdriver.support.ui import WebDriverWait, Select
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

    def test_signup_form(self):

        self.browser.get('http://localhost:5000/signup')

        email = self.browser.find_element_by_id("email")
        email.send_keys("selenium@test.com")
        password = self.browser.find_element_by_id("password")
        password.send_keys("testing123")
        fname = self.browser.find_element_by_id("firstname")
        fname.send_keys("Selenium")
        lname = self.browser.find_element_by_id("lastname")
        lname.send_keys("Test")
        city = Select(self.browser.find_element_by_id("city"))
        city.select_by_visible_text("Sunnyvale")

        self.browser.find_element_by_xpath("//button[@type='submit']").click()

# TODO: Add more Selenium tests - need to see if can add session / dummy data


if __name__ == "__main__":
    import unittest

    unittest.main()
