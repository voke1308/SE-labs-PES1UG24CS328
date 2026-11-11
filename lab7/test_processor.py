"""Lab 7 Hypothesis tests for the assigned shopping cart application."""

import pytest
from hypothesis import given, settings, strategies as st

from shopping_cart import cart_total, delivery_zone, promo_percent


mixed_inputs = st.text() | st.none() | st.integers() | st.binary()
zones_by_digit = ("North", "North", "West", "West", "South", "South", "East", "East")


@settings(max_examples=150, derandomize=True)
@given(mixed_inputs)
def test_cart_total_no_crash(value):
    result = cart_total(value)
    assert result is None or (type(result) is int and result >= 0)


@settings(max_examples=150, derandomize=True)
@given(mixed_inputs)
def test_promo_percent_no_crash(value):
    result = promo_percent(value)
    assert result is None or (type(result) is int and 0 <= result <= 100)


@settings(max_examples=150, derandomize=True)
@given(mixed_inputs)
def test_delivery_zone_no_crash(value):
    result = delivery_zone(value)
    assert result is None or result in zones_by_digit


@settings(max_examples=150, derandomize=True)
@given(st.lists(st.tuples(st.integers(0, 10000), st.integers(1, 100)), max_size=12))
def test_cart_total_matches_sum(items):
    cart = ",".join(f"item{i}:{price}x{qty}" for i, (price, qty) in enumerate(items))
    assert cart_total(cart) == sum(price * qty for price, qty in items)


@settings(max_examples=150, derandomize=True)
@given(st.integers(0, 100), st.sampled_from(["OFF", "off", "Off"]))
def test_valid_promo_returns_its_percent(percent, prefix):
    assert promo_percent(f"{prefix}{percent}") == percent


@settings(max_examples=150, derandomize=True)
@given(st.integers(1, 8), st.integers(0, 99999))
def test_valid_pincode_maps_to_expected_zone(first_digit, suffix):
    assert delivery_zone(f"{first_digit}{suffix:05d}") == zones_by_digit[first_digit - 1]


@pytest.mark.parametrize("value", [None, "pen", "pen:10x0", "pen:-5x2", "pen:10x2,", ":10x2"])
def test_invalid_cart_is_rejected(value):
    assert cart_total(value) is None


@pytest.mark.parametrize("value", [None, "", "OFF", "SALE20", "OFF-1", "OFF101"])
def test_invalid_promo_is_rejected(value):
    assert promo_percent(value) is None


@pytest.mark.parametrize("value", [None, "", "5", "56008A", "960085", "５６００８５"])
def test_invalid_pincode_is_rejected(value):
    assert delivery_zone(value) is None
