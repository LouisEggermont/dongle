from __future__ import annotations
from itertools import product
from typing import Dict, List, Optional

from wallet import DENOMINATIONS


def _expand_wallet(wallet: Dict[str, int]) -> List[int]:
    notes: List[int] = []
    for denom in DENOMINATIONS:
        notes.extend([denom] * int(wallet.get(str(denom), 0)))
    return notes


def summarize_notes(notes: List[int]) -> Dict[int, int]:
    summary: Dict[int, int] = {}
    for note in notes:
        summary[note] = summary.get(note, 0) + 1
    return dict(sorted(summary.items(), reverse=True))


def best_payment_options(wallet: Dict[str, int], price: int, limit: int = 3) -> List[dict]:
    """Return practical payment combinations from the user's physical notes.

    The search is exhaustive over note counts per denomination, which is tiny for an MVP wallet.
    It ranks exact payment first, then lowest overpay/change, then fewer notes.
    """
    if price <= 0:
        return []

    counts_by_denom = [(d, int(wallet.get(str(d), 0))) for d in DENOMINATIONS]
    ranges = [range(c + 1) for _, c in counts_by_denom]
    options = []

    for combo in product(*ranges):
        if not any(combo):
            continue
        total = sum(qty * denom for qty, (denom, _) in zip(combo, counts_by_denom))
        if total >= price:
            note_count = sum(combo)
            notes = {denom: qty for qty, (denom, _) in zip(combo, counts_by_denom) if qty}
            options.append({
                "give": total,
                "change": total - price,
                "notes": notes,
                "note_count": note_count,
                "exact": total == price,
            })

    options.sort(key=lambda x: (not x["exact"], x["change"], x["note_count"], x["give"]))
    return options[:limit]
