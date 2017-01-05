"""Selenium Testing"""

import os
import sys

current_file_path = os.path.realpath(__file__)
current_dir = os.path.dirname(current_file_path)
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from unittest import TestCase
from selenium import webdriver


class SeleniumTests(TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        """Test title of homepage."""

        self.browser.get('http://localhost:5000/')
        self.assertEqual(self.browser.title, 'Breadcrumbs || Homepage')

    def test_signup_link(self):
        """Test signup links on homepage."""

        self.browser.get('http://localhost:5000/')
        signup_links = self.browser.find_elements_by_link_text('Sign up')

        for link in signup_links:
            link.click()




if __name__ == "__main__":
    import unittest

    unittest.main()
