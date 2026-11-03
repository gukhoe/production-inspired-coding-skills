def calculate_total(items):
    """Calculate total price in cents, rejecting negative quantity."""
    total = 0
    for price, quantity in items:
        if price < 0 or quantity < 0:
            raise ValueError("negative input")
        total += price * quantity
    return total
