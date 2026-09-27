"""Central configuration access. Environment variables override config.ini."""
import configparser
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
CONFIG_FILE = ROOT_DIR / "config" / "config.ini"


class ConfigReader:
    _parser = None

    @classmethod
    def _load(cls):
        if cls._parser is None:
            cls._parser = configparser.ConfigParser()
            cls._parser.read(CONFIG_FILE)
        return cls._parser

    @classmethod
    def get(cls, section, key, fallback=None):
        env_value = os.getenv(key.upper())      # e.g. BROWSER=firefox pytest
        if env_value:
            return env_value
        return cls._load().get(section, key, fallback=fallback)

    @classmethod
    def get_bool(cls, section, key, fallback=False):
        value = cls.get(section, key, str(fallback))
        return str(value).strip().lower() in ("true", "1", "yes")

    @classmethod
    def base_url(cls):
        return cls.get("app", "base_url").rstrip("/")

    @classmethod
    def explicit_wait(cls):
        return int(cls.get("browser", "explicit_wait", "15"))
