"""Deliberately defective synthetic ledger for the connection audit demo."""
balance = 100
seen = set()


def apply_event(event_id, amount):
    global balance
    # Defect: a retry with the same event ID changes state again.
    balance += amount
    return balance
