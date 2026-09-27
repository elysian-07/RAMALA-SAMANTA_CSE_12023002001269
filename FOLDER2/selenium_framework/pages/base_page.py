from selenium.common.exceptions import (ElementClickInterceptedException,
                                        TimeoutException)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.config_reader import ConfigReader
from utilities.logger import get_logger


class BasePage:
    """Reusable Selenium wrappers shared by all page objects."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, ConfigReader.explicit_wait())
        self.log = get_logger(self.__class__.__name__)

    def open(self, path=""):
        url = f"{ConfigReader.base_url()}{path}"
        self.log.info("Opening %s", url)
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except ElementClickInterceptedException:   # ads / overlays
            self.log.warning("Click intercepted, using JS click: %s", locator)
            self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator):
        return self.find(locator).text

    def is_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_title_contains(self, text, timeout=None):
        """Wait until the browser title contains the given text (handles
        pages where the title updates after initial load)."""
        WebDriverWait(self.driver, timeout or ConfigReader.explicit_wait()).until(
            EC.title_contains(text)
        )

    @property
    def title(self):
        return self.driver.title

    @property
    def current_url(self):
        return self.driver.current_url