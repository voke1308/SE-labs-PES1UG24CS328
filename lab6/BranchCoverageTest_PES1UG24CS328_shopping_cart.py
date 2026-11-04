"""Lab 6 - Prajin Ravi Shankar, PES1UG24CS328, Section 5-F."""

import pytest

from shopping_cart import cart_discount, item_total, shipping_fee


@pytest.mark.parametrize("category, price, qty, expected", [
    ("food", 100, 1, 105),
    ("electronics", 100, 1, 118),
    ("clothing", 100, 1, 112),
    ("food", 100, 9, 945),       # Just below the bulk threshold.
    ("food", 100, 10, 945),      # Bulk discount starts here.
    ("food", 100, 11, 1039),
    ("electronics", 100, 10, 1062),
    ("clothing", 100, 10, 1008),
    ("food", 0, 1, 0),
    ("food", 0, 10, 0),
    ("food", 19, 1, 19),        # GST uses floor division.
    ("food", 19, 11, 198),      # 209 - 20 + 9.
])
def test_item_totals_and_boundaries(category, price, qty, expected):
    assert item_total(category, price, qty) == expected


@pytest.mark.parametrize("category", ["books", "", "Food"])
def test_unknown_category(category):
    with pytest.raises(ValueError, match="^unknown category$"):
        item_total(category, 100, 1)


@pytest.mark.parametrize("price, qty", [(-1, 1), (100, 0), (100, -1), (-1, 0)])
def test_invalid_price_or_quantity(price, qty):
    # Check both sides of the 'or', including when price is valid.
    with pytest.raises(ValueError, match="^invalid price or quantity$"):
        item_total("food", price, qty)


@pytest.mark.parametrize("value, expected", [
    (0, 0), (1999, 0), (2000, 200), (2001, 200),
    (4999, 200), (5000, 500), (5001, 500),
])
def test_discount_thresholds(value, expected):
    assert cart_discount(value, False, "") == expected


@pytest.mark.parametrize("value, prime, coupon, expected", [
    (999, False, "FLAT10", 0),
    (1000, False, "FLAT10", 100),
    (1001, False, "FLAT10", 100),
    (1000, False, "", 0),
    (1000, False, "OTHER", 0),
    (1000, False, "flat10", 0),
    (0, True, "", 100),
    (2000, True, "", 300),
    (5000, True, "", 600),
    (1000, True, "FLAT10", 200),
    (2000, True, "FLAT10", 500),
    (5000, True, "FLAT10", 1100),
    (5000, False, "FLAT10", 1000),
])
def test_prime_and_coupon_combinations(value, prime, coupon, expected):
    assert cart_discount(value, prime, coupon) == expected


@pytest.mark.parametrize("value, prime, express, expected", [
    (0, False, False, 40),
    (499, False, False, 40), (499, False, True, 140),
    (500, False, False, 0), (500, False, True, 100),
    (501, False, False, 0), (501, False, True, 100),
    (499, True, False, 0), (499, True, True, 50),
    (500, True, False, 0), (500, True, True, 50),
    (501, True, False, 0), (501, True, True, 50),
])
def test_shipping_options(value, prime, express, expected):
    assert shipping_fee(value, prime, express) == expected
