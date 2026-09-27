import unittest

from tests.base_test import BaseTest
from utilities.csv_reader import read_csv, resolve_credentials


class LoginUnittest(BaseTest):

    def test_login_page_loads(self):
        self.login_page.load()
        self.assertIn("/login", self.login_page.current_url)
        self.assertIn("Login", self.login_page.title)

    def test_login_data_driven(self):
        """Every row of login_data.csv is executed as its own sub-test."""
        for row in read_csv("login_data.csv"):
            with self.subTest(case=row["test_case"]):
                email, password = resolve_credentials(row)
                self.login_page.load().login(email, password)

                if row["expected"] == "success":
                    self.assertTrue(self.login_page.is_logged_in(),
                                    f"{row['test_case']}: login should succeed")
                    self.login_page.logout()
                else:
                    self.assertFalse(self.login_page.is_logged_in(),
                                     f"{row['test_case']}: login should fail")
                    if row["expected_message"]:
                        self.assertIn(row["expected_message"],
                                      self.login_page.get_error_message())


if __name__ == "__main__":
    unittest.main()
