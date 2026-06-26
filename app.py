from __future__ import annotations

import base64
import json
from html import escape
from pathlib import Path
from typing import Dict

import streamlit as st
from streamlit_option_menu import option_menu

from model import predict_banknotes
from payment import best_payment_options
from storage import load_wallet, reset_wallet, save_wallet
from styles import apply_styles
from wallet import DENOMINATIONS, add_counts, convert_vnd, format_vnd, subtract_counts, total_vnd

BASE = Path(__file__).parent
DATA_PATH = BASE / "data" / "banknotes.json"
ASSET_DIR = BASE / "assets"

NAV_ITEMS = [
    ("Wallet", "wallet2"),
    ("Scan", "camera"),
    ("Pay", "credit-card"),
    ("Explore", "geo-alt"),
]

NOTE_ACCENTS = {
    "teal": "#0f766e",
    "red": "#b91c1c",
    "green": "#15803d",
    "pink": "#be185d",
    "blue": "#1d4ed8",
    "brown": "#92400e",
    "navy": "#1e3a8a",
    "gray": "#475569",
    "lightgray": "#64748b",
}

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
if "bill_rendering" not in st.session_state:
    st.session_state.bill_rendering = "Simplified"


def persist_wallet() -> None:
    save_wallet(st.session_state.wallet)


def note_asset(denomination: int) -> str:
    if st.session_state.bill_rendering == "Simplified":
        asset_candidates = [
            f"{denomination}.jpg",
            f"{denomination}.png",
            f"{denomination}.svg",
            f"note_{denomination}.jpg",
            f"note_{denomination}.png",
            f"note_{denomination}.svg",
        ]
    else:
        asset_candidates = [
            f"note_{denomination}.jpg",
            f"note_{denomination}.png",
            f"note_{denomination}.svg",
            f"{denomination}.svg",
            f"{denomination}.png",
            f"{denomination}.jpg",
        ]

    for filename in asset_candidates:
        path = ASSET_DIR / filename
        if path.exists():
            return str(path)

    raise FileNotFoundError(f"No image found for denomination {denomination}")


def render_bill_style_control() -> None:
    st.markdown('<div class="display-settings-wrap">', unsafe_allow_html=True)
    with st.expander("Display settings"):
        selected = st.segmented_control(
            "Bill style",
            ["Simplified", "Realistic"],
            default=st.session_state.bill_rendering,
            key="bill_style_control",
        )
        if selected and selected != st.session_state.bill_rendering:
            st.session_state.bill_rendering = selected
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def render_header(title: str, subtitle: str) -> None:
    logo_svg = (ASSET_DIR / "logo.svg").read_text(encoding="utf-8")
    svg_base64 = base64.b64encode(logo_svg.encode("utf-8")).decode("ascii")
    logo_src = f"data:image/svg+xml;base64,{svg_base64}"
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:0.75rem;">
            <img src="{logo_src}" alt="logo" style="width:3rem;height:auto;display:block;" />
            <div>
                <h1 style="margin:0;">{escape(title)}</h1>
            </div>
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


def note_accent(item: dict) -> str:
    return NOTE_ACCENTS.get(item.get("color_hint", ""), "#0f766e")


def render_info_block(label: str, title: str, body: str, meta: str = "") -> None:
    meta_html = f'<div class="explore-meta">{escape(meta)}</div>' if meta else ""
    st.markdown(
        f"""
        <div class="explore-info-block">
            <div class="explore-kicker">{escape(label)}</div>
            <h3>{escape(title)}</h3>
            {meta_html}
            <p>{escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_culture_block(body: str) -> None:
    st.markdown(
        f"""
        <div class="explore-culture-block">
            <div class="explore-kicker">Cultural meaning</div>
            <h3>Why this scene matters</h3>
            <p>{escape(body)}</p>
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
    render_bill_style_control()

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
                if st.button("Pay with this option", type="primary", width="stretch", key=f"pay_option_{idx}"):
                    try:
                        st.session_state.wallet = subtract_counts(st.session_state.wallet, opt["notes"])
                    except ValueError as exc:
                        st.error(str(exc))
                    else:
                        persist_wallet()
                        st.toast(f"Paid {format_vnd(opt['give'])} from wallet")
                        st.rerun()


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
    material = series.get("material", series_key.title() if series_key else "Banknote")
    introduced = series.get("introduced")
    introduced_text = f"Introduced {introduced}" if introduced else "In circulation"
    back_title = back.get("title", "Back design")
    back_location = back.get("location", "")

    st.markdown(
        f"""
        <div class="explore-note-hero" style="--note-accent: {note_accent(item)};">
            <div>
                <div class="explore-kicker">Selected note</div>
                <h2>{escape(item["label"])}</h2>
                <div class="explore-chip-row">
                    <span>{escape(material)}</span>
                    <span>{escape(introduced_text)}</span>
                    <span>{escape(back_location or back_title)}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.image(note_asset(selected), width="stretch")

    render_info_block(
        "Front",
        item.get("front", "Portrait of Ho Chi Minh"),
        common_front.get("description", ""),
        common_front.get("title", ""),
    )
    render_info_block(
        "Back",
        back_title,
        back.get("description", ""),
        back_location,
    )
    render_culture_block(item.get("culture", ""))

    st.markdown(
        f"""
        <div class="explore-tip">
            <div class="explore-kicker">Practical use</div>
            <p>{escape(item.get("tip", ""))}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if series.get("description"):
        with st.expander(f"About {material.lower()} notes"):
            st.write(series["description"])


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
