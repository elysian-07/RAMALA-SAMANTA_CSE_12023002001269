from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    LOGIN_LINK = (By.XPATH, "//a[@href='/login']")
    PRODUCTS_LINK = (By.XPATH, "//a[@href='/products']")
    LOGO = (By.CSS_SELECTOR, ".logo img")

    def load(self):
        self.open("/")
        return self

    def is_loaded(self):
        return self.is_visible(self.LOGO)

    def go_to_login(self):
        self.click(self.LOGIN_LINK)

    def go_to_products(self):
        self.click(self.PRODUCTS_LINK)
