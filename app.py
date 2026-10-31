import streamlit as st
import sqlite3
import hashlib
import secrets
import hmac
import re
from pathlib import Path

# =====================================================
# KUSHAL PRO MAX TRADING | VERSION 1.0
# =====================================================

st.set_page_config(
    page_title="KUSHAL PRO MAX TRADING",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

DB_PATH = Path(__file__).with_name("kushal_users.db")
DEMO_OTP = "1234"


# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect(DB_PATH)
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
    return conn


def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        310000
    ).hex()
    return hashed, salt


def verify_password(password, stored_hash, salt):
    new_hash, _ = hash_password(password, salt)
    return hmac.compare_digest(new_hash, stored_hash)


def get_user(user_id):
    with get_db() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id.strip().casefold(),)
        ).fetchone()


def create_user(user_id, password, mobile, recovery_code):
    uid = user_id.strip().casefold()
    pwd_hash, pwd_salt = hash_password(password)
    rec_hash, rec_salt = hash_password(recovery_code)

    with get_db() as conn:
        conn.execute("""
            INSERT INTO users
            (user_id, password_hash, salt, mobile,
             recovery_hash, recovery_salt)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            uid, pwd_hash, pwd_salt, mobile,
            rec_hash, rec_salt
        ))


# ---------------- SESSION ----------------

defaults = {
    "page": "login",
    "current_user": None,
    "otp_verified": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def go(page):
    st.session_state.page = page
    st.rerun()


# ---------------- PREMIUM THEME ----------------

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at top, #10291b 0%, #06110b 45%, #020704 100%);
    color: #eafff0;
    font-family: Arial, sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 680px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.main-title {
    text-align: center;
    font-size: clamp(25px, 6vw, 38px);
    font-weight: 900;
    letter-spacing: 2px;
    color: #36ff91;
    text-shadow: 0 0 18px #00ff6680;
}

.welcome {
    text-align: center;
    color: #a8ffc8;
    font-size: 13px;
    letter-spacing: 5px;
    margin-bottom: 12px;
}

.subtitle {
    text-align: center;
    color: #80b99a;
    font-size: 12px;
    letter-spacing: 2px;
    margin-top: 8px;
    margin-bottom: 30px;
}

.panel {
    background: linear-gradient(145deg, #10251a, #09140e);
    border: 1px solid #246b43;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 0 25px #00ff6610;
    margin-bottom: 18px;
}

.section-title {
    color: #39ff91;
    text-align: center;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 20px;
}

.stTextInput label,
.stSelectbox label {
    color: #b6e9c7 !important;
    font-weight: 600;
}

.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    background-color: #0c1d13 !important;
    color: #eafff0 !important;
    border: 1px solid #267b49 !important;
    border-radius: 9px !important;
}

.stTextInput input:focus {
    border-color: #36ff91 !important;
    box-shadow: 0 0 8px #00ff6650 !important;
}

.stButton > button {
    width: 100%;
    min-height: 44px;
    border-radius: 9px;
    border: 1px solid #36ff91;
    background: linear-gradient(90deg, #12c866, #36ff91);
    color: #031008;
    font-weight: 900;
    letter-spacing: 1px;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #a0ffc5;
    color: #031008;
    box-shadow: 0 0 18px #36ff9170;
    border-color: #a0ffc5;
}

hr {
    border-color: #245b3b;
}

.footer {
    text-align: center;
    color: #65977a;
    font-size: 11px;
    letter-spacing: 1px;
    padding-top: 20px;
}

.status {
    text-align: center;
    color: #36ff91;
    font-size: 12px;
    letter-spacing: 1px;
    margin-top: 12px;
}

div[data-testid="stAlert"] {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- BRAND HEADER ----------------

def header():
    st.markdown(
        "<div class='welcome'>WELCOME TO</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='main-title'>KUSHAL PRO MAX<br>TRADING</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='subtitle'>ADVANCED FINANCIAL ANALYTICS</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='status'>● SYSTEM ONLINE &nbsp; | &nbsp; SECURE ACCESS</div>",
        unsafe_allow_html=True
    )
    st.markdown("---")


def footer():
    st.markdown(
        "<div class='footer'>"
        "KUSHAL PRO MAX © 2026<br>"
        "PREMIUM TRADING TERMINAL"
        "</div>",
        unsafe_allow_html=True
    )


header()


# =====================================================
# LOGIN SCREEN
# =====================================================

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

        if st.button("SECURE LOGIN →"):
            user = get_user(user_id)

            if user and verify_password(password, user[1], user[2]):
                st.session_state.current_user = user[0]
                st.session_state.otp_verified = False
                go("otp")
            else:
                st.error("ACCESS DENIED: INVALID USER ID OR PASSWORD")

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("CREATE ACCOUNT"):
                go("register")

        with col2:
            if st.button("FORGOT PASSWORD?"):
                go("forgot")


# =====================================================
# REGISTRATION SCREEN
# =====================================================

elif st.session_state.page == "register":

    st.markdown(
        "<div class='section-title'>CREATE ACCOUNT</div>",
        unsafe_allow_html=True
    )

    with st.container(border=True):

        new_id = st.text_input(
            "CREATE USER ID",
            placeholder="Choose a unique User ID"
        )

        new_password = st.text_input(
            "CREATE PASSWORD",
            type="password",
            placeholder="Minimum 8 characters"
        )

        confirm_password = st.text_input(
            "CONFIRM PASSWORD",
            type="password"
        )

        mobile = st.text_input(
            "MOBILE NUMBER",
            placeholder="10-digit mobile number"
        )

        recovery_code = st.text_input(
            "CREATE RECOVERY CODE",
            type="password",
            placeholder="Keep this code safe"
        )

        st.caption(
            "Recovery Code is required to reset your password "
            "or recover your User ID."
        )

        if st.button("REGISTER ACCOUNT →"):

            if not all([
                new_id.strip(),
                new_password,
                confirm_password,
                mobile,
                recovery_code
            ]):
                st.error("PLEASE FILL ALL FIELDS")

            elif not re.fullmatch(r"[A-Za-z0-9_.-]{4,30}", new_id.strip()):
                st.error("USER ID: USE 4-30 LETTERS, NUMBERS OR _ . -")

            elif len(new_password) < 8:
                st.error("PASSWORD MUST BE AT LEAST 8 CHARACTERS")

            elif new_password != confirm_password:
                st.error("PASSWORDS DO NOT MATCH")

            elif not re.fullmatch(r"[0-9]{10}", mobile.strip()):
                st.error("ENTER A VALID 10-DIGIT MOBILE NUMBER")

            elif len(recovery_code) < 6:
                st.error("RECOVERY CODE MUST BE AT LEAST 6 CHARACTERS")

            elif get_user(new_id):
                st.error("USER ID ALREADY EXISTS")

            else:
                try:
                    create_user(
                        new_id,
                        new_password,
                        mobile.strip(),
                        recovery_code
                    )
                    st.success("ACCOUNT CREATED SUCCESSFULLY!")
                    go("login")

                except sqlite3.IntegrityError:
                    st.error("USER ID ALREADY EXISTS")

        if st.button("← BACK TO LOGIN"):
            go("login")


# =====================================================
# OTP VERIFICATION
# =====================================================

elif st.session_state.page == "otp":

    user = get_user(st.session_state.current_user)

    if not user:
        st.session_state.current_user = None
        go("login")

    st.markdown(
        "<div class='section-title'>TWO-FACTOR AUTHENTICATION</div>",
        unsafe_allow_html=True
    )

    st.info(
        f"DEMO OTP SENT TO MOBILE ENDING IN "
        f"******{user[3][-4:]}. "
        f"DEMO CODE: {DEMO_OTP}"
    )

    otp = st.text_input(
        "ENTER 4-DIGIT OTP",
        type="password",
        max_chars=4
    )

    if st.button("VERIFY & LAUNCH TERMINAL →"):

        if otp == DEMO_OTP:
            st.session_state.otp_verified = True
            go("dashboard")
        else:
            st.error("INVALID OTP. PLEASE TRY AGAIN.")

    if st.button("CANCEL LOGIN"):
        st.session_state.current_user = None
        st.session_state.otp_verified = False
        go("login")


# =====================================================
# FORGOT PASSWORD / RECOVERY
# =====================================================

elif st.session_state.page == "forgot":

    st.markdown(
        "<div class='section-title'>ACCOUNT RECOVERY</div>",
        unsafe_allow_html=True
    )

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

        if st.button("RESET PASSWORD →"):

            user = get_user(uid)

            if not user or not verify_password(
                recovery, user[4], user[5]
            ):
                st.error("INVALID USER ID OR RECOVERY CODE")

            elif len(new_pwd) < 8:
                st.error("PASSWORD MUST BE AT LEAST 8 CHARACTERS")

            elif new_pwd != confirm_pwd:
                st.error("PASSWORDS DO NOT MATCH")

            else:
                new_hash, new_salt = hash_password(new_pwd)

                with get_db() as conn:
                    conn.execute("""
                        UPDATE users
                        SET password_hash = ?, salt = ?
                        WHERE user_id = ?
                    """, (new_hash, new_salt, user[0]))

                st.success("PASSWORD RESET SUCCESSFULLY!")
                st.session_state.page = "login"
                st.rerun()

    elif option == "RETRIEVE USER ID":

        mobile_input = st.text_input("ENTER REGISTERED MOBILE NUMBER")
        recovery = st.text_input(
            "ENTER RECOVERY CODE",
            type="password"
        )

        if st.button("RETRIEVE USER ID →"):

            found = None

            with get_db() as conn:
                users = conn.execute(
                    "SELECT * FROM users WHERE mobile = ?",
                    (mobile_input.strip(),)
                ).fetchall()

            for user in users:
                if verify_password(recovery, user[4], user[5]):
                    found = user[0]
                    break

            if found:
                st.success(f"YOUR USER ID: {found}")
            else:
                st.error("NO MATCHING ACCOUNT FOUND")

    elif option == "RETRIEVE MOBILE NUMBER":

        uid = st.text_input("ENTER USER ID")
        pwd = st.text_input("ENTER PASSWORD", type="password")

        if st.button("RETRIEVE MOBILE →"):

            user = get_user(uid)

            if user and verify_password(pwd, user[1], user[2]):
                st.success(
                    f"REGISTERED MOBILE: ******{user[3][-4:]}"
                )
            else:
                st.error("INVALID USER ID OR PASSWORD")

    st.markdown("---")

    if st.button("← RETURN TO LOGIN"):
        go("login")


# =====================================================
# MAIN DASHBOARD
# =====================================================

elif st.session_state.page == "dashboard":

    if (
        not st.session_state.current_user
        or not st.session_state.otp_verified
        or not get_user(st.session_state.current_user)
    ):
        st.session_state.current_user = None
        st.session_state.otp_verified = False
        go("login")

    st.success(
        f"TERMINAL ACTIVE | WELCOME "
        f"{st.session_state.current_user.upper()}"
    )

    st.markdown(
        "<div class='section-title'>TRADING DASHBOARD</div>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class='panel'>
        <h3 style='color:#36ff91;text-align:center;'>
            KUSHAL PRO MAX ENGINE
        </h3>
        <p style='color:#a8ffc8;text-align:center;'>
            ADVANCED FINANCIAL ANALYTICS
        </p>
        <p style='color:#36ff91;text-align:center;'>
            ● AUTHENTICATED SESSION ACTIVE
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.info("TRADING DASHBOARD MODULES WILL BE ADDED IN THE NEXT VERSION.")

    if st.button("DISCONNECT / LOGOUT"):
        st.session_state.current_user = None
        st.session_state.otp_verified = False
        go("login")


# ---------------- FOOTER ----------------

footer()
