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
    layout="wide",
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

# ==================== STYLING (Green & Black Theme - Original Title Restored) ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Segoe+UI:wght@400;600;700&display=swap');

.stApp {
    background: 
        radial-gradient(circle at 0% 0%, rgba(0, 200, 80, 0.12) 0%, transparent 40%),
        radial-gradient(circle at 100% 0%, rgba(0, 200, 80, 0.12) 0%, transparent 40%),
        #010503 !important;
    color: #00A94F !important;
    font-family: 'Segoe UI', Arial, sans-serif;
    background-attachment: fixed;
}
.block-container {
    max-width: 1200px !important;
    padding: 30px 40px 40px !important;
    margin: auto !important;
}
.main-header {
    background: #050D09;
    border: 2px solid #174B30;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 0 20px rgba(0, 255, 102, 0.15);
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
    color: #00F080 !important;
    font-size: 26px !important;
    font-weight: 800 !important;
    letter-spacing: 2px !important;
    margin: 4px 0 !important;
    text-shadow: 0 0 12px rgba(0, 240, 128, 0.5) !important;
}
.sub-title {
    color: #008F49 !important;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1.5px;
    margin: 0;
}
.heading-box {
    background: #0B2015;
    border: 1px solid #17683B;
    border-radius: 8px;
    padding: 12px;
    text-align: center;
    margin-bottom: 16px;
    color: #00E875;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 1.5px;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #09170F !important;
    border: 1px solid #174B30 !important;
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
}
.stTextInput label {
    color: #00C968 !important;
    font-size: 14px !important;
    font-weight: 700 !important;
}
.stTextInput input {
    background: #10271A !important;
    color: #00F080 !important;
    border: 1px solid #17683B !important;
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
    border: 1px solid #17683B !important;
    background: #0D2B1D !important;
    color: #00E875 !important;
    margin-top: 6px;
    margin-bottom: 6px;
}
.stButton button:hover {
    border-color: #00F080 !important;
    box-shadow: 0 0 10px rgba(0,240,128,0.4);
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
    padding: 10px;
    text-align: center;
    color: #008F49;
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
    <div class="sub-title">AUDITED PRODUCTION-GRADE SECURE TERMINAL</div>
</div>
""", unsafe_allow_html=True)

# ==================== 1. INITIAL MASTER SETUP ====================
if admin_data is None:
    st.markdown('<div class="heading-box">INITIAL MASTER SETUP</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.info("ESTABLISH SECURE MASTER CREDENTIALS.")
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
            st.info("ENTER YOUR 6-DIGIT SECURITY PIN TO UNLOCK THE TERMINAL.")
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
        st.info("ENTER REGISTERED MOBILE NUMBER FOR SECURE OTP VERIFICATION.")
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
        st.info("OTP VERIFIED. SELECT RECOVERY ACTION OR EXECUTE KDS OVERRIDE.")
        
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
                        st.success("MASTER OVERRIDE SUCCESSFUL!")
                        st.session_state.current_user = None
                        st.session_state.pin_verified = False
                        st.session_state.page = "login"
                        st.rerun()
                else:
                    st.error("INVALID SECRET KDS RECOVERY CODE")

        if st.button("← RETURN TO LOGIN"):
            st.session_state.page = "login"
            st.rerun()

# ==================== 6. DASHBOARD WITH MARKET SELECTOR BOX ====================
elif st.session_state.page == "dashboard":
    if not st.session_state.current_user or not st.session_state.pin_verified:
        st.error("UNAUTHORIZED ACCESS DETECTED.")
        st.session_state.current_user = None
        st.session_state.pin_verified = False
        st.session_state.page = "login"
        st.rerun()

    st.markdown('<div class="heading-box">TRADING TERMINAL ACTIVE</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f"<h3 style='color:#00F080; margin-top:0;'>WELCOME BACK, {admin_data['user_id'].upper()}</h3>", unsafe_allow_html=True)
        
        # MARKET SELECTOR BOX (Indian Market, Crypto Market, US Market)
        st.markdown("<p style='color:#00E875; font-weight:700; margin-bottom:10px;'>SELECT TRADING MARKET:</p>", unsafe_allow_html=True)
        
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            if st.button("🇮🇳 INDIAN MARKET", type="primary" if st.session_state.selected_market == "Indian Market" else "secondary"):
                st.session_state.selected_market = "Indian Market"
                st.rerun()
        with m_col2:
            if st.button("🪙 CRYPTO MARKET", type="primary" if st.session_state.selected_market == "Crypto Market" else "secondary"):
                st.session_state.selected_market = "Crypto Market"
                st.rerun()
        with m_col3:
            if st.button("🇺🇸 US MARKET", type="primary" if st.session_state.selected_market == "US Market" else "secondary"):
                st.session_state.selected_market = "US Market"
                st.rerun()

        st.markdown(f"""
        <div style="background:#10271A; border:1px solid #17683B; border-radius:10px; padding:20px; text-align:center; margin-top:15px; margin-bottom:15px;">
            <h4 style="color:#00F080; margin-top:0;">ACTIVE DASHBOARD: {st.session_state.selected_market.upper()}</h4>
            <p style="color:#008F49; font-size:14px; margin-bottom:5px;">REAL-TIME DATA STREAM & ANALYTICS READY</p>
            <p style="color:#00E875; font-size:12px;">● KUSHAL PRO MAX ENGINE SECURED</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Security & Credentials Settings Expander
        with st.expander("⚙️ SECURITY & CREDENTIALS SETTINGS"):
            st.info("UPDATE YOUR PASSWORD OR 6-DIGIT PIN SECURELY.")
            change_option = st.selectbox("SELECT ACTION", ["CHANGE PASSWORD", "CHANGE 6-DIGIT PIN", "VIEW SECURITY AUDIT LOGS"])
            
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
                        st.success("PASSWORD UPDATED! SESSION TERMINATED.")
                        st.session_state.current_user = None
                        st.session_state.pin_verified = False
                        st.session_state.page = "login"
                        st.rerun()
            
            elif change_option == "CHANGE 6-DIGIT PIN":
                old_pin = st.text_input("CURRENT 6-DIGIT PIN", type="password", max_chars=6)
                new_pin = st.text_input("NEW 6-DIGIT PIN", type="password", max_chars=6)
                conf_pin = st.text_input("CONFIRM NEW 6-DIGIT PIN", type="password", max_chars=6)
                if st.button("UPDATE PIN NOW"):
                    if not verify_secret(old_pin, admin_data["pin_hash"]):
                        st.error("CURRENT PIN IS INCORRECT")
                    elif not new_pin.isdigit() or len(new_pin) != 6:
                        st.error("NEW PIN MUST BE EXACTLY 6 NUMERIC DIGITS")
                    elif new_pin != conf_pin:
                        st.error("NEW PINS DO NOT MATCH")
                    else:
                        admin_data["pin_hash"] = hash_secret(new_pin)
                        save_admin_data(admin_data)
                        st.success("PIN UPDATED! SESSION TERMINATED.")
                        st.session_state.current_user = None
                        st.session_state.pin_verified = False
                        st.session_state.page = "login"
                        st.rerun()
                        
            elif change_option == "VIEW SECURITY AUDIT LOGS":
                st.markdown("### 🛡️ LIVE SECURITY EVENT LOGS")
                if st.session_state.audit_logs:
                    for log in reversed(st.session_state.audit_logs[-10:]):
                        st.code(log)
                else:
                    st.info("NO SECURITY EVENTS RECORDED.")

        if st.button("DISCONNECT & LOCK TERMINAL", type="primary"):
            log_security_event("LOGOUT", "User disconnected.")
            st.session_state.current_user = None
            st.session_state.pin_verified = False
            st.session_state.page = "login"
            st.rerun()

st.markdown("""
<div class="footer-box">
    ● FULL SCREEN DESKTOP SECURE | KUSHAL PRO MAX TRADING © 2026
</div>
""", unsafe_allow_html=True)

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kushal Pro Max Trading - Indian Market</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body { background-color: #0b0f19; color: #e2e8f0; font-family: 'Segoe UI', sans-serif; }
        .trading-card { background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(30, 41, 59, 0.8); backdrop-filter: blur(12px); transition: all 0.2s; }
        .trading-card:hover { border-color: #10b981; transform: translateY(-2px); }
        .glow-text { text-shadow: 0 0 10px rgba(16, 185, 129, 0.3); }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #0b0f19; }
        ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between p-4 md:p-6">
    <div>
        <header class="flex flex-col md:flex-row items-center justify-between border-b border-slate-800 pb-4 mb-6 gap-4">
            <div class="flex items-center gap-6">
                <a href="index.html" class="flex items-center gap-2 group text-left">
                    <div class="p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/20 group-hover:border-emerald-500/50 transition">
                        <i data-lucide="arrow-left" class="w-5 h-5 text-emerald-400"></i>
                    </div>
                    <div>
                        <span class="text-sm md:text-base font-bold tracking-wider text-emerald-400 glow-text block uppercase">Kushal Pro Max Trading</span>
                        <span class="text-[10px] text-slate-400 tracking-widest uppercase">Indian Market Terminal</span>
                    </div>
                </a>
            </div>
            <div class="flex items-center gap-3 w-full md:w-auto">
                <div class="relative w-full md:w-72">
                    <i data-lucide="search" class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"></i>
                    <input type="text" id="searchInput" onkeyup="filterCards()" placeholder="Search Nifty, Sensex, TCS..." 
                           class="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-4 py-2 text-xs text-slate-200 focus:outline-none focus:border-emerald-500">
                </div>
            </div>
        </header>

        <main>
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-xs uppercase font-bold tracking-wider text-slate-400">Indian Indices & Key Stocks</h2>
                <span class="text-[11px] text-slate-500">Click card for Performance Chart & Analytics</span>
            </div>
            <div id="cardsGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"></div>
        </main>
    </div>

    <!-- MODAL -->
    <div id="chartModal" class="fixed inset-0 bg-black/80 backdrop-blur-md hidden items-center justify-center p-4 z-50">
        <div class="bg-slate-900 border border-slate-800 rounded-xl w-full max-w-5xl max-h-[90vh] flex flex-col overflow-hidden shadow-2xl">
            <div class="flex items-center justify-between p-4 border-b border-slate-800 bg-slate-950">
                <div class="flex items-center gap-3">
                    <h3 id="modalTitle" class="text-base font-bold text-slate-100"></h3>
                    <span id="modalPrice" class="text-sm font-semibold text-emerald-400"></span>
                    <span id="modalChange" class="text-xs font-medium"></span>
                </div>
                <div class="flex items-center gap-3">
                    <button id="chartSwitchBtn" onclick="toggleChartMode()" class="px-3 py-1.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-md text-xs font-semibold hover:bg-emerald-500/20 transition flex items-center gap-1.5">
                        <i data-lucide="candlestick-chart" class="w-4 h-4"></i><span>Switch to TradingView Candlestick</span>
                    </button>
                    <button onclick="closeModal()" class="text-slate-400 hover:text-white"><i data-lucide="x" class="w-5 h-5"></i></button>
                </div>
            </div>
            <div class="flex-1 overflow-y-auto p-4 space-y-6">
                <div class="bg-slate-950/70 border border-slate-800 rounded-lg p-3 h-[380px] relative">
                    <div id="lineChartWrapper" class="w-full h-full"><canvas id="simpleLineChart"></canvas></div>
                    <div id="tradingviewWrapper" class="w-full h-full hidden"><div id="tradingview_widget_container" class="w-full h-full"></div></div>
                </div>
                <!-- Fundamentals -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="bg-slate-950 border border-slate-800 rounded-lg p-4 text-xs space-y-2">
                        <h4 class="font-bold uppercase text-slate-400 mb-2">Market Metrics</h4>
                        <div class="flex justify-between"><span class="text-slate-500">Today Open:</span><strong id="mOpen" class="text-slate-200"></strong></div>
                        <div class="flex justify-between"><span class="text-slate-500">Prev Close:</span><strong id="mClose" class="text-slate-200"></strong></div>
                        <div class="flex justify-between"><span class="text-slate-500">52W High / Low:</span><strong id="mHighLow" class="text-slate-200"></strong></div>
                    </div>
                    <div class="bg-slate-950 border border-slate-800 rounded-lg p-4 text-xs space-y-2">
                        <h4 class="font-bold uppercase text-slate-400 mb-2">Shareholding Pattern</h4>
                        <div class="flex justify-between"><span class="text-slate-400">Promoter:</span><strong id="mPromoter" class="text-slate-200"></strong></div>
                        <div class="flex justify-between"><span class="text-slate-400">FII / DII:</span><strong id="mFii" class="text-slate-200"></strong></div>
                        <div class="flex justify-between"><span class="text-slate-400">Public:</span><strong id="mPublic" class="text-slate-200"></strong></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        lucide.createIcons();
        const dataList = [
            { id: 'nifty', name: 'NIFTY 50', tv: 'NSE:NIFTY', price: 24350, change: 120, pct: 0.50, open: 24230, pClose: 24210, hl: '26,277 / 21,285', promoter: '71.77%', fii: '12.45%', pub: '15.78%' },
            { id: 'sensex', name: 'SENSEX', tv: 'BSE:SENSEX', price: 79800, change: 310, pct: 0.39, open: 79490, pClose: 79490, hl: '85,978 / 70,150', promoter: '70.50%', fii: '14.00%', pub: '15.50%' },
            { id: 'tcs', name: 'TCS (Tata Consultancy)', tv: 'NSE:TCS', price: 4150, change: 45, pct: 1.10, open: 4100, pClose: 4104, hl: '4,585 / 3,313', promoter: '71.77%', fii: '12.45%', pub: '15.78%' },
            { id: 'reliance', name: 'RELIANCE INDUSTRIES', tv: 'NSE:RELIANCE', price: 2980, change: -12, pct: -0.41, open: 2995, pClose: 2992, hl: '3,217 / 2,220', promoter: '50.30%', fii: '22.10%', pub: '27.60%' }
        ];

        function renderCards(list) {
            const grid = document.getElementById('cardsGrid');
            grid.innerHTML = '';
            list.forEach(i => {
                const pos = i.change >= 0;
                grid.innerHTML += `
                    <div onclick="openModal('${i.id}')" class="trading-card rounded-xl p-4 cursor-pointer space-y-3">
                        <div class="flex justify-between items-center"><span class="font-bold text-sm text-slate-100">${i.name}</span>
                        <span class="text-xs px-2 py-0.5 rounded ${pos ? 'text-emerald-400 bg-emerald-500/10' : 'text-rose-400 bg-rose-500/10'}">${pos ? '+' : ''}${i.pct}%</span></div>
                        <div class="text-2xl font-extrabold ${pos ? 'text-emerald-400' : 'text-rose-400'}">${i.price.toLocaleString()}</div>
                        <div class="text-xs text-slate-400">Open: ${i.open} | Prev Close: ${i.pClose}</div>
                    </div>`;
            });
        }
        renderCards(dataList);

        function filterCards() {
            const q = document.getElementById('searchInput').value.toLowerCase();
            renderCards(dataList.filter(i => i.name.toLowerCase().includes(q)));
        }

        let activeItem = null, mode = 'LINE', chartInst = null;
        function openModal(id) {
            activeItem = dataList.find(x => x.id === id);
            document.getElementById('modalTitle').innerText = activeItem.name;
            document.getElementById('modalPrice').innerText = activeItem.price.toLocaleString();
            document.getElementById('modalChange').innerText = `${activeItem.change >= 0 ? '+' : ''}${activeItem.change} (${activeItem.pct}%)`;
            document.getElementById('mOpen').innerText = activeItem.open;
            document.getElementById('mClose').innerText = activeItem.pClose;
            document.getElementById('mHighLow').innerText = activeItem.hl;
            document.getElementById('mPromoter').innerText = activeItem.promoter;
            document.getElementById('mFii').innerText = activeItem.fii;
            document.getElementById('mPublic').innerText = activeItem.pub;
            
            mode = 'LINE';
            updateChart();
            document.getElementById('chartModal').classList.remove('hidden');
            document.getElementById('chartModal').classList.add('flex');
        }

        function toggleChartMode() {
            mode = mode === 'LINE' ? 'CANDLE' : 'LINE';
            updateChart();
        }

        function updateChart() {
            if (mode === 'LINE') {
                document.getElementById('lineChartWrapper').classList.remove('hidden');
                document.getElementById('tradingviewWrapper').classList.add('hidden');
                document.getElementById('chartSwitchBtn').innerHTML = `<i data-lucide="candlestick-chart" class="w-4 h-4"></i><span>Switch to TradingView Candlestick</span>`;
                
                const ctx = document.getElementById('simpleLineChart').getContext('2d');
                if (chartInst) chartInst.destroy();
                chartInst = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['9:15', '10:00', '11:00', '12:00', '1:00', '2:00', '3:30'],
                        datasets: [{ data: [activeItem.open, activeItem.open+10, activeItem.open-20, activeItem.price-15, activeItem.price+5, activeItem.price], borderColor: '#10b981', fill: true, backgroundColor: 'rgba(16,185,129,0.1)', tension: 0.3 }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
                });
            } else {
                document.getElementById('lineChartWrapper').classList.add('hidden');
                document.getElementById('tradingviewWrapper').classList.remove('hidden');
                document.getElementById('chartSwitchBtn').innerHTML = `<i data-lucide="line-chart" class="w-4 h-4"></i><span>Switch to Simple Line Chart</span>`;
                document.getElementById('tradingview_widget_container').innerHTML = '';
                new TradingView.widget({ "autosize": true, "symbol": activeItem.tv, "interval": "5", "theme": "dark", "style": "1", "locale": "en", "container_id": "tradingview_widget_container" });
            }
            lucide.createIcons();
        }

        function closeModal() { document.getElementById('chartModal').classList.add('hidden'); }
    </script>
</body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kushal Pro Max Trading - Crypto Market</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body { background-color: #0b0f19; color: #e2e8f0; font-family: 'Segoe UI', sans-serif; }
        .trading-card { background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(30, 41, 59, 0.8); transition: all 0.2s; }
        .trading-card:hover { border-color: #f59e0b; transform: translateY(-2px); }
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between p-4 md:p-6">
    <div>
        <header class="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
            <a href="index.html" class="flex items-center gap-2 text-amber-400 font-bold">
                <i data-lucide="arrow-left" class="w-5 h-5"></i> Back to Home / Terminal
            </a>
            <h1 class="text-base font-bold uppercase tracking-wider text-amber-400">Crypto Market Terminal</h1>
        </header>

        <main class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="trading-card rounded-xl p-6 space-y-4">
                <h2 class="text-lg font-bold text-slate-100">Bitcoin (BTC / USDT)</h2>
                <div class="text-3xl font-black text-amber-400">$68,450.00</div>
                <div class="h-[350px]" id="tv_btc"></div>
            </div>
            <div class="trading-card rounded-xl p-6 space-y-4">
                <h2 class="text-lg font-bold text-slate-100">Ethereum (ETH / USDT)</h2>
                <div class="text-3xl font-black text-amber-400">$3,520.00</div>
                <div class="h-[350px]" id="tv_eth"></div>
            </div>
        </main>
    </div>
    <script>
        lucide.createIcons();
        new TradingView.widget({ "autosize": true, "symbol": "BINANCE:BTCUSDT", "interval": "15", "theme": "dark", "style": "1", "locale": "en", "container_id": "tv_btc" });
        new TradingView.widget({ "autosize": true, "symbol": "BINANCE:ETHUSDT", "interval": "15", "theme": "dark", "style": "1", "locale": "en", "container_id": "tv_eth" });
    </script>
</body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kushal Pro Max Trading - US Market</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body { background-color: #0b0f19; color: #e2e8f0; font-family: 'Segoe UI', sans-serif; }
        .trading-card { background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(30, 41, 59, 0.8); transition: all 0.2s; }
        .trading-card:hover { border-color: #3b82f6; transform: translateY(-2px); }
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between p-4 md:p-6">
    <div>
        <header class="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
            <a href="index.html" class="flex items-center gap-2 text-blue-400 font-bold">
                <i data-lucide="arrow-left" class="w-5 h-5"></i> Back to Home / Terminal
            </a>
            <h1 class="text-base font-bold uppercase tracking-wider text-blue-400">US Market Terminal (Nasdaq & S&P)</h1>
        </header>

        <main class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="trading-card rounded-xl p-6 space-y-4">
                <h2 class="text-lg font-bold text-slate-100">Nasdaq Composite (IXIC)</h2>
                <div class="text-3xl font-black text-blue-400">18,518.60</div>
                <div class="h-[350px]" id="tv_nasdaq"></div>
            </div>
            <div class="trading-card rounded-xl p-6 space-y-4">
                <h2 class="text-lg font-bold text-slate-100">Tesla Inc. (TSLA)</h2>
                <div class="text-3xl font-black text-blue-400">$245.50</div>
                <div class="h-[350px]" id="tv_tesla"></div>
            </div>
        </main>
    </div>
    <script>
        lucide.createIcons();
        new TradingView.widget({ "autosize": true, "symbol": "NASDAQ:IXIC", "interval": "15", "theme": "dark", "style": "1", "locale": "en", "container_id": "tv_nasdaq" });
        new TradingView.widget({ "autosize": true, "symbol": "NASDAQ:TSLA", "interval": "15", "theme": "dark", "style": "1", "locale": "en", "container_id": "tv_tesla" });
    </script>
</body>
</html>
