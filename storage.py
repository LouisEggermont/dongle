from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

STORAGE_DIR = Path(__file__).parent / "storage"
WALLET_PATH = STORAGE_DIR / "wallet.json"


def _empty_wallet() -> Dict[str, int]:
    return {str(d): 0 for d in [500000, 200000, 100000, 50000, 20000, 10000, 5000, 2000, 1000]}


def load_wallet() -> Dict[str, int]:
    STORAGE_DIR.mkdir(exist_ok=True)
    if not WALLET_PATH.exists():
        wallet = _empty_wallet()
        save_wallet(wallet)
        return wallet
    try:
        data = json.loads(WALLET_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        data = _empty_wallet()
    wallet = _empty_wallet()
    for denom, count in data.items():
        if denom in wallet:
            wallet[denom] = max(0, int(count))
    return wallet


def save_wallet(wallet: Dict[str, int]) -> None:
    STORAGE_DIR.mkdir(exist_ok=True)
    WALLET_PATH.write_text(json.dumps(wallet, indent=2), encoding="utf-8")


def reset_wallet() -> Dict[str, int]:
    wallet = _empty_wallet()
    save_wallet(wallet)
    return wallet
