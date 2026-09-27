import unittest

from tests.base_test import BaseTest
from utilities.csv_reader import read_csv


class SearchUnittest(BaseTest):

    def test_products_page_loads(self):
        self.products_page.load()
        self.assertTrue(self.products_page.is_visible(self.products_page.SEARCH_INPUT))

    def test_search_data_driven(self):
        for row in read_csv("search_data.csv"):
            with self.subTest(case=row["test_case"]):
                page = self.products_page.load().search(row["keyword"])
                self.assertEqual("SEARCHED PRODUCTS", page.heading().upper())
                if row["expected"] == "found":
                    self.assertGreater(page.result_count(), 0)
                else:
                    self.assertEqual(0, page.result_count())


if __name__ == "__main__":
    unittest.main()
