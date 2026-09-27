"""Shared fixtures + hook that captures a screenshot on failure and embeds it
in the pytest-html report. Works for both pytest-style and unittest tests."""
import base64

import pytest
from pytest_html import extras

from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utilities.driver_factory import get_driver
from utilities.screenshot import take_screenshot


@pytest.fixture
def driver():
    drv = get_driver()
    yield drv
    drv.quit()


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture
def products_page(driver):
    return ProductsPage(driver)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when in ("setup", "call") and report.failed:
        driver = item.funcargs.get("driver") if hasattr(item, "funcargs") else None
        if driver is None:  # unittest.TestCase subclasses keep it on self
            driver = getattr(getattr(item, "instance", None), "driver", None)
        if driver is None:
            return

        path = take_screenshot(driver, item.nodeid)
        if path:
            encoded = base64.b64encode(path.read_bytes()).decode()
            report.extras = getattr(report, "extras", []) + [extras.image(encoded)]
