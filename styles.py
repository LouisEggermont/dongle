import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap');

        :root {
            color-scheme: light;
            --bg: #eef1f5;
            --surface: #ffffff;
            --ink: #0f172a;
            --muted: #475569;
            --brand: #0f766e;
            --brand-dark: #115e59;
            --brand-soft: #ccfbf1;
            --border: #e2e8f0;
            --shadow: 0 8px 30px rgba(15, 23, 42, 0.06);
            --nav-height: 76px;
            --safe-bottom: env(safe-area-inset-bottom, 0px);
        }

        html, body, [class*="css"] {
            font-family: "DM Sans", -apple-system, BlinkMacSystemFont, sans-serif;
        }

        html, body, .stApp {
            color: var(--ink);
            overflow-x: hidden;
        }

        #MainMenu, footer, header[data-testid="stHeader"] {
            visibility: hidden;
            height: 0;
        }

        .stApp {
            background: linear-gradient(180deg, #f8fafc 0%, var(--bg) 100%);
        }

        div[data-testid="stAppViewContainer"],
        div[data-testid="stSidebarContent"],
        div[data-testid="stHeader"] {
            color-scheme: light;
        }

        .block-container {
            max-width: 480px;
            padding-top: 1rem;
            padding-bottom: calc(var(--nav-height) + var(--safe-bottom) + 2rem);
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .page-header {
            display: grid;
            grid-template-columns: 3rem minmax(0, 1fr);
            align-items: center;
            gap: 0.7rem;
            margin: 0.25rem 0 0.85rem 0;
        }

        .page-logo,
        .page-logo svg {
            width: 3rem !important;
            height: 3rem !important;
        }

        .page-logo {
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            border-radius: 999px;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
        }

        .page-logo svg {
            display: block;
            flex: 0 0 auto;
        }

        .page-title {
            min-width: 0;
        }

        .page-title h1 {
            margin: 0 0 0.1rem 0 !important;
            color: var(--ink) !important;
            font-size: 1.65rem !important;
            font-weight: 700 !important;
            line-height: 1.1 !important;
            letter-spacing: 0 !important;
            overflow-wrap: anywhere;
        }

        .page-title p {
            margin: 0 !important;
            color: var(--muted) !important;
            font-size: 0.9rem !important;
            line-height: 1.35 !important;
        }

        .bottom-nav-shell {
            position: fixed;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 999;
            height: calc(var(--nav-height) + var(--safe-bottom));
            padding: 0 1rem var(--safe-bottom);
            background: rgba(255, 255, 255, 0.94);
            border-top: 1px solid var(--border);
            box-shadow: 0 -10px 28px rgba(15, 23, 42, 0.08);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
        }

        iframe[title*="streamlit_option_menu"] {
            position: fixed !important;
            left: 50% !important;
            right: auto !important;
            bottom: var(--safe-bottom) !important;
            z-index: 1000 !important;
            display: block;
            width: min(480px, calc(100vw - 2rem)) !important;
            height: var(--nav-height) !important;
            margin: 0 !important;
            transform: translateX(-50%);
            border: 0 !important;
            border-radius: 18px !important;
            background: transparent !important;
        }

        div[data-testid="stIFrame"]:has(iframe[title*="streamlit_option_menu"]),
        div[data-testid="stCustomComponentV1"]:has(iframe[title*="streamlit_option_menu"]) {
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: visible !important;
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

        .explore-note-hero {
            position: relative;
            overflow: hidden;
            box-sizing: border-box;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1rem 1rem 0.95rem 1rem;
            margin: 0.85rem 0 0.75rem 0;
            box-shadow: var(--shadow);
        }

        .explore-note-hero::before {
            content: "";
            position: absolute;
            inset: 0 auto 0 0;
            width: 0.42rem;
            background: var(--note-accent, var(--brand));
        }

        .explore-note-hero h2 {
            margin: 0.15rem 0 0.65rem 0;
            color: var(--ink);
            font-size: 1.75rem;
            font-weight: 700;
            line-height: 1.08;
        }

        .explore-kicker {
            color: var(--muted);
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            line-height: 1.2;
            text-transform: uppercase;
        }

        .explore-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
        }

        .explore-chip-row span {
            display: inline-flex;
            align-items: center;
            min-height: 1.85rem;
            padding: 0.3rem 0.55rem;
            border-radius: 999px;
            background: #f1f5f9;
            border: 1px solid var(--border);
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 700;
            line-height: 1.15;
        }

        .explore-info-block {
            box-sizing: border-box;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 0.95rem 1rem;
            box-shadow: var(--shadow);
            margin: 0.75rem 0;
        }

        .explore-culture-block {
            box-sizing: border-box;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 0.95rem 1rem;
            box-shadow: var(--shadow);
            margin: 0.75rem 0;
        }

        .explore-info-block h3,
        .explore-culture-block h3 {
            margin: 0.22rem 0 0.15rem 0;
            color: var(--ink);
            font-size: 1.05rem;
            font-weight: 700;
            line-height: 1.25;
        }

        .explore-info-block p,
        .explore-culture-block p,
        .explore-tip p {
            margin: 0.55rem 0 0 0;
            color: var(--ink);
            font-size: 0.94rem;
            line-height: 1.55;
        }

        .explore-meta {
            color: var(--muted);
            font-size: 0.82rem;
            font-weight: 600;
            line-height: 1.35;
        }

        .banknote-flip-stage {
            position: relative;
            display: grid;
            place-items: center;
            width: 100%;
            max-width: 100%;
            min-height: 8.8rem;
            margin: 0.7rem 0 0.85rem 0;
            overflow: hidden;
            box-sizing: border-box;
            perspective: 900px;
            border-radius: 12px;
        }

        .banknote-flip-stage::after {
            content: "";
            position: absolute;
            inset: 0;
            border-radius: 12px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.45), transparent);
            opacity: 0;
            pointer-events: none;
            transform: translateX(-60%);
            animation: banknoteFlipSheen 520ms ease-out both;
        }

        .banknote-flip-stage img {
            display: block;
            width: 100%;
            height: auto;
            border-radius: 12px;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.14);
            animation: banknoteFlipToFront 520ms cubic-bezier(0.2, 0.75, 0.18, 1) both;
            transform-origin: center;
            backface-visibility: hidden;
        }

        .banknote-flip-stage.is-back img,
        .banknote-flip-stage.is-back .banknote-missing-back {
            animation-name: banknoteFlipToBack;
        }

        .banknote-flip-stage.is-front img,
        .banknote-flip-stage.is-front .banknote-missing-back {
            animation-name: banknoteFlipToFront;
        }

        .banknote-side-label {
            position: absolute;
            top: 0.55rem;
            left: 0.55rem;
            z-index: 2;
            display: inline-flex;
            align-items: center;
            min-height: 1.75rem;
            padding: 0.28rem 0.56rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(226, 232, 240, 0.9);
            color: var(--ink);
            font-size: 0.72rem;
            font-weight: 800;
            line-height: 1;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.09);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }

        .banknote-missing-back {
            box-sizing: border-box;
            width: 100%;
            max-width: 100%;
            min-height: 8.8rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 0.28rem;
            padding: 1.2rem 1.05rem;
            border-radius: 12px;
            border: 1px solid var(--border);
            background:
                linear-gradient(90deg, var(--note-accent, var(--brand)) 0 0.45rem, transparent 0.45rem),
                repeating-linear-gradient(135deg, #f8fafc 0 0.55rem, #eef2f7 0.55rem 1.1rem);
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.1);
            animation: banknoteFlipToFront 520ms cubic-bezier(0.2, 0.75, 0.18, 1) both;
            transform-origin: center;
            backface-visibility: hidden;
        }

        .banknote-missing-back h3 {
            margin: 0.08rem 0 0 0;
            color: var(--ink);
            font-size: 1.15rem;
            font-weight: 800;
            line-height: 1.16;
        }

        .banknote-missing-back p {
            margin: 0;
            color: var(--muted);
            font-size: 0.88rem;
            font-weight: 700;
        }

        @keyframes banknoteFlipToBack {
            from {
                opacity: 0.2;
                transform: rotateY(-180deg) scale(0.96);
            }
            48% {
                opacity: 0.55;
                transform: rotateY(-88deg) scale(0.98);
            }
            to {
                opacity: 1;
                transform: rotateY(0deg) scale(1);
            }
        }

        @keyframes banknoteFlipToFront {
            from {
                opacity: 0.2;
                transform: rotateY(180deg) scale(0.96);
            }
            48% {
                opacity: 0.55;
                transform: rotateY(88deg) scale(0.98);
            }
            to {
                opacity: 1;
                transform: rotateY(0deg) scale(1);
            }
        }

        @keyframes banknoteFlipSheen {
            0% {
                opacity: 0;
                transform: translateX(-70%);
            }
            35% {
                opacity: 0.7;
            }
            100% {
                opacity: 0;
                transform: translateX(70%);
            }
        }

        .explore-tip {
            box-sizing: border-box;
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            border-radius: 18px;
            padding: 0.95rem 1rem;
            margin: 0.75rem 0 0.9rem 0;
        }

        .balance-card {
            background: linear-gradient(135deg, var(--brand-dark) 0%, var(--brand) 100%);
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
            background: linear-gradient(135deg, #134e4a, var(--brand-dark));
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

        .display-settings-wrap {
            padding: 0.85rem 0 0.25rem;
        }

        .display-settings-wrap div[data-testid="stExpander"] {
            margin: 0;
        }

        .display-settings-wrap div[data-testid="stExpanderDetails"] {
            padding: 0.15rem 1rem 1rem;
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
