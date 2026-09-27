"""unittest base class: driver setup/teardown + screenshot on failure."""
import os
import unittest

from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utilities.driver_factory import get_driver
from utilities.screenshot import take_screenshot


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver()
        self.login_page = LoginPage(self.driver)
        self.products_page = ProductsPage(self.driver)

    def tearDown(self):
        # Under pytest, conftest.py handles screenshots (and the HTML report).
        if "PYTEST_CURRENT_TEST" not in os.environ and self._has_failed():
            take_screenshot(self.driver, self.id())
        self.driver.quit()

    def _has_failed(self):
        result = getattr(getattr(self, "_outcome", None), "result", None)
        if result is None:
            return False
        problems = list(getattr(result, "failures", [])) + list(getattr(result, "errors", []))
        return any(test is self for test, _ in problems)
