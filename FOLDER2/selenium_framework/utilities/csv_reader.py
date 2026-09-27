import csv
from utilities.config_reader import ROOT_DIR, ConfigReader

TESTDATA_DIR = ROOT_DIR / "testdata"


def read_csv(filename):
    """Return CSV rows as a list of dicts (header row = keys)."""
    with open(TESTDATA_DIR / filename, newline="", encoding="utf-8") as f:
        return [dict(row) for row in csv.DictReader(f)]


def resolve_credentials(row):
    """Replace <VALID_EMAIL>/<VALID_PASSWORD> placeholders with config values."""
    email, password = row["email"], row["password"]
    if email == "<VALID_EMAIL>":
        email = ConfigReader.get("credentials", "valid_email")
    if password == "<VALID_PASSWORD>":
        password = ConfigReader.get("credentials", "valid_password")
    return email, password
