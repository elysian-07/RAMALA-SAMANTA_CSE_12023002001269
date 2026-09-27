<div align="center">

# 🧪 Selenium Python Automation Framework

### Unittest + PyTest + Page Object Model

A scalable, production-style Selenium WebDriver framework that automates the
**Login** and **Product Search** features of a live e-commerce site.

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4-43B02A?logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![PyTest](https://img.shields.io/badge/PyTest-9.x-0A9EDC?logo=pytest&logoColor=white)](https://pytest.org/)
[![Unittest](https://img.shields.io/badge/Unittest-builtin-yellow)](https://docs.python.org/3/library/unittest.html)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](#)

[Overview](#-what-this-project-demonstrates) •
[Structure](#-project-structure) •
[Setup](#-setup) •
[Running Tests](#-running-the-tests) •
[Design Notes](#-design-notes)

</div>

---

## 📋 Overview

This framework targets [automationexercise.com](https://automationexercise.com)
and covers two core e-commerce flows end-to-end:

| Feature | What's tested |
|---|---|
| 🔐 **Login** | Valid login, wrong password, unregistered user, empty-field validation |
| 🔍 **Product Search** | Valid keywords returning results, invalid keywords returning none |

It's built to demonstrate **framework design**, not just individual test
scripts — Page Object Model, dual test-runner support, externalized config,
data-driven testing, automatic failure diagnostics, and HTML reporting.

---

## ✨ What this project demonstrates

| Capability | How it's implemented |
|---|---|
| **Page Object Model** | Locators and page actions live in `pages/`, isolated from test logic. A UI change means editing one class, not every test. |
| **Two test runners, one framework** | The same page objects and utilities back both `unittest`- and `pytest`-style tests. `pytest` runs both suites in a single command. |
| **Data-driven testing** | Login and search scenarios are defined in CSV, not hardcoded. New scenarios = new rows, no code changes. |
| **Externalized configuration** | Base URL, browser, headless mode, wait times, and credentials live in `config.ini`, with environment-variable overrides for CI. |
| **Failure diagnostics** | Any failure auto-captures a screenshot, embeds it in the HTML report, and logs every step to a timestamped file. |

---

## 🛠️ Tech Stack

`Python 3.14` · `Selenium 4` · `PyTest` · `pytest-html` · `unittest` · `configparser` · `csv`

---

## 📁 Project Structure

```
selenium_framework/
├── config/
│   └── config.ini              # base URL, browser, headless, waits, credentials
├── pages/                      # Page Object Model
│   ├── base_page.py            #   shared Selenium wrappers (click/type/wait)
│   ├── home_page.py
│   ├── login_page.py
│   └── products_page.py
├── utilities/
│   ├── config_reader.py        # config.ini + env-var overrides
│   ├── driver_factory.py       # Chrome / Firefox / Edge, headless support
│   ├── csv_reader.py           # loads CSV test data
│   ├── screenshot.py           # screenshot capture on failure
│   └── logger.py               # console + file logging
├── testdata/
│   ├── login_data.csv          # valid / invalid / empty-field login scenarios
│   └── search_data.csv         # valid and invalid search keywords
├── tests/
│   ├── base_test.py            # unittest base class (setUp/tearDown)
│   ├── test_login_unittest.py
│   ├── test_search_unittest.py
│   ├── test_login_pytest.py
│   └── test_search_pytest.py
├── conftest.py                 # pytest fixtures + failure-screenshot hook
├── pytest.ini                  # markers + HTML report config
├── run_unittest.py             # standalone unittest runner
├── requirements.txt
├── reports/                    # generated HTML reports
├── screenshots/                # generated failure screenshots
└── logs/                       # generated run logs
```

---

## ✅ Test Scenarios Covered

**Login** — `testdata/login_data.csv`

| Scenario | Expected result |
|---|---|
| Valid email + password | ✅ Login succeeds |
| Valid email + wrong password | ❌ Login fails, error message shown |
| Unregistered email | ❌ Login fails, error message shown |
| Empty email | ❌ Blocked by field validation |
| Empty password | ❌ Blocked by field validation |
| Empty email and password | ❌ Blocked by field validation |

**Product Search** — `testdata/search_data.csv`

| Scenario | Expected result |
|---|---|
| Keyword with matches (tshirt, dress, jeans, top) | ✅ Results returned |
| Keyword with no matches | ✅ Zero results, no error |

---

## 🚀 Setup

```bash
git clone <this-repo-url>
cd selenium_framework

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Then:
1. Register an account manually at automationexercise.com.
2. Add its email/password to `config/config.ini` under `[credentials]`
   — or set `VALID_EMAIL` / `VALID_PASSWORD` as environment variables
   (recommended — keeps real credentials out of version control).

---

## ▶️ Running the Tests

```bash
pytest                                 # everything (unittest + pytest suites)
pytest -m smoke                        # quick sanity check
pytest -m "login and regression"       # filter by marker
pytest tests/test_search_pytest.py     # a single file

pytest -n auto                         # parallel run (pip install pytest-xdist)
BROWSER=firefox HEADLESS=true pytest   # override config (Windows: set BROWSER=firefox)

python run_unittest.py                 # unittest suite, without pytest
```

| Output | Location |
|---|---|
| 📊 HTML report | `reports/report.html` |
| 📸 Failure screenshots | `screenshots/` (also embedded in the report) |
| 📝 Run logs | `logs/` |

---


## 🎥 Video Demonstrations

The demonstration videos are hosted externally because the video files are too large to store directly in this GitHub repository.

### Assignment 1 - 4

▶️ **[Watch CapStone Project Video](https://drive.google.com/file/d/13orL3fi43da-G-w3L_iACYt7y7g4oPTP/view?usp=sharing)**

---

## 🧩 Design Notes

- **POM** — `base_page.py` wraps Selenium actions with explicit waits and a
  JS-click fallback for intercepted clicks; every page class inherits from it.
  Tests call page methods (`login()`, `search()`) and assert outcomes — they
  never touch a locator directly.
- **Unittest** — `BaseTest` centralizes driver setup/teardown; `subTest`
  gives a separate pass/fail result per CSV row within one test method.
- **PyTest** — fixtures provide the driver and page objects; `parametrize`
  drives CSV-based scenarios; markers (`smoke`, `regression`, `login`,
  `search`) allow selective runs. PyTest also discovers and runs the
  `unittest.TestCase` classes, so one command covers both styles.
- **Screenshot on failure** — a `pytest_runtest_makereport` hook in
  `conftest.py` captures pytest failures; `BaseTest.tearDown` covers plain
  `unittest` runs — both save to `screenshots/` and log the path.

---

## 🔭 Possible Extensions

- Parallel execution via `pytest-xdist` (already wired up — see Run section)
- CI pipeline (GitHub Actions / Jenkins) running `pytest` on push
- Selenium Grid / remote WebDriver support in `driver_factory.py`
- Retry logic for flaky network-dependent assertions

---

<div align="center">

## 👤 Author

**Ramala Samanta**
B.Tech CSE Student · Built as a Selenium/Python test automation capstone project

</div>