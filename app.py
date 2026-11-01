
# ============================================================
# KUSHAL PRO MAX TRADING
# COMPLETE SINGLE FILE APPLICATION
# VERSION 1.0
# ============================================================

import streamlit as st
import streamlit.components.v1 as components
import json
import os
import bcrypt
import secrets
import tempfile
import html

from datetime import datetime, timedelta


# ============================================================
# SECTION 01: APPLICATION CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="KUSHAL PRO MAX TRADING",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

APP_NAME = "KUSHAL PRO MAX TRADING"

DB_FILE = "admin_config.json"
BACKUP_FILE = "admin_config.json.bak"


# ============================================================
# SECTION 02: MARKET CONFIGURATION
# ============================================================

MARKETS = {

    "Indian Market": {
        "icon": "🇮🇳",
        "description": "INDIAN STOCK MARKET",
        "default": "NSE:NIFTY",
        "symbols": {
            "NIFTY 50": "NSE:NIFTY",
            "BANK NIFTY": "NSE:BANKNIFTY",
            "SENSEX": "BSE:SENSEX",
            "RELIANCE": "NSE:RELIANCE",
            "TCS": "NSE:TCS",
            "INFOSYS": "NSE:INFY",
            "HDFC BANK": "NSE:HDFCBANK",
            "ICICI BANK": "NSE:ICICIBANK",
            "TATA MOTORS": "NSE:TATAMOTORS",
            "TATA POWER": "NSE:TATAPOWER",
            "WIPRO": "NSE:WIPRO",
            "HIMADRI SPECIALITY": "NSE:HSCL"
        }
    },

    "US Market": {
        "icon": "🇺🇸",
        "description": "UNITED STATES STOCK MARKET",
        "default": "NASDAQ:NDX",
        "symbols": {
            "NASDAQ 100": "NASDAQ:NDX",
            "S&P 500": "SP:SPX",
            "DOW JONES": "DJ:DJI",
            "APPLE": "NASDAQ:AAPL",
            "NVIDIA": "NASDAQ:NVDA",
            "TESLA": "NASDAQ:TSLA",
            "MICROSOFT": "NASDAQ:MSFT",
            "AMAZON": "NASDAQ:AMZN",
            "GOOGLE": "NASDAQ:GOOGL",
            "META": "NASDAQ:META"
        }
    },

    "Crypto Market": {
        "icon": "₿",
        "description": "CRYPTOCURRENCY MARKET",
        "default": "BINANCE:BTCUSDT",
        "symbols": {
            "BITCOIN": "BINANCE:BTCUSDT",
            "ETHEREUM": "BINANCE:ETHUSDT",
            "SOLANA": "BINANCE:SOLUSDT",
            "BNB": "BINANCE:BNBUSDT",
            "XRP": "BINANCE:XRPUSDT",
            "DOGECOIN": "BINANCE:DOGEUSDT",
            "CARDANO": "BINANCE:ADAUSDT",
            "AVALANCHE": "BINANCE:AVAXUSDT"
        }
    }
}


# ============================================================
# SECTION 03: SESSION INITIALIZATION
# ============================================================

DEFAULT_SESSION = {
    "page": "login",
    "current_user": None,
    "pin_verified": False,
    "failed_login_attempts": 0,
    "lockout_time": None,
    "failed_pin_attempts": 0,
    "pin_lockout_time": None,
    "otp_session": {
        "hash": None,
        "expiry": None,
        "attempts": 0
    },
    "selected_market": "Indian Market",
    "selected_symbols": {},
    "audit_logs": []
}

for key, value in DEFAULT_SESSION.items():
    if key not in st.session_state:
        st.session_state[key] = value.copy() if isinstance(value, (dict, list)) else value


# ============================================================
# SECTION 04: SECURITY FUNCTIONS
# ============================================================

def hash_secret(secret_text):

    return bcrypt.hashpw(
        secret_text.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_secret(secret_text, hashed_text):

    try:
        return bcrypt.checkpw(
            secret_text.encode("utf-8"),
            hashed_text.encode("utf-8")
        )
    except Exception:
        return False


def log_security_event(event_type, details):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.session_state.audit_logs.append(
        f"[{timestamp}] [{event_type}] {details}"
    )

    st.session_state.audit_logs = (
        st.session_state.audit_logs[-200:]
    )


# ============================================================
# SECTION 05: DATABASE FUNCTIONS
# ============================================================

def load_admin_data():

    if not os.path.exists(DB_FILE):
        return None

    try:
        with open(DB_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        required = [
            "user_id",
            "mobile",
            "password_hash",
            "pin_hash",
            "kds_hash"
        ]

        if not isinstance(data, dict):
            return None

        if not all(key in data for key in required):
            return None

        return data

    except Exception:

        try:
            with open(BACKUP_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            required = [
                "user_id",
                "mobile",
                "password_hash",
                "pin_hash",
                "kds_hash"
            ]

            if isinstance(data, dict) and all(
                key in data for key in required
            ):
                return data

        except Exception:
            pass

        return None


def save_admin_data(data):

    temp_name = None

    try:

        directory = os.path.dirname(DB_FILE) or "."

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=directory,
            delete=False
        ) as temp_file:

            json.dump(data, temp_file, indent=4)
            temp_name = temp_file.name

        if os.path.exists(DB_FILE):

            with open(DB_FILE, "r", encoding="utf-8") as old_file:
                old_data = json.load(old_file)

            backup_temp = BACKUP_FILE + ".tmp"

            with open(backup_temp, "w", encoding="utf-8") as backup:
                json.dump(old_data, backup, indent=4)

            os.replace(backup_temp, BACKUP_FILE)

        os.replace(temp_name, DB_FILE)

        log_security_event("DATABASE", "Master data saved.")

        return True

    except Exception as error:

        st.error(f"DATABASE ERROR: {error}")

        if temp_name and os.path.exists(temp_name):
            try:
                os.remove(temp_name)
            except OSError:
                pass

        return False


admin_data = load_admin_data()


# ============================================================
# SECTION 06: GLOBAL DESIGN
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&display=swap');

.stApp {
    background:
        radial-gradient(circle at top left,
        rgba(0,180,80,0.15), transparent 35%),
        radial-gradient(circle at top right,
        rgba(0,180,80,0.10), transparent 35%),
        #030806 !important;

    color: #e8fff0;
}

.block-container {
    max-width: 1350px;
    padding: 25px 30px 40px;
}

.main-header {
    background: linear-gradient(135deg,#071b10,#102b1b);
    border: 1px solid #168447;
    border-radius: 15px;
    padding: 22px 10px;
    text-align: center;
    margin-bottom: 24px;
    box-shadow: 0 0 25px #00ff6618;
}

.welcome-tag {
    color: #00f080;
    font-size: 12px;
    letter-spacing: 3px;
    font-weight: 800;
}

.main-title {
    color: #00f080;
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(20px, 4vw, 34px);
    font-weight: 900;
    letter-spacing: 2px;
    margin: 8px 0;
    text-shadow: 0 0 15px #00ff6655;
}

.sub-title {
    color: #87cda3;
    font-size: 11px;
    letter-spacing: 2px;
}

.heading-box {
    background: #0b2115;
    border: 1px solid #17683b;
    border-left: 4px solid #00e875;
    border-radius: 8px;
    padding: 13px;
    margin: 18px 0;
    color: #00ed7a;
    font-weight: 800;
    letter-spacing: 1px;
}

.market-card {
    background: linear-gradient(145deg,#10291b,#07130c);
    border: 1px solid #176b3a;
    border-radius: 13px;
    padding: 20px 10px;
    text-align: center;
    min-height: 120px;
    margin-bottom: 12px;
    box-shadow: 0 0 15px #00ff6610;
}

.market-card h3 {
    color: #4dff91;
    font-size: 17px;
}

.market-card p {
    color: #b5d9c2;
    font-size: 11px;
}

.stTextInput label,
.stSelectbox label {
    color: #00d878 !important;
    font-weight: 700 !important;
}

.stTextInput input {
    background: #10271a !important;
    color: #eafff0 !important;
    border: 1px solid #17683b !important;
}

.stButton button {
    width: 100%;
    min-height: 43px;
    background: #0d2b1d;
    color: #00e875;
    border: 1px solid #17683b;
    border-radius: 8px;
    font-weight: 800;
}

.stButton button:hover {
    background: #00d875;
    color: #001b0b;
    border-color: #00f080;
}

.stButton button[kind="primary"] {
    background: #00d875;
    color: #031008;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #09170f;
    border: 1px solid #174b30;
    border-radius: 12px;
}

.info-note {
    background: #10251a;
    border: 1px solid #245a38;
    border-radius: 8px;
    padding: 12px;
    color: #b9d8c4;
    font-size: 12px;
    margin: 10px 0;
}

.footer-box {
    text-align: center;
    color: #65a77f;
    border-top: 1px solid #174b30;
    padding: 15px;
    margin-top: 30px;
    font-size: 11px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SECTION 07: COMMON HEADER
# ============================================================

def render_header():

    st.markdown("""
    <div class="main-header">
        <div class="welcome-tag">WELCOME TO</div>
        <div class="main-title">⚡ KUSHAL PRO MAX TRADING</div>
        <div class="sub-title">
            ADVANCED FINANCIAL MARKET TERMINAL
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():

    st.markdown("""
    <div class="footer-box">
        KUSHAL PRO MAX TRADING |
        MARKET DATA SUBJECT TO PROVIDER AVAILABILITY
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# SECTION 08: MASTER ACCOUNT SETUP
# ============================================================

if admin_data is None:

    render_header()

    st.markdown(
        '<div class="heading-box">INITIAL MASTER SETUP</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        st.info("CREATE YOUR MASTER ACCOUNT.")

        new_user = st.text_input(
            "CREATE MASTER USER ID",
            key="setup_user"
        )

        mobile = st.text_input(
            "MOBILE NUMBER (10 DIGITS)",
            max_chars=10,
            key="setup_mobile"
        )

        password = st.text_input(
            "CREATE PASSWORD (MIN 8 CHARACTERS)",
            type="password",
            key="setup_password"
        )

        confirm_password = st.text_input(
            "CONFIRM PASSWORD",
            type="password",
            key="setup_confirm_password"
        )

        kds_code = st.text_input(
            "SECRET KDS RECOVERY CODE",
            type="password",
            key="setup_kds"
        )

        pin = st.text_input(
            "CREATE 6-DIGIT PIN",
            type="password",
            max_chars=6,
            key="setup_pin"
        )

        confirm_pin = st.text_input(
            "CONFIRM 6-DIGIT PIN",
            type="password",
            max_chars=6,
            key="setup_confirm_pin"
        )

        if st.button(
            "CREATE MASTER ACCOUNT →",
            type="primary"
        ):

            if not all([
                new_user,
                mobile,
                password,
                confirm_password,
                kds_code,
                pin,
                confirm_pin
            ]):

                st.error("PLEASE COMPLETE ALL FIELDS.")

            elif not mobile.isdigit() or len(mobile) != 10:

                st.error("MOBILE NUMBER MUST HAVE 10 DIGITS.")

            elif len(password) < 8:

                st.error("PASSWORD MUST HAVE AT LEAST 8 CHARACTERS.")

            elif password != confirm_password:

                st.error("PASSWORDS DO NOT MATCH.")

            elif len(kds_code) < 8:

                st.error("KDS RECOVERY CODE MUST HAVE AT LEAST 8 CHARACTERS.")

            elif not pin.isdigit() or len(pin) != 6:

                st.error("PIN MUST HAVE EXACTLY 6 DIGITS.")

            elif pin != confirm_pin:

                st.error("PINS DO NOT MATCH.")

            else:

                secure_data = {
                    "user_id": new_user.strip(),
                    "mobile": mobile.strip(),
                    "password_hash": hash_secret(password),
                    "pin_hash": hash_secret(pin),
                    "kds_hash": hash_secret(kds_code)
                }

                if save_admin_data(secure_data):

                    st.success("MASTER ACCOUNT CREATED.")
                    st.rerun()

    render_footer()


# ============================================================
# SECTION 09: MASTER LOGIN
# ============================================================

elif st.session_state.page == "login":

    render_header()

    st.markdown(
        '<div class="heading-box">SECURE MASTER LOGIN</div>',
        unsafe_allow_html=True
    )

    lockout = st.session_state.lockout_time

    if lockout and datetime.now() < lockout:

        remaining = int(
            (lockout - datetime.now()).total_seconds()
        )

        st.error(f"LOGIN LOCKED. TRY AGAIN IN {remaining} SECONDS.")

    else:

        if lockout:

            st.session_state.lockout_time = None
            st.session_state.failed_login_attempts = 0

        with st.container(border=True):

            user_id = st.text_input(
                "MASTER USER ID",
                key="login_user"
            )

            password = st.text_input(
                "MASTER PASSWORD",
                type="password",
                key="login_password"
            )

            if st.button(
                "AUTHENTICATE →",
                type="primary"
            ):

                valid_user = (
                    secrets.compare_digest(
                        user_id.strip(),
                        str(admin_data["user_id"])
                    )
                    and verify_secret(
                        password,
                        admin_data["password_hash"]
                    )
                )

                if valid_user:

                    st.session_state.failed_login_attempts = 0
                    st.session_state.current_user = user_id.strip()
                    st.session_state.page = "pin_verify"

                    log_security_event(
                        "LOGIN",
                        "Master login successful."
                    )

                    st.rerun()

                else:

                    st.session_state.failed_login_attempts += 1

                    if st.session_state.failed_login_attempts >= 5:

                        st.session_state.lockout_time = (
                            datetime.now() + timedelta(minutes=5)
                        )

                        st.error("5 FAILED ATTEMPTS. LOCKED FOR 5 MINUTES.")

                    else:

                        remaining = 5 - st.session_state.failed_login_attempts

                        st.error(
                            f"INVALID LOGIN. {remaining} ATTEMPTS REMAINING."
                        )

            if st.button("FORGOT PASSWORD / ID / PIN?"):

                st.session_state.page = "forgot_step1"
                st.rerun()

    render_footer()


# ============================================================
# SECTION 10: PIN VERIFICATION
# ============================================================

elif st.session_state.page == "pin_verify":

    render_header()

    st.markdown(
        '<div class="heading-box">6-DIGIT TERMINAL SECURITY PIN</div>',
        unsafe_allow_html=True
    )

    lockout = st.session_state.pin_lockout_time

    if lockout and datetime.now() < lockout:

        remaining = int(
            (lockout - datetime.now()).total_seconds()
        )

        st.error(f"PIN LOCKED. TRY AGAIN IN {remaining} SECONDS.")

    else:

        if lockout:

            st.session_state.pin_lockout_time = None
            st.session_state.failed_pin_attempts = 0

        with st.container(border=True):

            st.info("ENTER YOUR 6-DIGIT PIN TO OPEN YOUR TERMINAL.")

            pin_input = st.text_input(
                "TERMINAL PIN",
                type="password",
                max_chars=6,
                key="terminal_pin"
            )

            if st.button(
                "UNLOCK TERMINAL →",
                type="primary"
            ):

                if verify_secret(
                    pin_input,
                    admin_data["pin_hash"]
                ):

                    st.session_state.failed_pin_attempts = 0
                    st.session_state.pin_verified = True
                    st.session_state.page = "dashboard"

                    log_security_event(
                        "PIN",
                        "Terminal unlocked."
                    )

                    st.rerun()

                else:

                    st.session_state.failed_pin_attempts += 1

                    if st.session_state.failed_pin_attempts >= 5:

                        st.session_state.pin_lockout_time = (
                            datetime.now() + timedelta(minutes=5)
                        )

                        st.error("5 INCORRECT PINS. LOCKED FOR 5 MINUTES.")

                    else:

                        remaining = 5 - st.session_state.failed_pin_attempts

                        st.error(
                            f"INVALID PIN. {remaining} ATTEMPTS REMAINING."
                        )

            if st.button("FORGOT PIN?"):

                st.session_state.page = "forgot_step1"
                st.rerun()

            if st.button("← BACK TO LOGIN"):

                st.session_state.current_user = None
                st.session_state.pin_verified = False
                st.session_state.page = "login"

                st.rerun()

    render_footer()


# ============================================================
# SECTION 11: OTP DEMO RECOVERY
# ============================================================

elif st.session_state.page == "forgot_step1":

    render_header()

    st.markdown(
        '<div class="heading-box">ACCOUNT RECOVERY - DEMO OTP</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        st.warning(
            "DEMO MODE: OTP IS DISPLAYED ON SCREEN. "
            "THIS IS NOT REAL SMS VERIFICATION."
        )

        mobile = st.text_input(
            "REGISTERED MOBILE NUMBER",
            max_chars=10,
            key="recovery_mobile"
        )

        if st.button("GENERATE DEMO OTP"):

            if mobile.strip() == admin_data["mobile"]:

                otp = "".join(
                    str(secrets.randbelow(10))
                    for _ in range(6)
                )

                st.session_state.otp_session = {
                    "hash": hash_secret(otp),
                    "expiry": datetime.now() + timedelta(minutes=5),
                    "attempts": 0
                }

                st.session_state.demo_otp_display = otp

                st.success(
                    f"DEMO OTP: {otp} | VALID FOR 5 MINUTES"
                )

            else:

                st.error("REGISTERED MOBILE NUMBER NOT FOUND.")

        if st.session_state.otp_session["hash"]:

            if st.session_state.get("demo_otp_display"):

                st.info(
                    "Demo OTP: " +
                    st.session_state.demo_otp_display
                )

            otp_input = st.text_input(
                "ENTER 6-DIGIT OTP",
                type="password",
                max_chars=6,
                key="recovery_otp"
            )

            if st.button(
                "VERIFY OTP →",
                type="primary"
            ):

                otp_data = st.session_state.otp_session

                if datetime.now() > otp_data["expiry"]:

                    st.error("OTP EXPIRED. REQUEST A NEW OTP.")

                elif otp_data["attempts"] >= 3:

                    st.error("MAXIMUM OTP ATTEMPTS EXCEEDED.")

                elif verify_secret(
                    otp_input.strip(),
                    otp_data["hash"]
                ):

                    st.session_state.otp_session = {
                        "hash": None,
                        "expiry": None,
                        "attempts": 0
                    }

                    st.session_state.demo_otp_display = None
                    st.session_state.page = "forgot_step2"

                    st.rerun()

                else:

                    otp_data["attempts"] += 1

                    st.error(
                        f"INVALID OTP. ATTEMPT {otp_data['attempts']}/3"
                    )

        if st.button("← RETURN TO LOGIN"):

            st.session_state.page = "login"
            st.rerun()

    render_footer()


# ============================================================
# SECTION 12: PASSWORD / PIN / MASTER RECOVERY
# ============================================================

elif st.session_state.page == "forgot_step2":

    render_header()

    st.markdown(
        '<div class="heading-box">CREDENTIAL RECOVERY</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        choice = st.selectbox(
            "SELECT RECOVERY ACTION",
            [
                "RESET PASSWORD",
                "RESET 6-DIGIT PIN",
                "FULL RECOVERY VIA KDS CODE"
            ]
        )

        if choice == "RESET PASSWORD":

            new_password = st.text_input(
                "NEW PASSWORD",
                type="password"
            )

            confirm_password = st.text_input(
                "CONFIRM NEW PASSWORD",
                type="password"
            )

            if st.button("UPDATE PASSWORD", type="primary"):

                if len(new_password) < 8:

                    st.error("PASSWORD MUST HAVE AT LEAST 8 CHARACTERS.")

                elif new_password != confirm_password:

                    st.error("PASSWORDS DO NOT MATCH.")

                else:

                    admin_data["password_hash"] = hash_secret(new_password)

                    if save_admin_data(admin_data):

                        st.session_state.current_user = None
                        st.session_state.pin_verified = False
                        st.session_state.page = "login"

                        st.success("PASSWORD UPDATED.")
                        st.rerun()

        elif choice == "RESET 6-DIGIT PIN":

            new_pin = st.text_input(
                "NEW 6-DIGIT PIN",
                type="password",
                max_chars=6
            )

            confirm_pin = st.text_input(
                "CONFIRM NEW PIN",
                type="password",
                max_chars=6
            )

            if st.button("UPDATE PIN", type="primary"):

                if not new_pin.isdigit() or len(new_pin) != 6:

                    st.error("PIN MUST HAVE EXACTLY 6 DIGITS.")

                elif new_pin != confirm_pin:

                    st.error("PINS DO NOT MATCH.")

                else:

                    admin_data["pin_hash"] = hash_secret(new_pin)

                    if save_admin_data(admin_data):

                        st.session_state.current_user = None
                        st.session_state.pin_verified = False
                        st.session_state.page = "login"

                        st.success("PIN UPDATED.")
                        st.rerun()

        elif choice == "FULL RECOVERY VIA KDS CODE":

            st.warning("MASTER RECOVERY. KEEP YOUR KDS CODE SECRET.")

            kds = st.text_input(
                "KDS RECOVERY CODE",
                type="password"
            )

            new_user = st.text_input("NEW MASTER USER ID")

            new_password = st.text_input(
                "NEW PASSWORD",
                type="password"
            )

            new_pin = st.text_input(
                "NEW 6-DIGIT PIN",
                type="password",
                max_chars=6
            )

            if st.button("EXECUTE MASTER RECOVERY", type="primary"):

                if not verify_secret(kds, admin_data["kds_hash"]):

                    st.error("INVALID KDS RECOVERY CODE.")

                elif not new_user.strip():

                    st.error("NEW USER ID IS REQUIRED.")

                elif len(new_password) < 8:

                    st.error("PASSWORD MUST HAVE AT LEAST 8 CHARACTERS.")

                elif not new_pin.isdigit() or len(new_pin) != 6:

                    st.error("PIN MUST HAVE EXACTLY 6 DIGITS.")

                else:

                    admin_data["user_id"] = new_user.strip()
                    admin_data["password_hash"] = hash_secret(new_password)
                    admin_data["pin_hash"] = hash_secret(new_pin)

                    if save_admin_data(admin_data):

                        st.session_state.current_user = None
                        st.session_state.pin_verified = False
                        st.session_state.page = "login"

                        st.success("MASTER ACCOUNT UPDATED.")
                        st.rerun()

        if st.button("← BACK TO LOGIN"):

            st.session_state.page = "login"
            st.rerun()

    render_footer()


# ============================================================
# SECTION 13: MARKET SELECTION DASHBOARD
# ============================================================

elif st.session_state.page == "dashboard":

    if (
        not st.session_state.pin_verified
        or not st.session_state.current_user
    ):

        st.session_state.page = "login"
        st.session_state.pin_verified = False
        st.rerun()

    render_header()

    st.markdown(
        '<div class="heading-box">SELECT YOUR MARKET</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "WELCOME, " +
        html.escape(st.session_state.current_user)
    )

    columns = st.columns(3)

    for index, (market_name, market) in enumerate(MARKETS.items()):

        with columns[index]:

            st.markdown(
                f"""
                <div class="market-card">
                    <h3>{market['icon']} {html.escape(market_name)}</h3>
                    <p>{html.escape(market['description'])}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                f"OPEN {market_name.upper()}",
                key=f"market_{index}",
                type="primary"
            ):

                st.session_state.selected_market = market_name
                st.session_state.page = "market_view"

                st.session_state.selected_symbols[market_name] = (
                    market["default"]
                )

                st.rerun()

    render_footer()


# ============================================================
# SECTION 14: MARKET WATCHLIST
# ============================================================

elif st.session_state.page == "market_view":

    if (
        not st.session_state.pin_verified
        or not st.session_state.current_user
    ):

        st.session_state.page = "login"
        st.session_state.pin_verified = False
        st.rerun()

    market_name = st.session_state.selected_market

    if market_name not in MARKETS:

        st.session_state.page = "dashboard"
        st.rerun()

    market = MARKETS[market_name]

    render_header()

    top1, top2 = st.columns([3, 1])

    with top1:

        st.markdown(
            f"""
            <div class="heading-box">
                {market['icon']} {html.escape(market_name).upper()} DASHBOARD
            </div>
            """,
            unsafe_allow_html=True
        )

    with top2:

        if st.button("← ALL MARKETS"):

            st.session_state.page = "dashboard"
            st.rerun()

    st.markdown(
        '<div class="heading-box">MARKET WATCHLIST</div>',
        unsafe_allow_html=True
    )

    symbols = market["symbols"]

    watch_columns = st.columns(4)

    for index, (name, symbol) in enumerate(symbols.items()):

        with watch_columns[index % 4]:

            st.markdown(
                f"""
                <div class="market-card">
                    <h3>{html.escape(name)}</h3>
                    <p>{html.escape(symbol)}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "VIEW CHART",
                key=f"view_{market_name}_{index}"
            ):

                st.session_state.selected_symbols[market_name] = symbol
                st.rerun()


# ============================================================
# SECTION 15: MARKET SYMBOL SEARCH
# ============================================================

    st.markdown(
        '<div class="heading-box">SEARCH STOCK / INDEX / COIN</div>',
        unsafe_allow_html=True
    )

    search_text = st.text_input(
        "SEARCH SYMBOL",
        placeholder="Example: RELIANCE / NVIDIA / BITCOIN",
        key=f"search_{market_name}"
    )

    matching_names = [
        name
        for name in symbols
        if search_text.strip().lower() in name.lower()
    ] if search_text.strip() else list(symbols.keys())

    if matching_names:

        selected_name = st.selectbox(
            "SELECT SYMBOL",
            matching_names,
            key=f"select_{market_name}"
        )

        if st.button(
            "OPEN SELECTED SYMBOL",
            type="primary",
            key=f"open_symbol_{market_name}"
        ):

            st.session_state.selected_symbols[market_name] = (
                symbols[selected_name]
            )

            st.rerun()

    elif search_text.strip():

        st.info(
            "SYMBOL NOT FOUND IN THE CURRENT DEMO LIST."
        )


# ============================================================
# SECTION 16: TRADINGVIEW CHART
# ============================================================

    selected_symbol = st.session_state.selected_symbols.get(
        market_name,
        market["default"]
    )

    if selected_symbol not in symbols.values():

        selected_symbol = market["default"]

        st.session_state.selected_symbols[market_name] = selected_symbol

    st.markdown(
        '<div class="heading-box">ADVANCED MARKET CHART</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="info-note">
            Chart supplied by TradingView. Data availability,
            exchange permissions and delay depend on the provider.
            This chart is for market viewing, not trade execution.
        </div>
        """,
        unsafe_allow_html=True
    )

    safe_symbol = html.escape(selected_symbol, quote=True)

    chart_html = f"""
    <div class="tradingview-widget-container"
         style="height:560px;width:100%">

      <div id="tv_chart"
           style="height:540px;width:100%">
      </div>

      <script src="https://s3.tradingview.com/tv.js"></script>

      <script>
        new TradingView.widget({{
            "autosize": true,
            "symbol": "{safe_symbol}",
            "interval": "15",
            "timezone": "Asia/Kolkata",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "enable_publishing": false,
            "allow_symbol_change": false,
            "hide_side_toolbar": false,
            "withdateranges": true,
            "details": true,
            "hotlist": false,
            "calendar": false,
            "container_id": "tv_chart"
        }});
      </script>

    </div>
    """

    components.html(
        chart_html,
        height=570,
        scrolling=False
    )

    st.caption(
        "Selected Symbol: " + selected_symbol
    )

    if st.button("← BACK TO MARKET SELECTION"):

        st.session_state.page = "dashboard"
        st.rerun()

    render_footer()


# ============================================================
# SECTION 17: LOGOUT
# ============================================================

if (
    st.session_state.pin_verified
    and st.session_state.page in ["dashboard", "market_view"]
):

    st.divider()

    if st.button("🔒 LOGOUT FROM TERMINAL"):

        log_security_event(
            "LOGOUT",
            "User logged out."
        )

        st.session_state.current_user = None
        st.session_state.pin_verified = False
        st.session_state.page = "login"

        st.session_state.selected_market = "Indian Market"
        st.session_state.selected_symbols = {}

        st.rerun()


# ============================================================
# END OF KUSHAL PRO MAX TRADING
# ============================================================
