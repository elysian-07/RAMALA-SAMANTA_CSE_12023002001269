from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "/login"

    EMAIL = (By.CSS_SELECTOR, "[data-qa='login-email']")
    PASSWORD = (By.CSS_SELECTOR, "[data-qa='login-password']")
    LOGIN_BTN = (By.CSS_SELECTOR, "[data-qa='login-button']")
    ERROR_MSG = (By.XPATH, "//form[@action='/login']/p")
    LOGGED_IN_AS = (By.XPATH, "//a[contains(.,'Logged in as')]")
    LOGOUT_LINK = (By.XPATH, "//a[@href='/logout']")

    def load(self):
        self.open(self.PATH)
        return self

    def login(self, email, password):
        self.log.info("Logging in as '%s'", email)
        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)
        return self

    def is_logged_in(self):
        return self.is_visible(self.LOGGED_IN_AS, timeout=5)

    def get_error_message(self):
        if self.is_visible(self.ERROR_MSG, timeout=3):
            return self.text_of(self.ERROR_MSG)
        return ""

    def logout(self):
        self.click(self.LOGOUT_LINK)
