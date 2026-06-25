from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import streamlit as st
from streamlit_option_menu import option_menu

from model import predict_banknotes
from payment import best_payment_options
from storage import load_wallet, reset_wallet, save_wallet
from styles import apply_styles
from wallet import DENOMINATIONS, add_counts, convert_vnd, format_vnd, total_vnd

BASE = Path(__file__).parent
DATA_PATH = BASE / "data" / "banknotes.json"
ASSET_DIR = BASE / "assets"

NAV_ITEMS = [
    ("Wallet", "wallet2"),
    ("Scan", "camera"),
    ("Pay", "credit-card"),
    ("Explore", "geo-alt"),
]

st.set_page_config(page_title="Dongle", page_icon="🇻🇳", layout="centered")
apply_styles()


@st.cache_data
def load_banknote_data() -> dict:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {"common": {}, "bills": data}
    return data


BANKNOTE_DATA = load_banknote_data()
BANKNOTE_COMMON = BANKNOTE_DATA.get("common", {})
BANKNOTES = BANKNOTE_DATA.get("bills", [])
BANKNOTE_MAP = {item["denomination"]: item for item in BANKNOTES}


if "wallet" not in st.session_state:
    st.session_state.wallet = load_wallet()
if "detected" not in st.session_state:
    st.session_state.detected = {}
if "nav" not in st.session_state:
    st.session_state.nav = "Wallet"


def persist_wallet() -> None:
    save_wallet(st.session_state.wallet)


# def note_asset(denomination: int) -> str:
#     return str(ASSET_DIR / f"{denomination}.jpg")

def note_asset(denomination: int) -> str:
    for ext in (".jpg", ".png", ".svg"):
        path = ASSET_DIR / f"{denomination}{ext}"
        if path.exists():
            return str(path)

    raise FileNotFoundError(f"No image found for denomination {denomination}")


def render_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="">
            <h1>{title}</h1>

        </div>
        """,
        unsafe_allow_html=True,
    )


def render_balance_card() -> None:
    total = total_vnd(st.session_state.wallet)
    fx = convert_vnd(total)
    st.markdown(
        f"""
        <div class="balance-card">
            <div class="label">Total balance</div>
            <div class="amount">{format_vnd(total)}</div>
            <div class="fx-row">
                <div class="fx-chip">USD<strong>${fx['USD']:.2f}</strong></div>
                <div class="fx-chip">EUR<strong>€{fx['EUR']:.2f}</strong></div>
                <div class="fx-chip">GBP<strong>£{fx['GBP']:.2f}</strong></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_note_line(denomination: int, count: int, editable: bool = False) -> None:
    with st.container():
        left, right = st.columns([1.1, 0.9])
        left.image(note_asset(denomination), width="stretch")
        # mid.markdown(f"**{BANKNOTE_MAP[denomination]['label']}**")
        # mid.caption(BANKNOTE_MAP[denomination]["tip"])
        if editable:
            new_count = right.number_input(
                "Qty",
                min_value=0,
                max_value=99,
                value=int(count),
                key=f"qty_{denomination}",
                label_visibility="collapsed",
            )
            if int(new_count) != int(count):
                st.session_state.wallet[str(denomination)] = int(new_count)
                persist_wallet()
                st.rerun()
        else:
            right.markdown(
                f"<div style='text-align:right;font-size:1.35rem;font-weight:700;color:#0f172a;'>× {count}</div>",
                unsafe_allow_html=True,
            )


def screen_wallet() -> None:
    render_header("Your Wallet", "")
    render_balance_card()

    st.markdown('<div class="section-title">Your cash</div>', unsafe_allow_html=True)
    for denom in DENOMINATIONS:
        render_note_line(denom, st.session_state.wallet.get(str(denom), 0), editable=True)
        st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    if col1.button("Save wallet", type="primary", width="stretch"):
        persist_wallet()
        st.toast("Wallet saved locally")
    if col2.button("Reset wallet", width="stretch"):
        st.session_state.wallet = reset_wallet()
        st.rerun()


def screen_scan() -> None:
    render_header("Scan Cash", "Snap or upload a photo, then add detected notes to your wallet.")
    st.info("The AI hook is in `model.py`. Replace `predict_banknotes()` with your Colab model inference code.")

    mode = st.segmented_control("Input", ["Camera", "Upload"], default="Upload")
    image_file = None
    if mode == "Camera":
        image_file = st.camera_input("Take a photo of the banknotes", label_visibility="collapsed")
    else:
        image_file = st.file_uploader(
            "Upload a banknote photo",
            type=["png", "jpg", "jpeg", "webp"],
            label_visibility="collapsed",
        )

    if image_file:
        st.image(image_file, caption="Input image", width="stretch")
        if st.button("Run AI detection", type="primary", width="stretch"):
            st.session_state.detected = predict_banknotes(image_file)
            st.rerun()

    detected: Dict[int, int] = {int(k): int(v) for k, v in st.session_state.detected.items()}
    if detected:
        st.markdown('<div class="section-title">Detected notes</div>', unsafe_allow_html=True)
        for denom, qty in detected.items():
            if qty > 0 and denom in BANKNOTE_MAP:
                render_note_line(denom, qty)
        detected_total = sum(k * v for k, v in detected.items())
        st.success(f"Detected total: {format_vnd(detected_total)}")
        c1, c2 = st.columns(2)
        if c1.button("Add to wallet", type="primary", width="stretch"):
            st.session_state.wallet = add_counts(st.session_state.wallet, detected)
            persist_wallet()
            st.session_state.detected = {}
            st.toast("Detected cash added")
            st.rerun()
        if c2.button("Clear detection", width="stretch"):
            st.session_state.detected = {}
            st.rerun()


def screen_pay() -> None:
    render_header("Payment Assistant", "Enter a bill amount and get the simplest way to pay with your cash.")
    render_balance_card()
    st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)

    price = st.number_input("Purchase amount (VND)", min_value=0, step=1000, value=185000)
    options = best_payment_options(st.session_state.wallet, int(price))

    if int(price) <= 0:
        st.warning("Enter a purchase amount to get a recommendation.")
    elif not options:
        st.error("Your wallet does not have enough cash for this amount.")
    else:
        st.markdown('<div class="section-title">Suggested payments</div>', unsafe_allow_html=True)
        for idx, opt in enumerate(options, start=1):
            title = (
                "Exact payment"
                if opt["exact"]
                else f"Give {format_vnd(opt['give'])}, expect {format_vnd(opt['change'])} change"
            )
            with st.expander(f"Option {idx}: {title}", expanded=idx == 1):
                cols = st.columns(min(3, max(1, len(opt["notes"]))))
                for i, (denom, qty) in enumerate(opt["notes"].items()):
                    with cols[i % len(cols)]:
                        st.image(note_asset(denom), width="stretch")
                        st.markdown(f"**{BANKNOTE_MAP[denom]['label']} × {qty}**")


def screen_explore() -> None:
    render_header("Currency Explorer", "Browse Vietnamese banknotes and the stories behind them.")
    selected = st.selectbox(
        "Choose a banknote",
        DENOMINATIONS,
        format_func=lambda d: BANKNOTE_MAP[d]["label"],
    )
    item = BANKNOTE_MAP[selected]
    back = item.get("back", {})
    if isinstance(back, str):
        back = {"title": back, "location": "", "description": ""}

    common_front = BANKNOTE_COMMON.get("front", {})
    series_key = item.get("series")
    series = BANKNOTE_COMMON.get("series", {}).get(series_key, {})

    with st.container(border=True):
        st.image(note_asset(selected), width="stretch")
        st.subheader(item["label"])
        if series:
            introduced = series.get("introduced")
            introduced_text = f", introduced in {introduced}" if introduced else ""
            st.caption(f"{series.get('material', series_key.title())}{introduced_text}")

        st.markdown(f"**Front:** {item['front']}")
        if common_front.get("description"):
            with st.expander(common_front.get("title", "Common front details")):
                st.write(common_front["description"])

        st.markdown(f"**Back:** {back.get('title', '')}")
        if back.get("location"):
            st.caption(back["location"])
        if back.get("description"):
            st.write(back["description"])

        st.write(item["culture"])
        if series.get("description"):
            with st.expander("About this note series"):
                st.write(series["description"])
        st.info(item["tip"])


SCREENS = {
    "Wallet": screen_wallet,
    "Scan": screen_scan,
    "Pay": screen_pay,
    "Explore": screen_explore,
}


def render_bottom_nav() -> None:
    nav_labels = [label for label, _ in NAV_ITEMS]
    selected_nav = option_menu(
        menu_title=None,
        options=nav_labels,
        icons=[icon for _, icon in NAV_ITEMS],
        default_index=nav_labels.index(st.session_state.nav),
        orientation="horizontal",
        styles={
            "container": {
                "padding": "0.45rem 0.55rem",
                "background-color": "transparent",
            },
            "nav": {
                "display": "grid",
                "grid-template-columns": f"repeat({len(NAV_ITEMS)}, minmax(0, 1fr))",
                "gap": "0.25rem",
                "margin": "0",
            },
            "nav-link": {
                "display": "flex",
                "flex-direction": "column",
                "align-items": "center",
                "justify-content": "center",
                "gap": "0.12rem",
                "min-height": "3.35rem",
                "padding": "0.35rem 0.2rem",
                "border-radius": "16px",
                "color": "#475569",
                "font-size": "0.76rem",
                "font-weight": "600",
                "text-align": "center",
                "white-space": "nowrap",
            },
            "nav-link-selected": {
                "background-color": "#ccfbf1",
                "color": "#0f766e",
            },
            "icon": {
                "font-size": "1.18rem",
                "margin": "0",
            },
        },
        key="bottom_nav",
    )

    if selected_nav != st.session_state.nav:
        st.session_state.nav = selected_nav


render_bottom_nav()
SCREENS[st.session_state.nav]()
