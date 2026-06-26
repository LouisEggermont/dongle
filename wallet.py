from __future__ import annotations
from typing import Dict

DENOMINATIONS = [500000, 200000, 100000, 50000, 20000, 10000, 5000, 2000, 1000]
DEMO_RATES = {"USD": 0.000039, "EUR": 0.000036, "GBP": 0.000031}


def total_vnd(wallet: Dict[str, int]) -> int:
    return sum(int(denom) * int(count) for denom, count in wallet.items())


def convert_vnd(amount_vnd: int) -> Dict[str, float]:
    return {currency: amount_vnd * rate for currency, rate in DEMO_RATES.items()}


def format_vnd(amount: int) -> str:
    return f"{amount:,.0f} VND"


def add_counts(wallet: Dict[str, int], counts: Dict[int | str, int]) -> Dict[str, int]:
    updated = dict(wallet)
    for denom, qty in counts.items():
        key = str(denom)
        if key in updated:
            updated[key] = max(0, int(updated[key]) + int(qty))
    return updated


def subtract_counts(wallet: Dict[str, int], counts: Dict[int | str, int]) -> Dict[str, int]:
    updated = dict(wallet)
    for denom, qty in counts.items():
        key = str(denom)
        if key not in updated:
            continue
        remaining = int(updated[key]) - int(qty)
        if remaining < 0:
            raise ValueError(f"Not enough {key} VND notes in wallet")
        updated[key] = remaining
    return updated
