import logging
from datetime import datetime
from utilities.config_reader import ROOT_DIR

_LOG_FILE = ROOT_DIR / "logs" / f"automation_{datetime.now():%Y%m%d}.log"


def get_logger(name="framework"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s | %(levelname)-7s | %(name)s | %(message)s")
        file_handler = logging.FileHandler(_LOG_FILE, encoding="utf-8")
        file_handler.setFormatter(fmt)
        console = logging.StreamHandler()
        console.setFormatter(fmt)
        logger.addHandler(file_handler)
        logger.addHandler(console)
        logger.propagate = False
    return logger
