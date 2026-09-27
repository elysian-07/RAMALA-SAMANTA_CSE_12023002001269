from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from utilities.config_reader import ConfigReader
from utilities.logger import get_logger

log = get_logger("driver")


def get_driver():
    browser = ConfigReader.get("browser", "browser", "chrome").lower()
    headless = ConfigReader.get_bool("browser", "headless", False)
    log.info("Launching %s (headless=%s)", browser, headless)

    if browser == "chrome":
        opts = ChromeOptions()
        opts.page_load_strategy = "eager"
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--disable-notifications")
        if headless:
            opts.add_argument("--headless=new")
        driver = webdriver.Chrome(options=opts)
    elif browser == "firefox":
        opts = FirefoxOptions()
        opts.page_load_strategy = "eager"
        if headless:
            opts.add_argument("-headless")
        driver = webdriver.Firefox(options=opts)
    elif browser == "edge":
        opts = EdgeOptions()
        opts.page_load_strategy = "eager"
        if headless:
            opts.add_argument("--headless=new")
        driver = webdriver.Edge(options=opts)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()
    return driver
