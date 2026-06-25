import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap');

        :root {
            --bg: #eef1f5;
            --surface: #ffffff;
            --ink: #0f172a;
            --muted: #64748b;
            --brand: #0d9488;
            --brand-dark: #0f766e;
            --brand-soft: #ccfbf1;
            --border: #e2e8f0;
            --shadow: 0 8px 30px rgba(15, 23, 42, 0.06);
            --nav-height: 76px;
            --safe-bottom: env(safe-area-inset-bottom, 0px);
        }

        html, body, [class*="css"] {
            font-family: "DM Sans", -apple-system, BlinkMacSystemFont, sans-serif;
        }

        #MainMenu, footer, header[data-testid="stHeader"] {
            visibility: hidden;
            height: 0;
        }

        .stApp {
            background: linear-gradient(180deg, #f8fafc 0%, var(--bg) 100%);
        }

        .block-container {
            max-width: 480px;
            padding-top: 1rem;
            padding-bottom: calc(var(--nav-height) + var(--safe-bottom) + 1.5rem);
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero {
            border-radius: 24px;
            padding: 1.35rem 1.25rem;
            background: linear-gradient(145deg, #ecfdf5 0%, #f0f9ff 55%, #ffffff 100%);
            border: 1px solid #d1fae5;
            box-shadow: var(--shadow);
            margin-bottom: 0.25rem;
        }

        .hero h1 {
            margin: 0 0 0.35rem 0;
            font-size: 1.65rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            color: var(--ink);
        }

        .hero .muted {
            color: var(--muted);
            font-size: 0.92rem;
            line-height: 1.45;
        }

        .section-title {
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--muted);
            margin: 1.25rem 0 0.65rem 0;
        }

        .balance-card {
            background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%);
            border-radius: 22px;
            padding: 1.15rem 1.2rem;
            color: white;
            box-shadow: 0 14px 34px rgba(13, 148, 136, 0.28);
            margin: 0.85rem 0 0.35rem 0;
        }

        .balance-card .label {
            font-size: 0.78rem;
            opacity: 0.85;
            font-weight: 500;
        }

        .balance-card .amount {
            font-size: 1.85rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            margin: 0.15rem 0 0.75rem 0;
        }

        .fx-row {
            display: flex;
            gap: 0.5rem;
        }

        .fx-chip {
            flex: 1;
            background: rgba(255, 255, 255, 0.16);
            border: 1px solid rgba(255, 255, 255, 0.22);
            border-radius: 14px;
            padding: 0.55rem 0.65rem;
            font-size: 0.78rem;
            line-height: 1.2;
        }

        .fx-chip strong {
            display: block;
            font-size: 0.95rem;
            font-weight: 700;
        }

        div[data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 0.75rem 0.85rem;
            box-shadow: var(--shadow);
        }

        div[data-testid="stMetric"] label {
            color: var(--muted) !important;
            font-size: 0.75rem !important;
        }

        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-size: 1rem !important;
            font-weight: 700 !important;
            color: var(--ink) !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--surface);
            border: 1px solid var(--border) !important;
            border-radius: 18px !important;
            padding: 0.65rem 0.85rem !important;
            box-shadow: var(--shadow);
            margin-bottom: 0.55rem;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] img {
            border-radius: 10px;
        }

        .stButton > button {
            border-radius: 14px;
            font-weight: 600;
            min-height: 2.75rem;
            border: 1px solid var(--border);
            box-shadow: none;
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, var(--brand-dark), var(--brand));
            border: none;
            color: white;
        }

        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #115e59, var(--brand-dark));
            border: none;
            color: white;
        }

        .stButton > button[kind="secondary"] {
            background: var(--surface);
        }

        div[data-testid="stAlert"] {
            border-radius: 16px;
            border: 1px solid var(--border);
        }

        div[data-testid="stExpander"] {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            box-shadow: var(--shadow);
            overflow: hidden;
        }

        div[data-testid="stFileUploader"], div[data-testid="stCameraInput"] {
            background: var(--surface);
            border: 1px dashed #cbd5e1;
            border-radius: 18px;
            padding: 0.35rem;
        }

        div[data-testid="stSegmentedControl"] {
            background: #e2e8f0;
            border-radius: 999px;
            padding: 0.2rem;
        }

        .bottom-nav-shell {
            position: fixed;
            left: 0;
            right: 0;
            bottom: 0;
            height: calc(var(--nav-height) + var(--safe-bottom));
            padding-bottom: var(--safe-bottom);
            background: rgba(255, 255, 255, 0.92);
            border-top: 1px solid var(--border);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            z-index: 999;
            box-shadow: 0 -8px 24px rgba(15, 23, 42, 0.06);
        }

        div[data-testid="stRadio"] {
            position: fixed;
            left: 50%;
            transform: translateX(-50%);
            bottom: calc(8px + var(--safe-bottom));
            z-index: 1000;
            width: min(480px, calc(100vw - 1rem));
            margin: 0;
            padding: 0;
            background: transparent;
            border: none;
            box-shadow: none;
        }

        div[data-testid="stRadio"] > label {
            display: none !important;
        }

        div[data-testid="stRadio"] div[role="radiogroup"] {
            display: grid !important;
            grid-template-columns: repeat(4, 1fr);
            gap: 0.25rem;
            width: 100%;
            background: transparent;
        }

        div[data-testid="stRadio"] div[role="radiogroup"] > label {
            display: flex !important;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 0.15rem;
            min-height: 58px;
            margin: 0 !important;
            padding: 0.45rem 0.25rem !important;
            border-radius: 16px !important;
            border: none !important;
            background: transparent !important;
            color: var(--muted) !important;
            font-size: 0.68rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.01em;
            transition: background 0.15s ease, color 0.15s ease;
        }

        div[data-testid="stRadio"] div[role="radiogroup"] > label span {
            white-space: pre-line;
            text-align: center;
            line-height: 1.15;
        }

        div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
            background: var(--brand-soft) !important;
            color: var(--brand-dark) !important;
        }

        div[data-testid="stRadio"] div[role="radiogroup"] > label input {
            position: absolute;
            opacity: 0;
            pointer-events: none;
        }

        div[data-testid="stNumberInput"] input {
            border-radius: 12px;
            text-align: center;
            font-weight: 700;
        }

        h2, h3 {
            letter-spacing: -0.02em;
        }

        img {
            border-radius: 12px;
        }
        </style>
        <div class="bottom-nav-shell" aria-hidden="true"></div>
        """,
        unsafe_allow_html=True,
    )
