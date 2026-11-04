"""Corrected synthetic ledger. Assumes the demo's single-threaded HTTP server."""
balance = 100
seen = set()


def apply_event(event_id, amount):
    global balance
    if event_id in seen:
        return balance
    balance += amount
    seen.add(event_id)
    return balance
