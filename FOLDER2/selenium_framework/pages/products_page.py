from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductsPage(BasePage):
    PATH = "/products"

    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BTN = (By.ID, "submit_search")
    PAGE_HEADING = (By.CSS_SELECTOR, "h2.title.text-center")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".features_items .product-image-wrapper")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".features_items .productinfo p")

    def load(self):
        self.open(self.PATH)
        return self

    def search(self, keyword):
        self.log.info("Searching for '%s'", keyword)
        self.type(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BTN)
        return self

    def heading(self):
        return self.text_of(self.PAGE_HEADING)

    def result_count(self):
        return len(self.find_all(self.PRODUCT_CARDS))

    def result_names(self):
        return [e.text.strip() for e in self.find_all(self.PRODUCT_NAMES)]
