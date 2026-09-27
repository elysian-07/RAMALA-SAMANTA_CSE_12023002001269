import re
from datetime import datetime
from utilities.config_reader import ROOT_DIR
from utilities.logger import get_logger

log = get_logger("screenshot")
SCREENSHOT_DIR = ROOT_DIR / "screenshots"


def take_screenshot(driver, test_name):
    """Save a PNG named <test>_<timestamp>.png and return its path (or None)."""
    safe = re.sub(r"[^\w\-]+", "_", test_name)[:100]
    path = SCREENSHOT_DIR / f"{safe}_{datetime.now():%Y%m%d_%H%M%S}.png"
    try:
        SCREENSHOT_DIR.mkdir(exist_ok=True)
        driver.save_screenshot(str(path))
        log.info("Screenshot saved: %s", path)
        return path
    except Exception as exc:  # never let a screenshot break the test run
        log.error("Could not take screenshot: %s", exc)
        return None
