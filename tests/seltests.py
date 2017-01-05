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
        self.browser.get('http://localhost:5000/')
        self.assertEqual(self.browser.title, 'Breadcrumbs || Homepage')


if __name__ == "__main__":
    import unittest

    unittest.main()
