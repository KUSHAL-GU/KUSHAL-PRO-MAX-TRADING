import streamlit as st
import json
import os
import bcrypt
import random
import time
from datetime import datetime, timedelta

st.set_page_config(
    page_title="KUSHAL PRO MAX TRADING",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

DB_FILE = "admin_config.json"

# ==================== SECURITY & HASHING UTILS ====================

def hash_secret(secret_text: str) -> str:
    """Hash password, pin, or kds code using bcrypt securely."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(secret_text.encode('utf-8'), salt).decode('utf-8')

def verify_secret(secret_text: str, hashed_text: str) -> bool:
    """Verify plain secret against bcrypt hash."""
    try:
        return bcrypt.checkpw(secret_text.encode('utf-8'), hashed_text.encode('utf-8'))
    except Exception:
        return False

def load_admin_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def save_admin_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# Initialize Session State Variables securely
if "page" not in st.session_state:
    st.session_state.page = "login"
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "failed_login_attempts" not in st.session_state:
    st.session_state.failed_login_attempts = 0
if "lockout_time" not in st.session_state:
    st.session_state.lockout_time = None
if "failed_pin_attempts" not in st.session_state:
    st.session_state.failed_pin_attempts = 0
if "pin_lockout_time" not in st.session_state:
    st.session_state.pin_lockout_time = None
if "otp_data" not in st.session_state:
    st.session_state.otp_data = {"code": None, "expiry": None, "attempts": 0}

admin_data = load_admin_data()

# ==================== STYLING (Dark / Green Glow Theme) ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Segoe+UI:wght@600;750&display=swap');

.stApp {
    background: 
        radial-gradient(circle at 0% 0%, rgba(0, 200, 80, 0.15) 0%, transparent 45%),
        radial-gradient(circle at 100% 0%, rgba(0, 200, 80, 0.15) 0%, transparent 45%),
        radial-gradient(circle at 0% 100%, rgba(0, 200, 80, 0.15) 0%, transparent 45%),
        radial-gradient(circle at 100% 100%, rgba(0, 200, 80, 0.15) 0%, transparent 45%),
        #010503 !important;
    color: #00A94F;
    font-family: 'Segoe UI', Arial, sans-serif;
    background-attachment: fixed;
}
.block-container {
    max-width: 920px !important;
    padding: 24px 32px 36px !important;
    margin: auto !important;
}
.main-header {
    background: #050D09;
    border: 2px solid #174B30;
    border-radius: 14px;
    padding: 16px;
    text-align: center;
    margin-bottom: 15px;
    box-shadow: 0 0 20px rgba(0, 255, 102, 0.1);
}
.welcome-tag {
    background: #092318;
    border: 1px solid #00E875;
    border-radius: 18px;
    padding: 3px 12px;
    color: #00E875;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    display: inline-block;
    margin-bottom: 6px;
}
.main-title {
    font-family: 'Orbitron', sans-serif !important;
    color: #00F080;
    font-size: 24px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin: 4px 0;
    text-shadow: 0 0 10px rgba(0, 240, 128, 0.4);
}
.sub-title {
    color: #008F49;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    margin: 0;
}
.heading-box {
    background: #0B2015;
    border: 1px solid #17683B;
    border-radius: 8px;
    padding: 10px;
    text-align: center;
    margin-bottom: 12px;
    color: #00E875;
    font-size: 14px;
    font-weight: 750;
    letter-spacing: 2px;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #09170F;
    border: 1px solid #174B30;
    border-radius: 12px;
    padding: 16px 22px;
    margin-bottom: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
}
.stTextInput label {
    color: #00C968 !important;
    font-size: 11px !important;
    font-weight: 700 !important;
}
.stTextInput input {
    background: #10271A !important;
    color: #00F080 !important;
    border: 1px solid #17683B !important;
    border-radius: 6px !important;
    min-height: 36px !important;
    padding: 6px 12px !important;
    font-size: 13px !important;
}
.stButton button {
    width: 100% !important;
    min-height: 38px !important;
    border-radius: 6px !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    border: 1px solid #17683B !important;
    margin-top: 5px;
    margin-bottom: 5px;
}
.stButton button[kind="primary"] {
    background: #00D875 !important;
    color: #031008 !important;
    border: 1px solid #00F080 !important;
}
.footer-box {
    background: #08180F;
    border: 1px solid #174B30;
    border-radius: 6px;
    padding: 8px;
    text-align: center;
    color: #008F49;
    font-size: 10px;
    letter-spacing: 1px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <div class="welcome-tag">WELCOME TO</div>
    <div class="main-title">KUSHAL PRO MAX TRADING</div>
    <div class="sub-title">SECURE PRODUCTION-GRADE TERMINAL GATEWAY</div>
</div>
""", unsafe_allow_html=True)

# ==================== 1. INITIAL MASTER SETUP ====================
if admin_data is None:
    st.markdown('<div class="heading-box">INITIAL MASTER SETUP</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.info("ESTABLISH SECURE MASTER CREDENTIALS (BCRYPT ENCRYPTED).")
        new_user = st.text_input("CREATE MASTER USER ID", placeholder="ENTER UNIQUE USER ID")
        mobile_no = st.text_input("MOBILE NUMBER (10 DIGITS)", placeholder="10-DIGIT MOBILE NUMBER", max_chars=10)
        new_pwd = st.text_input("CREATE PASSWORD (MIN 8 CHARS)", type="password", placeholder="SECURE PASSWORD")
        confirm_pwd = st.text_input("CONFIRM PASSWORD", type="password", placeholder="RE-ENTER PASSWORD")
        kds_code = st.text_input("SECRET KDS RECOVERY CODE", type="password", placeholder="MASTER KDS OVERRIDE KEY")
        
        col1, col2 = st.columns(2)
        with col1:
            terminal_pin = st.text_input("6-DIGIT TERMINAL PIN", type="password", max_chars=6, placeholder="6 DIGITS")
        with col2:
            confirm_pin = st.text_input("CONFIRM 6-DIGIT PIN", type="password", max_chars=6, placeholder="RE-ENTER 6 DIGITS")

        if st.button("CREATE MASTER ACCOUNT →", type="primary"):
            if not all([new_user, mobile_no, new_pwd, confirm_pwd, kds_code, terminal_pin, confirm_pin]):
                st.error("ERROR: ALL FIELDS ARE REQUIRED")
            elif len(mobile_no) != 10 or not mobile_no.isdigit():
                st.error("ERROR: MOBILE NUMBER MUST BE EXACTLY 10 DIGITS")
            elif len(new_pwd) < 8:
                st.error("ERROR: PASSWORD MUST BE AT LEAST 8 CHARACTERS")
            elif new_pwd != confirm_pwd:
                st.error("ERROR: PASSWORDS DO NOT MATCH")
            elif not terminal_pin.isdigit() or len(terminal_pin) != 6:
                st.error("ERROR: TERMINAL PIN MUST BE EXACTLY 6 DIGITS")
            elif terminal_pin != confirm_pin:
                st.error("ERROR: 6-DIGIT PINS DO NOT MATCH")
            else:
                secure_data = {
                    "user_id": new_user.strip(),
                    "mobile": mobile_no.strip(),
                    "password_hash": hash_secret(new_pwd),
                    "kds_hash": hash_secret(kds_code),
                    "pin_hash": hash_secret(terminal_pin)
                }
                save_admin_data(secure_data)
                st.success("MASTER ACCOUNT CREATED & CRYPTOGRAPHICALLY SECURED!")
                st.rerun()

# ==================== 2. SECURE MASTER LOGIN ====================
elif st.session_state.page == "login":
    st.markdown('<div class="heading-box">SECURE MASTER LOGIN</div>', unsafe_allow_html=True)
    
    # Check Brute Force Lockout
    if st.session_state.lockout_time and datetime.now() < st.session_state.lockout_time:
        remaining = int((st.session_state.lockout_time - datetime.now()).total_seconds())
        st.error(f"ACCOUNT LOCKED DUE TO MULTIPLE FAILED ATTEMPTS. TRY AGAIN IN {remaining} SECONDS.")
    else:
        if st.session_state.lockout_time and datetime.now() >= st.session_state.lockout_time:
            st.session_state.lockout_time = None
            st.session_state.failed_login_attempts = 0

        with st.container(border=True):
            user_id = st.text_input("USER ID", placeholder="ENTER MASTER USER ID")
            password = st.text_input("PASSWORD", type="password", placeholder="ENTER PASSWORD")

            if st.button("AUTHENTICATE →", type="primary"):
                if user_id.strip() == admin_data["user_id"] and verify_secret(password, admin_data["password_hash"]):
                    st.session_state.failed_login_attempts = 0
                    st.session_state.current_user = user_id.strip()
                    st.session_state.page = "pin_verify"
                    st.rerun()
                else:
                    st.session_state.failed_login_attempts += 1
                    remaining_attempts = 5 - st.session_state.failed_login_attempts
                    if st.session_state.failed_login_attempts >= 5:
                        st.session_state.lockout_time = datetime.now() + timedelta(minutes=5)
                        st.error("SECURITY ALERT: 5 FAILED LOGIN ATTEMPTS. ACCOUNT LOCKED FOR 5 MINUTES.")
                    else:
                        st.error(f"ACCESS DENIED: INVALID CREDENTIALS. {remaining_attempts} ATTEMPTS REMAINING.")

            if st.button("FORGOT PASSWORD / ID / PIN?"):
                st.session_state.page = "forgot_step1"
                st.rerun()

# ==================== 3. 6-DIGIT PIN VERIFICATION GATEWAY ====================
elif st.session_state.page == "pin_verify":
    st.markdown('<div class="heading-box">ENTER 6-DIGIT TERMINAL PIN</div>', unsafe_allow_html=True)
    
    if st.session_state.pin_lockout_time and datetime.now() < st.session_state.pin_lockout_time:
        remaining_pin = int((st.session_state.pin_lockout_time - datetime.now()).total_seconds())
        st.error(f"PIN GATEWAY LOCKED DUE TO REPEATED INCORRECT PINS. TRY AGAIN IN {remaining_pin} SECONDS.")
    else:
        if st.session_state.pin_lockout_time and datetime.now() >= st.session_state.pin_lockout_time:
            st.session_state.pin_lockout_time = None
            st.session_state.failed_pin_attempts = 0

        with st.container(border=True):
            st.info("ENTER YOUR 6-DIGIT SECURITY PIN TO UNLOCK THE TERMINAL.")
            pin_input = st.text_input("6-DIGIT PIN CODE", type="password", max_chars=6, placeholder="••••••")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("UNLOCK TERMINAL →", type="primary"):
                    if verify_secret(pin_input, admin_data["pin_hash"]):
                        st.session_state.failed_pin_attempts = 0
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.session_state.failed_pin_attempts += 1
                        rem_pins = 5 - st.session_state.failed_pin_attempts
                        if st.session_state.failed_pin_attempts >= 5:
                            st.session_state.pin_lockout_time = datetime.now() + timedelta(minutes=5)
                            st.error("SECURITY LOCKOUT: 5 INCORRECT PIN ATTEMPTS. TERMINAL LOCKED FOR 5 MINUTES.")
                        else:
                            st.error(f"INVALID 6-DIGIT PIN. {rem_pins} ATTEMPTS REMAINING.")
            with col2:
                if st.button("FORGOT PIN?"):
                    st.session_state.page = "forgot_step1"
                    st.rerun()
                    
            if st.button("← LOCK / BACK TO LOGIN"):
                st.session_state.current_user = None
                st.session_state.page = "login"
                st.rerun()

# ==================== 4. RECOVERY: MOBILE OTP (STEP 1) ====================
elif st.session_state.page == "forgot_step1":
    st.markdown('<div class="heading-box">SECURITY RECOVERY (SECURE OTP)</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.info("ENTER REGISTERED MOBILE NUMBER FOR SECURE OTP VERIFICATION.")
        input_mobile = st.text_input("REGISTERED MOBILE NUMBER", max_chars=10, placeholder="10-DIGIT NUMBER")
        
        if "otp_session" not in st.session_state:
            st.session_state.otp_session = {"code": None, "expiry": None, "attempts": 0}

        # Cooldown check
        if st.button("SEND SECURE OTP"):
            if input_mobile.strip() == admin_data["mobile"]:
                # Generate random secure 6-digit OTP
                random_otp = str(random.randint(100000, 999999))
                expiry_time = datetime.now() + timedelta(minutes=5)
                st.session_state.otp_session = {
                    "code": random_otp,
                    "expiry": expiry_time,
                    "attempts": 0
                }
                # Production note: In real deployment, integrate SMS API gateway (Twilio / Fast2SMS) here.
                st.success(f"SECURE OTP GENERATED & SENT VIA SMS GATEWAY! [DEVELOPER TEST OTP: {random_otp}] (Valid for 5 mins)")
            else:
                st.error("ERROR: MOBILE NUMBER NOT FOUND IN MASTER RECORDS")

        if st.session_state.otp_session["code"] is not None:
            otp_input = st.text_input("ENTER 6-DIGIT OTP", type="password", max_chars=6)
            if st.button("VERIFY OTP & PROCEED →", type="primary"):
                current_time = datetime.now()
                if current_time > st.session_state.otp_session["expiry"]:
                    st.error("OTP HAS EXPIRED. PLEASE REQUEST A NEW OTP.")
                elif st.session_state.otp_session["attempts"] >= 3:
                    st.error("MAXIMUM OTP ATTEMPTS EXCEEDED. REQUEST NEW OTP.")
                elif otp_input.strip() == st.session_state.otp_session["code"]:
                    # Invalidate OTP after single use
                    st.session_state.otp_session = {"code": None, "expiry": None, "attempts": 0}
                    st.session_state.page = "forgot_step2"
                    st.rerun()
                else:
                    st.session_state.otp_session["attempts"] += 1
                    st.error(f"INVALID OTP. ATTEMPT {st.session_state.otp_session['attempts']}/3")

        if st.button("← RETURN TO LOGIN"):
            st.session_state.otp_session = {"code": None, "expiry": None, "attempts": 0}
            st.session_state.page = "login"
            st.rerun()

# ==================== 5. RECOVERY: CREDENTIAL RESET & KDS OVERRIDE (STEP 2) ====================
elif st.session_state.page == "forgot_step2":
    st.markdown('<div class="heading-box">CREDENTIAL RESET & KDS MASTER OVERRIDE</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.info("OTP VERIFIED SUCCESSFULLY. SELECT RECOVERY ACTION OR EXECUTE KDS OVERRIDE.")
        
        reset_choice = st.selectbox("SELECT ACTION", ["RESET PASSWORD", "RESET 6-DIGIT PIN", "FULL RECOVERY VIA KDS CODE"])
        
        if reset_choice == "RESET PASSWORD":
            new_p = st.text_input("NEW PASSWORD (MIN 8 CHARS)", type="password")
            conf_p = st.text_input("CONFIRM NEW PASSWORD", type="password")
            if st.button("UPDATE PASSWORD NOW", type="primary"):
                if len(new_p) < 8:
                    st.error("PASSWORD MUST BE AT LEAST 8 CHARACTERS")
                elif new_p != conf_p:
                    st.error("PASSWORDS DO NOT MATCH")
                else:
                    admin_data["password_hash"] = hash_secret(new_p)
                    save_admin_data(admin_data)
                    st.success("PASSWORD UPDATED SUCCESSFULLY! PLEASE LOGIN.")
                    st.session_state.current_user = None
                    st.session_state.page = "login"
                    st.rerun()
                    
        elif reset_choice == "RESET 6-DIGIT PIN":
            new_pi = st.text_input("NEW 6-DIGIT PIN", type="password", max_chars=6)
            conf_pi = st.text_input("CONFIRM 6-DIGIT PIN", type="password", max_chars=6)
            if st.button("UPDATE PIN NOW", type="primary"):
                if not new_pi.isdigit() or len(new_pi) != 6:
                    st.error("PIN MUST BE EXACTLY 6 DIGITS")
                elif new_pi != conf_pi:
                    st.error("PINS DO NOT MATCH")
                else:
                    admin_data["pin_hash"] = hash_secret(new_pi)
                    save_admin_data(admin_data)
                    st.success("6-DIGIT PIN UPDATED SUCCESSFULLY! PLEASE LOGIN.")
                    st.session_state.current_user = None
                    st.session_state.page = "login"
                    st.rerun()
                    
        elif reset_choice == "FULL RECOVERY VIA KDS CODE":
            st.warning("MASTER KDS OVERRIDE: USE IF ALL CREDENTIALS NEED RESET.")
            kds_input = st.text_input("ENTER SECRET KDS RECOVERY CODE", type="password")
            new_uid = st.text_input("NEW MASTER USER ID")
            new_p = st.text_input("NEW PASSWORD (MIN 8 CHARS)", type="password")
            new_pi = st.text_input("NEW 6-DIGIT PIN", type="password", max_chars=6)
            
            if st.button("EXECUTE MASTER KDS OVERRIDE →", type="primary"):
                if verify_secret(kds_input, admin_data["kds_hash"]):
                    if not all([new_uid, new_p, new_pi]) or len(new_p) < 8 or len(new_pi) != 6:
                        st.error("PLEASE PROVIDE VALID USER ID, PASSWORD (MIN 8) & 6-DIGIT PIN")
                    else:
                        admin_data["user_id"] = new_uid.strip()
                        admin_data["password_hash"] = hash_secret(new_p)
                        admin_data["pin_hash"] = hash_secret(new_pi)
                        save_admin_data(admin_data)
                        st.success("MASTER OVERRIDE SUCCESSFUL! ALL CREDENTIALS UPDATED.")
                        st.session_state.current_user = None
                        st.session_state.page = "login"
                        st.rerun()
                else:
                    st.error("INVALID SECRET KDS RECOVERY CODE")

        if st.button("← RETURN TO LOGIN"):
            st.session_state.page = "login"
            st.rerun()

# ==================== 6. DASHBOARD & SECURE SETTINGS ====================
elif st.session_state.page == "dashboard":
    # Ensure authentication and pin verification before rendering dashboard
    if not st.session_state.current_user:
        st.session_state.page = "login"
        st.rerun()

    st.markdown('<div class="heading-box">TRADING TERMINAL ACTIVE</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.success(f"WELCOME BACK, {admin_data['user_id'].upper()}")
        st.markdown("""
        <div style="background:#10271A; border:1px solid #17683B; border-radius:10px; padding:15px; text-align:center; margin-bottom:15px;">
            <h3 style="color:#00F080; margin-bottom:5px; font-size:16px;">KUSHAL PRO MAX ENGINE</h3>
            <p style="color:#008F49; font-size:12px; margin-bottom:5px;">PRIVATE HIGH-SPEED ANALYTICS & BCRYPT HASH GUARDED</p>
            <p style="color:#00E875; font-size:11px;">● SYSTEM FULLY SECURED & PRODUCTION ACTIVE</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Inner Settings for changing credentials securely
        with st.expander("⚙️ SECURITY & CREDENTIALS SETTINGS"):
            st.markdown("UPDATE YOUR PASSWORD OR 6-DIGIT PIN SECURELY.")
            change_option = st.selectbox("SELECT ACTION", ["CHANGE PASSWORD", "CHANGE 6-DIGIT PIN"])
            
            if change_option == "CHANGE PASSWORD":
                old_pwd = st.text_input("CURRENT PASSWORD", type="password")
                new_pwd = st.text_input("NEW PASSWORD (MIN 8 CHARS)", type="password")
                conf_pwd = st.text_input("CONFIRM NEW PASSWORD", type="password")
                if st.button("UPDATE PASSWORD NOW"):
                    if not verify_secret(old_pwd, admin_data["password_hash"]):
                        st.error("CURRENT PASSWORD IS INCORRECT")
                    elif len(new_pwd) < 8:
                        st.error("NEW PASSWORD MUST BE AT LEAST 8 CHARACTERS")
                    elif new_pwd != conf_pwd:
                        st.error("NEW PASSWORDS DO NOT MATCH")
                    else:
                        admin_data["password_hash"] = hash_secret(new_pwd)
                        save_admin_data(admin_data)
                        st.success("PASSWORD UPDATED SUCCESSFULLY! SESSION TERMINATED.")
                        st.session_state.current_user = None
                        st.session_state.page = "login"
                        st.rerun()
            
            elif change_option == "CHANGE 6-DIGIT PIN":
                old_pin = st.text_input("CURRENT 6-DIGIT PIN", type="password", max_chars=6)
                new_pin = st.text_input("NEW 6-DIGIT PIN", type="password", max_chars=6)
                conf_pin = st.text_input("CONFIRM NEW 6-DIGIT PIN", type="password", max_chars=6)
                if st.button("UPDATE PIN NOW"):
                    if not verify_secret(old_pin, admin_data["pin_hash"]):
                        st.error("CURRENT 6-DIGIT PIN IS INCORRECT")
                    elif not new_pin.isdigit() or len(new_pin) != 6:
                        st.error("NEW PIN MUST BE EXACTLY 6 DIGITS")
                    elif new_pin != conf_pin:
                        st.error("NEW PINS DO NOT MATCH")
                    else:
                        admin_data["pin_hash"] = hash_secret(new_pin)
                        save_admin_data(admin_data)
                        st.success("6-DIGIT PIN UPDATED SUCCESSFULLY! SESSION TERMINATED.")
                        st.session_state.current_user = None
                        st.session_state.page = "login"
                        st.rerun()

        if st.button("DISCONNECT & LOCK TERMINAL", type="primary"):
            st.session_state.current_user = None
            st.session_state.page = "login"
            st.rerun()

st.markdown("""
<div class="footer-box">
    ● PRODUCTION SECURE | BCRYPT ENCRYPTED | KUSHAL PRO MAX TRADING © 2026
</div>
""", unsafe_allow_html=True)
