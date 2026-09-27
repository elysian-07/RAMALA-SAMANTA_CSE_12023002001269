import pytest

from utilities.csv_reader import read_csv, resolve_credentials

LOGIN_DATA = read_csv("login_data.csv")


@pytest.mark.smoke
@pytest.mark.login
def test_login_page_title(login_page):
    login_page.load()
    login_page.wait_for_title_contains("Login")
    assert "Login" in login_page.title


@pytest.mark.regression
@pytest.mark.login
@pytest.mark.parametrize("row", LOGIN_DATA, ids=[r["test_case"] for r in LOGIN_DATA])
def test_login_data_driven(login_page, row):
    email, password = resolve_credentials(row)
    login_page.load().login(email, password)

    if row["expected"] == "success":
        assert login_page.is_logged_in(), "Expected successful login"
    else:
        assert not login_page.is_logged_in(), "Login should have failed"
        if row["expected_message"]:
            assert row["expected_message"] in login_page.get_error_message()