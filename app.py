import streamlit as st
import json
import os

st.set_page_config(
    page_title="KUSHAL PRO MAX TRADING",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

DB_FILE = "admin_config.json"

def load_admin_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return None

def save_admin_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

if "page" not in st.session_state:
    st.session_state.page = "login"

admin_data = load_admin_data()

# Styling with Green Glow & Tech Fonts
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
    <div class="sub-title">SECURE TERMINAL GATEWAY</div>
</div>
""", unsafe_allow_html=True)

# ----------------- INITIAL SETUP (First Time Only) -----------------
if admin_data is None:
    st.markdown('<div class="heading-box">INITIAL MASTER SETUP</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.info("SET UP YOUR MASTER ACCOUNT, MOBILE, KDS CODE & 6-DIGIT PIN.")
        new_user = st.text_input("CREATE MASTER USER ID", placeholder="ENTER YOUR USER ID")
        mobile_no = st.text_input("MOBILE NUMBER (FOR OTP VERIFICATION)", placeholder="10-DIGIT MOBILE NUMBER", max_chars=10)
        new_pwd = st.text_input("CREATE PASSWORD", type="password", placeholder="MIN 8 CHARACTERS")
        confirm_pwd = st.text_input("CONFIRM PASSWORD", type="password", placeholder="RE-ENTER PASSWORD")
        kds_code = st.text_input("SECRET KDS RECOVERY CODE", type="password", placeholder="ULTIMATE RECOVERY MASTER KEY")
        
        col1, col2 = st.columns(2)
        with col1:
            terminal_pin = st.text_input("6-DIGIT TERMINAL PIN", type="password", max_chars=6, placeholder="6 DIGITS")
        with col2:
            confirm_pin = st.text_input("CONFIRM 6-DIGIT PIN", type="password", max_chars=6, placeholder="RE-ENTER 6 DIGITS")

        if st.button("CREATE MASTER ACCOUNT →", type="primary"):
            if not all([new_user, mobile_no, new_pwd, confirm_pwd, kds_code, terminal_pin, confirm_pin]):
                st.error("PLEASE FILL ALL REQUIRED FIELDS")
            elif len(mobile_no) != 10 or not mobile_no.isdigit():
                st.error("ENTER A VALID 10-DIGIT MOBILE NUMBER")
            elif len(new_pwd) < 8:
                st.error("PASSWORD MUST BE AT LEAST 8 CHARACTERS")
            elif new_pwd != confirm_pwd:
                st.error("PASSWORDS DO NOT MATCH")
            elif not terminal_pin.isdigit() or len(terminal_pin) != 6:
                st.error("TERMINAL PIN MUST BE EXACTLY 6 DIGITS")
            elif terminal_pin != confirm_pin:
                st.error("6-DIGIT PINS DO NOT MATCH")
            else:
                data = {
                    "user_id": new_user,
                    "mobile": mobile_no,
                    "password": new_pwd,
                    "kds": kds_code,
                    "pin": terminal_pin
                }
                save_admin_data(data)
                st.success("MASTER ACCOUNT CREATED & SECURED!")
                st.rerun()

# ----------------- LOGIN PAGE -----------------
elif st.session_state.page == "login":
    st.markdown('<div class="heading-box">SECURE MASTER LOGIN</div>', unsafe_allow_html=True)
    with st.container(border=True):
        user_id = st.text_input("USER ID", placeholder="ENTER MASTER USER ID")
        password = st.text_input("PASSWORD", type="password", placeholder="ENTER PASSWORD")

        if st.button("AUTHENTICATE →", type="primary"):
            if user_id == admin_data["user_id"] and password == admin_data["password"]:
                st.session_state.current_user = user_id
                st.session_state.page = "pin_verify"
                st.rerun()
            else:
                st.error("ACCESS DENIED: INVALID USER ID OR PASSWORD")

        if st.button("FORGOT PASSWORD / ID / PIN?"):
            st.session_state.page = "forgot_step1"
            st.rerun()

# ----------------- 6-DIGIT PIN GATEWAY -----------------
elif st.session_state.page == "pin_verify":
    st.markdown('<div class="heading-box">ENTER 6-DIGIT TERMINAL PIN</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.info("ENTER YOUR 6-DIGIT SECURITY PIN TO UNLOCK THE TERMINAL.")
        pin_input = st.text_input("6-DIGIT PIN CODE", type="password", max_chars=6, placeholder="••••••")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("UNLOCK TERMINAL →", type="primary"):
                if pin_input == admin_data["pin"]:
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("INVALID 6-DIGIT PIN")
        with col2:
            if st.button("FORGOT PIN?"):
                st.session_state.page = "forgot_step1"
                st.rerun()
                
        if st.button("← LOCK / BACK TO LOGIN"):
            st.session_state.current_user = None
            st.session_state.page = "login"
            st.rerun()

# ----------------- RECOVERY / FORGOT FLOW (STEP 1: Mobile & OTP) -----------------
elif st.session_state.page == "forgot_step1":
    st.markdown('<div class="heading-box">SECURITY RECOVERY (MOBILE OTP)</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.info("ENTER REGISTERED MOBILE NUMBER FOR OTP VERIFICATION.")
        input_mobile = st.text_input("REGISTERED MOBILE NUMBER", max_chars=10, placeholder="10-DIGIT NUMBER")
        
        if "otp_sent" not in st.session_state:
            st.session_state.otp_sent = False

        if st.button("SEND OTP VIA SMS"):
            if input_mobile == admin_data["mobile"]:
                st.session_state.otp_sent = True
                st.success("OTP SENT SUCCESSFULLY TO YOUR MOBILE! (DEMO OTP: 1234)")
            else:
                st.error("MOBILE NUMBER NOT MATCHED WITH SYSTEM RECORD")

        if st.session_state.otp_sent:
            otp_input = st.text_input("ENTER 4-DIGIT OTP", type="password", max_chars=4)
            if st.button("VERIFY OTP & PROCEED →", type="primary"):
                if otp_input == "1234":
                    st.session_state.otp_sent = False
                    st.session_state.page = "forgot_step2"
                    st.rerun()
                else:
                    st.error("INVALID OTP CODE")

        if st.button("← RETURN TO LOGIN"):
            st.session_state.otp_sent = False
            st.session_state.page = "login"
            st.rerun()

# ----------------- RECOVERY / FORGOT FLOW (STEP 2: Reset & KDS Master Override) -----------------
elif st.session_state.page == "forgot_step2":
    st.markdown('<div class="heading-box">CREDENTIAL RESET & KDS MASTER OVERRIDE</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.info("OTP VERIFIED. CHOOSE WHAT YOU WANT TO RESET OR USE KDS CODE FOR FULL RECOVERY.")
        
        reset_choice = st.selectbox("SELECT ACTION", ["RESET PASSWORD", "RESET 6-DIGIT PIN", "FULL RECOVERY VIA KDS CODE"])
        
        if reset_choice == "RESET PASSWORD":
            new_p = st.text_input("NEW PASSWORD", type="password")
            conf_p = st.text_input("CONFIRM NEW PASSWORD", type="password")
            if st.button("UPDATE PASSWORD NOW", type="primary"):
                if len(new_p) < 8:
                    st.error("PASSWORD MUST BE AT LEAST 8 CHARACTERS")
                elif new_p != conf_p:
                    st.error("PASSWORDS DO NOT MATCH")
                else:
                    admin_data["password"] = new_p
                    save_admin_data(admin_data)
                    st.success("PASSWORD UPDATED SUCCESSFULLY! PLEASE LOGIN.")
                    st.session_state.page = "login"
                    st.rerun()
                    
        elif reset_choice == "RESET 6-DIGIT PIN":
            new_pi = st.text_input("NEW 6-DIGIT PIN", type="password", max_chars=6)
            conf_pi = st.text_input("CONFIRM NEW 6-DIGIT PIN", type="password", max_chars=6)
            if st.button("UPDATE PIN NOW", type="primary"):
                if not new_pi.isdigit() or len(new_pi) != 6:
                    st.error("PIN MUST BE EXACTLY 6 DIGITS")
                elif new_pi != conf_pi:
                    st.error("PINS DO NOT MATCH")
                else:
                    admin_data["pin"] = new_pi
                    save_admin_data(admin_data)
                    st.success("6-DIGIT PIN UPDATED SUCCESSFULLY! PLEASE LOGIN.")
                    st.session_state.page = "login"
                    st.rerun()
                    
        elif reset_choice == "FULL RECOVERY VIA KDS CODE":
            st.warning("MASTER KDS OVERRIDE: USE THIS IF BOTH PASSWORD & PIN ARE LOST.")
            kds_input = st.text_input("ENTER SECRET KDS RECOVERY CODE", type="password")
            new_uid = st.text_input("NEW MASTER USER ID")
            new_p = st.text_input("NEW PASSWORD", type="password")
            new_pi = st.text_input("NEW 6-DIGIT PIN", type="password", max_chars=6)
            
            if st.button("EXECUTE MASTER KDS OVERRIDE →", type="primary"):
                if kds_input == admin_data["kds"]:
                    if not all([new_uid, new_p, new_pi]) or len(new_p) < 8 or len(new_pi) != 6:
                        st.error("PLEASE PROVIDE VALID USER ID, PASSWORD (MIN 8) & 6-DIGIT PIN")
                    else:
                        admin_data["user_id"] = new_uid
                        admin_data["password"] = new_p
                        admin_data["pin"] = new_pi
                        save_admin_data(admin_data)
                        st.success("MASTER OVERRIDE SUCCESSFUL! ALL CREDENTIALS UPDATED.")
                        st.session_state.page = "login"
                        st.rerun()
                else:
                    st.error("INVALID SECRET KDS RECOVERY CODE")

        if st.button("← RETURN TO LOGIN"):
            st.session_state.page = "login"
            st.rerun()

# ----------------- DASHBOARD -----------------
elif st.session_state.page == "dashboard":
    st.markdown('<div class="heading-box">TRADING TERMINAL ACTIVE</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.success(f"WELCOME BACK, {admin_data['user_id'].upper()}")
        st.markdown("""
        <div style="background:#10271A; border:1px solid #17683B; border-radius:10px; padding:15px; text-align:center; margin-bottom:15px;">
            <h3 style="color:#00F080; margin-bottom:5px; font-size:16px;">KUSHAL PRO MAX ENGINE</h3>
            <p style="color:#008F49; font-size:12px; margin-bottom:5px;">PRIVATE HIGH-SPEED ANALYTICS & SECURE OTP/KDS GUARDED</p>
            <p style="color:#00E875; font-size:11px;">● SYSTEM FULLY SECURED & RECOVERY READY</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Inner Settings for changing credentials
        with st.expander("⚙️ SECURITY & CREDENTIALS SETTINGS"):
            st.markdown("UPDATE YOUR PASSWORD OR 6-DIGIT PIN SECURELY FROM HERE.")
            change_option = st.selectbox("SELECT ACTION", ["CHANGE PASSWORD", "CHANGE 6-DIGIT PIN"])
            
            if change_option == "CHANGE PASSWORD":
                old_pwd = st.text_input("CURRENT PASSWORD", type="password")
                new_pwd = st.text_input("NEW PASSWORD (MIN 8 CHARS)", type="password")
                conf_pwd = st.text_input("CONFIRM NEW PASSWORD", type="password")
                if st.button("UPDATE PASSWORD NOW"):
                    if old_pwd != admin_data["password"]:
                        st.error("CURRENT PASSWORD is INCORRECT")
                    elif len(new_pwd) < 8:
                        st.error("NEW PASSWORD MUST BE AT LEAST 8 CHARACTERS")
                    elif new_pwd != conf_pwd:
                        st.error("NEW PASSWORDS DO NOT MATCH")
                    else:
                        admin_data["password"] = new_pwd
                        save_admin_data(admin_data)
                        st.success("PASSWORD UPDATED SUCCESSFULLY!")
            
            elif change_option == "CHANGE 6-DIGIT PIN":
                old_pin = st.text_input("CURRENT 6-DIGIT PIN", type="password", max_chars=6)
                new_pin = st.text_input("NEW 6-DIGIT PIN", type="password", max_chars=6)
                conf_pin = st.text_input("CONFIRM NEW 6-DIGIT PIN", type="password", max_chars=6)
                if st.button("UPDATE PIN NOW"):
                    if old_pin != admin_data["pin"]:
                        st.error("CURRENT 6-DIGIT PIN is INCORRECT")
                    elif not new_pin.isdigit() or len(new_pin) != 6:
                        st.error("NEW PIN MUST BE EXACTLY 6 DIGITS")
                    elif new_pin != conf_pin:
                        st.error("NEW PINS DO NOT MATCH")
                    else:
                        admin_data["pin"] = new_pin
                        save_admin_data(admin_data)
                        st.success("6-DIGIT PIN UPDATED SUCCESSFULLY!")

        if st.button("DISCONNECT & LOCK TERMINAL", type="primary"):
            st.session_state.current_user = None
            st.session_state.page = "login"
            st.rerun()

st.markdown("""
<div class="footer-box">
    ● SYSTEM ONLINE | MOBILE OTP & KDS SECURED | KUSHAL PRO MAX TRADING © 2026
</div>
""", unsafe_allow_html=True)
