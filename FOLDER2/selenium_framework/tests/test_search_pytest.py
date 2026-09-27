import pytest

from utilities.csv_reader import read_csv

SEARCH_DATA = read_csv("search_data.csv")


@pytest.mark.smoke
@pytest.mark.search
def test_search_box_visible(products_page):
    products_page.load()
    assert products_page.is_visible(products_page.SEARCH_INPUT)


@pytest.mark.regression
@pytest.mark.search
@pytest.mark.parametrize("row", SEARCH_DATA, ids=[r["test_case"] for r in SEARCH_DATA])
def test_product_search(products_page, row):
    products_page.load().search(row["keyword"])
    assert products_page.heading().upper() == "SEARCHED PRODUCTS"

    if row["expected"] == "found":
        assert products_page.result_count() > 0
    else:
        assert products_page.result_count() == 0


@pytest.mark.regression
@pytest.mark.search
def test_search_results_match_keyword(products_page):
    products_page.load().search("dress")
    names = products_page.result_names()
    assert names, "Expected at least one result"
    assert any("dress" in n.lower() for n in names), \
        f"No product name contains 'dress': {names}"