"""Lab 6 - Prajin Ravi Shankar, PES1UG24CS328, Section 5-F."""

import pytest

from shopping_cart import cart_discount, item_total, shipping_fee


@pytest.mark.parametrize("category, price, qty, expected", [
    ("food", 100, 2, 210),
    ("electronics", 100, 10, 1062),
    ("clothing", 100, 1, 112),
])
def test_item_totals(category, price, qty, expected):
    assert item_total(category, price, qty) == expected


def test_unknown_category():
    with pytest.raises(ValueError, match="^unknown category$"):
        item_total("books", 100, 1)


def test_negative_price():
    with pytest.raises(ValueError, match="^invalid price or quantity$"):
        item_total("food", -1, 1)


@pytest.mark.parametrize("value, expected", [
    (5000, 1100), (2000, 500), (500, 100),
])
def test_discount_slabs(value, expected):
    assert cart_discount(value, True, "FLAT10") == expected


@pytest.mark.parametrize("value, prime, expected", [
    (100, True, 50), (500, False, 100), (499, False, 140),
])
def test_express_shipping(value, prime, expected):
    assert shipping_fee(value, prime, True) == expected
