import streamlit as st
import sqlite3
import hashlib
import secrets
import hmac
import re
from pathlib import Path
from contextlib import closing

# ==================================================
# KUSHAL PRO MAX TRADING
# PREMIUM LOGIN SYSTEM - VERSION 2.0
# ==================================================

st.set_page_config(
    page_title="KUSHAL PRO MAX TRADING",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

DB_PATH = Path(__file__).with_name("kushal_users.db")
DEMO_OTP = "1234"


# ==================================================
# DATABASE
# ==================================================

def database():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            yield conn


def initialize_database():
    with database() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                mobile TEXT NOT NULL,
                recovery_hash TEXT NOT NULL,
                recovery_salt TEXT NOT NULL
            )
        """)


def hash_value(value, salt=None):
    salt = salt or secrets.token_hex(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        value.encode("utf-8"),
        salt.encode("utf-8"),
        310000
    ).hex()

    return hashed, salt


def verify_value(value, stored_hash, salt):
    new_hash, _ = hash_value(value, salt)
    return hmac.compare_digest(new_hash, stored_hash)


def get_user(user_id):
    uid = user_id.strip().casefold()

    with database() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (uid,)
        ).fetchone()


def create_user(uid, password, mobile, recovery):
    password_hash, password_salt = hash_value(password)
    recovery_hash, recovery_salt = hash_value(recovery)

    with database() as conn:
        conn.execute("""
            INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)
        """, (
            uid.strip().casefold(),
            password_hash,
            password_salt,
            mobile,
            recovery_hash,
            recovery_salt
        ))


initialize_database()


# ==================================================
# SESSION
# ==================================================

defaults = {
    "page": "login",
    "current_user": None,
    "otp_verified": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def navigate(page):
    st.session_state.page = page
    st.rerun()


# ==================================================
# PREMIUM BLACK & NEON GREEN THEME
# ==================================================

st.markdown("""
<style>

.stApp {
    background: #020805 !important;
    color: #D5EBDD !important;
    font-family: "Segoe UI", Arial, sans-serif !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

.block-container {
    max-width: 940px !important;
    padding: 48px 28px 28px !important;
    margin: 20px auto !important;
    background: #050D09 !important;
    border: 2px solid #19452F !important;
    border-radius: 32px !important;
    box-shadow: 0 0 35px #00FF6610 !important;
}

/* WELCOME */

.welcome {
    display: table;
    margin: 0 auto 22px auto;
    padding: 8px 20px;
    border-radius: 30px;
    background: #08291A;
    color: #42F995;
    font-size: 23px;
    letter-spacing: 1px;
}

/* BRAND NAME */

.main-title {
    text-align: center;
    color: #38F58B;
    font-size: clamp(34px, 6vw, 58px);
    font-weight: 750;
    line-height: 1.35;
    letter-spacing: -1.5px;
    text-shadow: 0 0 15px #16E87535;
}

.subtitle {
    text-align: center;
    color: #9ABBA7;
    font-size: 21px;
    margin: 18px 0 30px;
    letter-spacing: .3px;
}

.section-title {
    color: #40F795;
    text-align: center;
    font-size: 36px;
    font-weight: 650;
    margin: 0 0 28px;
}

/* LOGIN PANEL */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #0B1A12 !important;
    border: 2px solid #24563B !important;
    border-radius: 26px !important;
    padding: 18px !important;
    box-shadow: 0 0 20px #00FF6608 !important;
}

/* INPUT */

.stTextInput label,
.stSelectbox label {
    color: #B3CFBD !important;
    font-size: 19px !important;
    font-weight: 500 !important;
}

.stTextInput input {
    min-height: 60px !important;
    background: #14271C !important;
    color: #E4FFF0 !important;
    border: 1px solid transparent !important;
    border-radius: 16px !important;
    font-size: 19px !important;
    padding: 12px 18px !important;
}

.stTextInput input:focus {
    border: 1px solid #39EF8A !important;
    box-shadow: 0 0 12px #00FF6630 !important;
}

/* BUTTONS */

.stButton > button {
    width: 100% !important;
    min-height: 62px !important;
    border-radius: 15px !important;
    font-size: 19px !important;
    font-weight: 700 !important;
    transition: all .25s ease !important;
}

/* PRIMARY */

.stButton > button[kind="primary"] {
    background: #16D875 !important;
    color: #031108 !important;
    border: none !important;
    box-shadow: 0 0 15px #16D87520 !important;
}

.stButton > button[kind="primary"]:hover {
    background: #40F995 !important;
    box-shadow: 0 0 24px #16D87565 !important;
}

/* SECONDARY */

.stButton > button[kind="secondary"] {
    background: #14271C !important;
    color: #40F795 !important;
    border: 1px solid transparent !important;
}

.stButton > button[kind="secondary"]:hover {
    background: #1B3828 !important;
    border: 1px solid #35E987 !important;
}

hr {
    border-color: #24563B !important;
    margin: 25px 0 !important;
}

.footer {
    text-align: center;
    color: #71947E;
    font-size: 16px;
    line-height: 2;
    margin-top: 25px;
    letter-spacing: .5px;
}

[data-testid="stAlert"] {
    border-radius: 14px !important;
}

/* MOBILE */

@media (max-width: 600px) {

    .block-container {
        padding: 28px 15px 22px !important;
        margin: 10px auto !important;
        border-radius: 24px !important;
    }

    .main-title {
        font-size: 34px !important;
    }

    .subtitle {
        font-size: 15px !important;
    }

    .section-title {
        font-size: 28px !important;
    }

    .welcome {
        font-size: 17px !important;
    }

    .stTextInput input {
        min-height: 55px !important;
        font-size: 17px !important;
    }

    .stTextInput label {
        font-size: 17px !important;
    }

    .stButton > button {
        min-height: 55px !important;
        font-size: 16px !important;
    }
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# HEADER
# ==================================================

def show_header():

    st.markdown(
        "<div class='welcome'>WELCOME TO</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='main-title'>"
        "KUSHAL PRO MAX<br>TRADING"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>"
        "ADVANCED FINANCIAL ANALYTICS"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<hr style='width:55%;border:1px solid #38F58B;margin:auto;'>",
        unsafe_allow_html=True
    )


def show_footer():

    st.markdown("""
    <div style="
        display:flex;
        justify-content:space-between;
        color:#80B99A;
        font-size:14px;
        margin-top:25px;
        gap:10px;
        flex-wrap:wrap;
    ">
        <span>● SYSTEM ONLINE</span>
        <span>ENCRYPTED ACCESS</span>
    </div>

    <div class="footer">
        KUSHAL PRO MAX © 2026
    </div>
    """, unsafe_allow_html=True)


show_header()


# ==================================================
# LOGIN PAGE
# ==================================================

if st.session_state.page == "login":

    st.markdown(
        "<div class='section-title'>SECURE LOGIN</div>",
        unsafe_allow_html=True
    )

    with st.container(border=True):

        user_id = st.text_input(
            "USER ID",
            placeholder="Enter your User ID",
            key="login_user"
        )

        password = st.text_input(
            "PASSWORD",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        col1, col2 = st.columns([1, 1])

        with col2:
            if st.button("Forgot Password?"):
                navigate("forgot")

        if st.button("SECURE LOGIN →", type="primary"):

            user = get_user(user_id)

            if user and verify_value(password, user[1], user[2]):

                st.session_state.current_user = user[0]
                st.session_state.otp_verified = False
                navigate("otp")

            else:
                st.error("INVALID USER ID OR PASSWORD")

        if st.button("+ CREATE ACCOUNT"):

            navigate("register")

        st.markdown(
            "<p style='text-align:center;color:#8FAF9B;'>"
            "NEW USER? REGISTER YOUR ACCOUNT"
            "</p>",
            unsafe_allow_html=True
        )


# ==================================================
# REGISTRATION
# ==================================================

elif st.session_state.page == "register":

    st.markdown(
        "<div class='section-title'>CREATE ACCOUNT</div>",
        unsafe_allow_html=True
    )

    with st.container(border=True):

        uid = st.text_input("CREATE USER ID")

        pwd = st.text_input(
            "CREATE PASSWORD",
            type="password"
        )

        confirm = st.text_input(
            "CONFIRM PASSWORD",
            type="password"
        )

        mobile = st.text_input(
            "MOBILE NUMBER",
            max_chars=10
        )

        recovery = st.text_input(
            "CREATE RECOVERY CODE",
            type="password"
        )

        st.caption(
            "Keep your recovery code safe. "
            "It will be needed for account recovery."
        )

        if st.button("REGISTER ACCOUNT →", type="primary"):

            if not all([uid.strip(), pwd, confirm, mobile, recovery]):
                st.error("PLEASE FILL ALL REQUIRED FIELDS")

            elif not re.fullmatch(r"[A-Za-z0-9_.-]{4,30}", uid.strip()):
                st.error("USER ID MUST BE 4-30 CHARACTERS")

            elif len(pwd) < 8:
                st.error("PASSWORD MUST HAVE AT LEAST 8 CHARACTERS")

            elif pwd != confirm:
                st.error("PASSWORDS DO NOT MATCH")

            elif not re.fullmatch(r"[0-9]{10}", mobile.strip()):
                st.error("ENTER VALID 10-DIGIT MOBILE NUMBER")

            elif len(recovery) < 6:
                st.error("RECOVERY CODE MUST HAVE AT LEAST 6 CHARACTERS")

            elif get_user(uid):
                st.error("USER ID ALREADY EXISTS")

            else:
                try:
                    create_user(uid, pwd, mobile.strip(), recovery)
                    st.success("ACCOUNT CREATED SUCCESSFULLY!")
                    navigate("login")

                except sqlite3.IntegrityError:
                    st.error("USER ID ALREADY EXISTS")

        if st.button("← BACK TO LOGIN"):
            navigate("login")


# ==================================================
# OTP PAGE
# ==================================================

elif st.session_state.page == "otp":

    user = get_user(st.session_state.current_user or "")

    if not user:
        st.session_state.current_user = None
        navigate("login")

    st.markdown(
        "<div class='section-title'>SECURITY VERIFICATION</div>",
        unsafe_allow_html=True
    )

    st.info(
        f"DEMO OTP: {DEMO_OTP} | MOBILE ENDING: {user[3][-4:]}"
    )

    otp = st.text_input(
        "ENTER 4-DIGIT OTP",
        type="password",
        max_chars=4
    )

    if st.button("VERIFY & LAUNCH TERMINAL →", type="primary"):

        if hmac.compare_digest(otp, DEMO_OTP):
            st.session_state.otp_verified = True
            navigate("dashboard")
        else:
            st.error("INVALID OTP")

    if st.button("CANCEL LOGIN"):
        st.session_state.current_user = None
        st.session_state.otp_verified = False
        navigate("login")


# ==================================================
# FORGOT PASSWORD & RECOVERY
# ==================================================

elif st.session_state.page == "forgot":

    st.markdown(
        "<div class='section-title'>ACCOUNT RECOVERY</div>",
        unsafe_allow_html=True
    )

    with st.container(border=True):

        option = st.selectbox(
            "SELECT RECOVERY OPTION",
            [
                "RESET PASSWORD",
                "RETRIEVE USER ID",
                "RETRIEVE MOBILE NUMBER"
            ]
        )

        st.markdown("---")

        if option == "RESET PASSWORD":

            uid = st.text_input("ENTER USER ID")

            recovery = st.text_input(
                "ENTER RECOVERY CODE",
                type="password"
            )

            new_pwd = st.text_input(
                "NEW PASSWORD",
                type="password"
            )

            confirm_pwd = st.text_input(
                "CONFIRM NEW PASSWORD",
                type="password"
            )

            if st.button("RESET PASSWORD →", type="primary"):

                user = get_user(uid)

                if not user or not verify_value(recovery, user[4], user[5]):
                    st.error("INVALID USER ID OR RECOVERY CODE")

                elif len(new_pwd) < 8:
                    st.error("PASSWORD MUST HAVE 8 CHARACTERS")

                elif new_pwd != confirm_pwd:
                    st.error("PASSWORDS DO NOT MATCH")

                else:
                    new_hash, new_salt = hash_value(new_pwd)

                    with database() as conn:
                        conn.execute("""
                            UPDATE users
                            SET password_hash = ?, salt = ?
                            WHERE user_id = ?
                        """, (new_hash, new_salt, user[0]))

                    st.success("PASSWORD UPDATED SUCCESSFULLY!")
                    navigate("login")

        elif option == "RETRIEVE USER ID":

            mobile_input = st.text_input("REGISTERED MOBILE NUMBER")

            recovery = st.text_input(
                "RECOVERY CODE",
                type="password"
            )

            if st.button("RETRIEVE USER ID →", type="primary"):

                with database() as conn:
                    users = conn.execute(
                        "SELECT * FROM users WHERE mobile = ?",
                        (mobile_input.strip(),)
                    ).fetchall()

                found = None

                for user in users:
                    if verify_value(recovery, user[4], user[5]):
                        found = user[0]
                        break

                if found:
                    st.success(f"YOUR USER ID: {found}")
                else:
                    st.error("ACCOUNT NOT FOUND")

        elif option == "RETRIEVE MOBILE NUMBER":

            uid = st.text_input("ENTER USER ID")

            pwd = st.text_input(
                "ENTER PASSWORD",
                type="password"
            )

            if st.button("RETRIEVE MOBILE →", type="primary"):

                user = get_user(uid)

                if user and verify_value(pwd, user[1], user[2]):
                    st.success(
                        f"REGISTERED MOBILE: ******{user[3][-4:]}"
                    )
                else:
                    st.error("INVALID USER ID OR PASSWORD")

        if st.button("← RETURN TO LOGIN"):
            navigate("login")


# ==================================================
# DASHBOARD
# ==================================================

elif st.session_state.page == "dashboard":

    if (
        not st.session_state.current_user
        or not st.session_state.otp_verified
        or not get_user(st.session_state.current_user)
    ):
        st.session_state.current_user = None
        st.session_state.otp_verified = False
        navigate("login")

    st.success(
        f"TERMINAL ACTIVE: "
        f"{st.session_state.current_user.upper()}"
    )

    st.markdown(
        "<div class='section-title'>"
        "TRADING DASHBOARD"
        "</div>",
        unsafe_allow_html=True
    )

    with st.container(border=True):

        st.markdown("""
        <h2 style="text-align:center;color:#40F795;">
            KUSHAL PRO MAX ENGINE
        </h2>
        <p style="text-align:center;color:#9ABBA7;">
            ADVANCED FINANCIAL ANALYTICS
        </p>
        <p style="text-align:center;color:#40F795;">
            ● AUTHENTICATED SESSION ACTIVE
        </p>
        """, unsafe_allow_html=True)

        st.info(
            "TRADING DASHBOARD MODULES WILL BE ADDED IN THE NEXT VERSION."
        )

        if st.button("DISCONNECT / LOGOUT", type="primary"):

            st.session_state.current_user = None
            st.session_state.otp_verified = False
            navigate("login")


# ==================================================
# FOOTER
# ==================================================

show_footer()
