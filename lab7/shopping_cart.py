"""Parse shopping cart entries, promotions, and delivery pincodes."""

import re


ZONES = {"1": "North", "2": "North", "3": "West", "4": "West",
         "5": "South", "6": "South", "7": "East", "8": "East"}

ITEM = re.compile(r"([^:,]+):\s*([0-9]+)\s*x\s*([0-9]+)")
PROMO = re.compile(r"OFF([0-9]+)", re.IGNORECASE | re.ASCII)
PINCODE = re.compile(r"[1-8][0-9]{5}")


def cart_total(cart):
    """Return the total, 0 for an empty cart, or None for invalid input."""
    if not isinstance(cart, str):
        return None
    if not cart.strip():
        return 0

    total = 0
    for item in cart.split(","):
        match = ITEM.fullmatch(item.strip())
        if match is None or not match[1].strip():
            return None
        try:
            price, quantity = int(match[2]), int(match[3])
        except ValueError:
            return None
        if quantity == 0:
            return None
        total += price * quantity
    return total


def promo_percent(code):
    """Return the percentage for an OFF code, or None if it is invalid."""
    if not isinstance(code, str):
        return None
    match = PROMO.fullmatch(code.strip())
    if match is None:
        return None
    try:
        percent = int(match[1])
    except ValueError:
        return None
    return percent if percent <= 100 else None


def delivery_zone(pincode):
    """Return the delivery zone for a supported six-digit PIN, or None."""
    if not isinstance(pincode, str):
        return None
    pincode = pincode.strip()
    if PINCODE.fullmatch(pincode) is None:
        return None
    return ZONES[pincode[0]]


def main():
    print("==== Running cart_total ====")
    cart = input("Enter cart as name:pricexqty CSV (e.g. pen:10x2,book:250x1): ")
    total = cart_total(cart)
    if total is None:
        print("Invalid cart. Check the item names, prices and quantities.")
    else:
        print("Cart Total:", total)

    print("\n==== Running promo_percent ====")
    code = input("Enter a promo code (e.g. OFF20): ")
    percent = promo_percent(code)
    if percent is None:
        print("Invalid promo code. Enter OFF followed by a number from 0 to 100.")
    else:
        print("Discount Percent:", percent)

    print("\n==== Running delivery_zone ====")
    pincode = input("Enter a 6 digit pincode (e.g. 560085): ")
    zone = delivery_zone(pincode)
    if zone is None:
        print("Invalid pincode. Enter six digits starting with 1 to 8.")
    else:
        print("Delivery Zone:", zone)


if __name__ == "__main__":
    main()
