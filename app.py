import streamlit as st
import json
import os
import bcrypt
import secrets
import tempfile
from datetime import datetime, timedelta

st.set_page_config(
    page_title="KUSHAL PRO MAX TRADING",
    page_icon="⚡",
    layout="wide",  # Full screen / Wide layout for desktop
    initial_sidebar_state="collapsed"
)

DB_FILE = "admin_config.json"
BACKUP_FILE = "admin_config.json.bak"

# ==================== SECURITY & CRYPTOGRAPHIC UTILS ====================

def hash_secret(secret_text: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(secret_text.encode('utf-8'), salt).decode('utf-8')

def verify_secret(secret_text: str, hashed_text: str) -> bool:
    try:
        return bcrypt.checkpw(secret_text.encode('utf-8'), hashed_text.encode('utf-8'))
    except Exception:
        return False

def log_security_event(event_type: str, details: str):
    if "audit_logs" not in st.session_state:
        st.session_state.audit_logs = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{event_type.upper()}] {details}"
    st.session_state.audit_logs.append(log_entry)

def load_admin_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            log_security_event("ERROR", "Primary database corrupted.")
            if os.path.exists(BACKUP_FILE):
                try:
                    with open(BACKUP_FILE, "r") as bf:
                        return json.load(bf)
                except Exception:
                    pass
            return None
        except Exception:
            return None
    return None

def save_admin_data(data):
    try:
        if os.path.exists(DB_FILE):
            if os.path.exists(BACKUP_FILE):
                os.remove(BACKUP_FILE)
            os.rename(DB_FILE, BACKUP_FILE)
            
        dir_name = os.path.dirname(DB_FILE) or "."
        with tempfile.NamedTemporaryFile('w', dir=dir_name, delete=False) as tf:
            json.dump(data, tf)
            temp_name = tf.name
        os.replace(temp_name, DB_FILE)
        log_security_event("INFO", "Master credentials updated successfully.")
    except Exception as e:
        st.error(f"DATABASE WRITE FAILED: {e}")

# ==================== SESSION STATE INITIALIZATION ====================
if "page" not in st.session_state:
    st.session_state.page = "login"
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "pin_verified" not in st.session_state:
    st.session_state.pin_verified = False
if "failed_login_attempts" not in st.session_state:
    st.session_state.failed_login_attempts = 0
if "lockout_time" not in st.session_state:
    st.session_state.lockout_time = None
if "failed_pin_attempts" not in st.session_state:
    st.session_state.failed_pin_attempts = 0
if "pin_lockout_time" not in st.session_state:
    st.session_state.pin_lockout_time = None
if "otp_session" not in st.session_state:
    st.session_state.otp_session = {"hash": None, "expiry": None, "attempts": 0}
if "selected_market" not in st.session_state:
    st.session_state.selected_market = "Indian Market"
if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = []

admin_data = load_admin_data()

# ==================== STYLING (Black Background, Green Glow, White Text Inside Boxes) ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Segoe+UI:wght@400;600;700&display=swap');

.stApp {
    background: 
        radial-gradient(circle at 0% 0%, rgba(0, 200, 80, 0.1) 0%, transparent 40%),
        radial-gradient(circle at 100% 0%, rgba(0, 200, 80, 0.1) 0%, transparent 40%),
        #010302 !important;
    color: #FFFFFF !important;
    font-family: 'Segoe UI', Arial, sans-serif;
    background-attachment: fixed;
}
.block-container {
    max-width: 1200px !important;
    padding: 30px 40px 40px !important;
    margin: auto !important;
}
.main-header {
    background: #050B08;
    border: 2px solid #00C968;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 0 25px rgba(0, 232, 117, 0.2);
}
.welcome-tag {
    background: #092318;
    border: 1px solid #00E875;
    border-radius: 18px;
    padding: 4px 14px;
    color: #00E875;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    display: inline-block;
    margin-bottom: 8px;
}
.main-title {
    font-family: 'Orbitron', sans-serif !important;
    color: #00F080;
    font-size: 26px;
    font-weight: 800;
    letter-spacing: 2px;
    margin: 4px 0;
    text-shadow: 0 0 12px rgba(0, 240, 128, 0.5);
}
.sub-title {
    color: #00A94F;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1.5px;
    margin: 0;
}
.heading-box {
    background: #07160F;
    border: 1px solid #00A94F;
    border-radius: 8px;
    padding: 12px;
    text-align: center;
    margin-bottom: 16px;
    color: #00F080;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 1.5px;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #060F0A !important;
    border: 1px solid #174B30 !important;
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.6);
}
/* White text inside boxes for maximum readability */
p, span, label, div, .stMarkdown {
    color: #FFFFFF !important;
}
.stTextInput label {
    color: #00E875 !important;
    font-size: 14px !important;
    font-weight: 700 !important;
}
.stTextInput input {
    background: #020805 !important;
    color: #FFFFFF !important;
    border: 1px solid #00A94F !important;
    border-radius: 6px !important;
    min-height: 42px !important;
    padding: 8px 14px !important;
    font-size: 15px !important;
}
.stButton button {
    width: 100% !important;
    min-height: 44px !important;
    border-radius: 6px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    border: 1px solid #00A94F !important;
    background: #0D2B1D !important;
    color: #FFFFFF !important;
    margin-top: 6px;
    margin-bottom: 6px;
    transition: 0.2s ease;
}
.stButton button:hover {
    border-color: #00F080 !important;
    box-shadow: 0 0 10px rgba(0,240,128,0.4);
}
.stButton button[kind="primary"] {
    background: #00C968 !important;
    color: #020805 !important;
    border: 1px solid #00F080 !important;
}
.footer-box {
    background: #050B08;
    border: 1px solid #174B30;
    border-radius: 6px;
    padding: 10px;
    text-align: center;
    color: #00A94F;
    font-size: 12px;
    letter-spacing: 1px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <div class="welcome-tag">WELCOME TO</div>
    <div class="main-title">KUSHAL PRO MAX TRADING</div>
    <div class="sub-title">DESKTOP TRADING TERMINAL & ANALYTICS</div>
</div>
""", unsafe_allow_html=True)

# ==================== 1. INITIAL MASTER SETUP ====================
if admin_data is None:
    st.markdown('<div class="heading-box">INITIAL MASTER SETUP</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<p style='color:#00E875; font-weight:600;'>ESTABLISH SECURE MASTER CREDENTIALS.</p>", unsafe_allow_html=True)
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
                st.error("ERROR: TERMINAL PIN MUST BE EXACTLY 6 NUMERIC DIGITS")
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
                log_security_event("SETUP", "Master account established.")
                st.success("MASTER ACCOUNT CREATED & SECURED SUCCESSFULLY!")
                st.rerun()

# ==================== 2. SECURE MASTER LOGIN ====================
elif st.session_state.page == "login":
    st.markdown('<div class="heading-box">SECURE MASTER LOGIN</div>', unsafe_allow_html=True)
    
    if st.session_state.lockout_time and datetime.now() < st.session_state.lockout_time:
        remaining = int((st.session_state.lockout_time - datetime.now()).total_seconds())
        st.error(f"ACCOUNT TEMPORARILY LOCKED. TRY AGAIN IN {remaining} SECONDS.")
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
                    log_security_event("LOGIN_SUCCESS", f"User logged in: {user_id.strip()}")
                    st.session_state.page = "pin_verify"
                    st.rerun()
                else:
                    st.session_state.failed_login_attempts += 1
                    rem = 5 - st.session_state.failed_login_attempts
                    if st.session_state.failed_login_attempts >= 5:
                        st.session_state.lockout_time = datetime.now() + timedelta(minutes=5)
                        st.error("SECURITY ALERT: 5 FAILED LOGIN ATTEMPTS. LOCKED FOR 5 MINUTES.")
                    else:
                        st.error(f"ACCESS DENIED: INVALID CREDENTIALS. {rem} ATTEMPTS REMAINING.")

            if st.button("FORGOT PASSWORD / ID / PIN?"):
                st.session_state.page = "forgot_step1"
                st.rerun()

# ==================== 3. 6-DIGIT PIN VERIFICATION GATEWAY ====================
elif st.session_state.page == "pin_verify":
    st.markdown('<div class="heading-box">ENTER 6-DIGIT TERMINAL PIN</div>', unsafe_allow_html=True)
    
    if st.session_state.pin_lockout_time and datetime.now() < st.session_state.pin_lockout_time:
        rem_pin = int((st.session_state.pin_lockout_time - datetime.now()).total_seconds())
        st.error(f"PIN GATEWAY LOCKED. TRY AGAIN IN {rem_pin} SECONDS.")
    else:
        if st.session_state.pin_lockout_time and datetime.now() >= st.session_state.pin_lockout_time:
            st.session_state.pin_lockout_time = None
            st.session_state.failed_pin_attempts = 0

        with st.container(border=True):
            st.markdown("<p style='color:#FFFFFF;'>ENTER YOUR 6-DIGIT SECURITY PIN TO UNLOCK THE TERMINAL.</p>", unsafe_allow_html=True)
            pin_input = st.text_input("6-DIGIT PIN CODE", type="password", max_chars=6, placeholder="••••••")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("UNLOCK TERMINAL →", type="primary"):
                    if verify_secret(pin_input, admin_data["pin_hash"]):
                        st.session_state.failed_pin_attempts = 0
                        st.session_state.pin_verified = True
                        log_security_event("PIN_SUCCESS", "Terminal unlocked.")
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.session_state.failed_pin_attempts += 1
                        rem_p = 5 - st.session_state.failed_pin_attempts
                        if st.session_state.failed_pin_attempts >= 5:
                            st.session_state.pin_lockout_time = datetime.now() + timedelta(minutes=5)
                            st.error("SECURITY LOCKOUT: 5 INCORRECT PINS. LOCKED FOR 5 MINUTES.")
                        else:
                            st.error(f"INVALID 6-DIGIT PIN. {rem_p} ATTEMPTS REMAINING.")
            with col2:
                if st.button("FORGOT PIN?"):
                    st.session_state.page = "forgot_step1"
                    st.rerun()
                    
            if st.button("← LOCK / BACK TO LOGIN"):
                st.session_state.current_user = None
                st.session_state.pin_verified = False
                st.session_state.page = "login"
                st.rerun()

# ==================== 4. RECOVERY: SECURE OTP (STEP 1) ====================
elif st.session_state.page == "forgot_step1":
    st.markdown('<div class="heading-box">SECURITY RECOVERY (SECURE OTP)</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<p style='color:#FFFFFF;'>ENTER REGISTERED MOBILE NUMBER FOR SECURE OTP VERIFICATION.</p>", unsafe_allow_html=True)
        input_mobile = st.text_input("REGISTERED MOBILE NUMBER", max_chars=10, placeholder="10-DIGIT NUMBER")

        if st.button("SEND SECURE OTP"):
            if input_mobile.strip() == admin_data["mobile"]:
                raw_otp = "".join([str(secrets.randbelow(10)) for _ in range(6)])
                otp_hash_val = hash_secret(raw_otp)
                expiry_time = datetime.now() + timedelta(minutes=5)
                st.session_state.otp_session = {
                    "hash": otp_hash_val,
                    "expiry": expiry_time,
                    "attempts": 0
                }
                st.success(f"SECURE OTP GENERATED! [TEST OTP: {raw_otp}] (Valid for 5 mins)")
            else:
                st.error("ERROR: MOBILE NUMBER NOT FOUND IN MASTER RECORDS")

        if st.session_state.otp_session["hash"] is not None:
            otp_input = st.text_input("ENTER 6-DIGIT OTP", type="password", max_chars=6)
            if st.button("VERIFY OTP & PROCEED →", type="primary"):
                current_time = datetime.now()
                if current_time > st.session_state.otp_session["expiry"]:
                    st.error("OTP HAS EXPIRED. PLEASE REQUEST A NEW OTP.")
                elif st.session_state.otp_session["attempts"] >= 3:
                    st.error("MAXIMUM OTP ATTEMPTS EXCEEDED.")
                elif verify_secret(otp_input.strip(), st.session_state.otp_session["hash"]):
                    st.session_state.otp_session = {"hash": None, "expiry": None, "attempts": 0}
                    st.session_state.page = "forgot_step2"
                    st.rerun()
                else:
                    st.session_state.otp_session["attempts"] += 1
                    st.error(f"INVALID OTP. ATTEMPT {st.session_state.otp_session['attempts']}/3")

        if st.button("← RETURN TO LOGIN"):
            st.session_state.page = "login"
            st.rerun()

# ==================== 5. RECOVERY: CREDENTIAL RESET & KDS OVERRIDE (STEP 2) ====================
elif st.session_state.page == "forgot_step2":
    st.markdown('<div class="heading-box">CREDENTIAL RESET & KDS MASTER OVERRIDE</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<p style='color:#FFFFFF;'>OTP VERIFIED. SELECT RECOVERY ACTION OR EXECUTE KDS OVERRIDE.</p>", unsafe_allow_html=True)
        
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
                    st.success("PASSWORD UPDATED! PLEASE LOGIN.")
                    st.session_state.current_user = None
                    st.session_state.pin_verified = False
                    st.session_state.page = "login"
                    st.rerun()
                    
        elif reset_choice == "RESET 6-DIGIT PIN":
            new_pi = st.text_input("NEW 6-DIGIT PIN", type="password", max_chars=6)
            conf_pi = st.text_input("CONFIRM 6-DIGIT PIN", type="password", max_chars=6)
            if st.button("UPDATE PIN NOW", type="primary"):
                if not new_pi.isdigit() or len(new_pi) != 6:
                    st.error("PIN MUST BE EXACTLY 6 NUMERIC DIGITS")
                elif new_pi != conf_pi:
                    st.error("PINS DO NOT MATCH")
                else:
                    admin_data["pin_hash"] = hash_secret(new_pi)
                    save_admin_data(admin_data)
                    st.success("6-DIGIT PIN UPDATED! PLEASE LOGIN.")
                    st.session_state.current_user = None
                    st.session_state.pin_verified = False
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
                    if not all([new_uid, new_p, new_pi]) or len(new_p) < 8 or not new_pi.isdigit() or len(new_pi) != 6:
                        st.error("PLEASE PROVIDE VALID DETAILS")
                    else:
                        admin_data["user_id"] = new_uid.strip()
                        admin_data["password_hash"] = hash_secret(new_p)
                        admin_data["pin_hash"] = hash_secret(new_pi)
                        save_admin_data(admin_data)
