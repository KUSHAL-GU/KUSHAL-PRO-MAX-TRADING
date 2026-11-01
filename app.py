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
        st.info("SET UP YOUR PERMANENT MASTER ACCOUNT & 6-DIGIT PIN.")
        new_user = st.text_input("CREATE MASTER USER ID", placeholder="ENTER YOUR USER ID")
        new_pwd = st.text_input("CREATE PASSWORD", type="password", placeholder="ENTER SECURE PASSWORD (MIN 8 CHARS)")
        confirm_pwd = st.text_input("CONFIRM PASSWORD", type="password", placeholder="RE-ENTER PASSWORD")
        kds_code = st.text_input("SECRET KDS RECOVERY CODE", type="password", placeholder="USED FOR PASSWORD/ID RECOVERY")
        
        col1, col2 = st.columns(2)
        with col1:
            terminal_pin = st.text_input("6-DIGIT TERMINAL PIN", type="password", max_chars=6, placeholder="6 DIGITS")
        with col2:
            confirm_pin = st.text_input("CONFIRM 6-DIGIT PIN", type="password", max_chars=6, placeholder="RE-ENTER 6 DIGITS")

        if st.button("CREATE MASTER ACCOUNT →", type="primary"):
            if not all([new_user, new_pwd, confirm_pwd, kds_code, terminal_pin, confirm_pin]):
                st.error("PLEASE FILL ALL REQUIRED FIELDS")
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
                    "password": new_pwd,
                    "kds": kds_code,
                    "pin": terminal_pin
                }
                save_admin_data(data)
                st.success("MASTER ACCOUNT CREATED & LOCKED SECURELY!")
                st.rerun()

        if st.button("← BACK TO LOGIN / BYPASS"):
            st.session_state.page = "login"
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

        if st.button("FORGOT USER ID OR PASSWORD?"):
            st.session_state.page = "forgot"
            st.rerun()

# ----------------- 6-DIGIT PIN GATEWAY -----------------
elif st.session_state.page == "pin_verify":
    st.markdown('<div class="heading-box">ENTER 6-DIGIT TERMINAL PIN</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.info("ENTER YOUR 6-DIGIT SECURITY PIN TO UNLOCK THE TERMINAL.")
        pin_input = st.text_input("6-DIGIT PIN CODE", type="password", max_chars=6, placeholder="••••••")
        
        if st.button("UNLOCK TERMINAL →", type="primary"):
            if pin_input == admin_data["pin"]:
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("INVALID 6-DIGIT PIN")
                
        if st.button("← CANCEL / BACK TO LOGIN"):
            st.session_state.current_user = None
            st.session_state.page = "login"
            st.rerun()

# ----------------- FORGOT / RECOVERY PAGE -----------------
elif st.session_state.page == "forgot":
    st.markdown('<div class="heading-box">ACCOUNT RECOVERY & ASSISTANCE</div>', unsafe_allow_html=True)
    with st.container(border=True):
        option = st.selectbox("SELECT RECOVERY ACTION", ["RESET PASSWORD", "RETRIEVE USER ID"])
        st.markdown("---")
        
        if option == "RESET PASSWORD":
            u_id = st.text_input("ENTER MASTER USER ID")
            kds_in = st.text_input("ENTER SECRET KDS RECOVERY CODE", type="password")
            new_pwd = st.text_input("ENTER NEW PASSWORD", type="password", placeholder="MIN 8 CHARACTERS")
            confirm_pwd = st.text_input("CONFIRM NEW PASSWORD", type="password", placeholder="RE-ENTER NEW PASSWORD")
            
            if st.button("UPDATE PASSWORD →", type="primary"):
                if u_id == admin_data["user_id"] and kds_in == admin_data["kds"]:
                    if len(new_pwd) < 8:
                        st.error("PASSWORD MUST BE AT LEAST 8 CHARACTERS")
                    elif new_pwd != confirm_pwd:
                        st.error("PASSWORDS DO NOT MATCH")
                    else:
                        admin_data["password"] = new_pwd
                        save_admin_data(admin_data)
                        st.success("PASSWORD UPDATED SUCCESSFULLY! PLEASE LOGIN.")
                        st.session_state.page = "login"
                        st.rerun()
                else:
                    st.error("RECOVERY AUTHORIZATION FAILED")
                    
        elif option == "RETRIEVE USER ID":
            kds_in = st.text_input("ENTER SECRET KDS RECOVERY CODE", type="password")
            if st.button("RETRIEVE USER ID →", type="primary"):
                if kds_in == admin_data["kds"]:
                    st.success(f"YOUR REGISTERED USER ID IS: {admin_data['user_id']}")
                else:
                    st.error("INVALID KDS RECOVERY CODE")

        if st.button("← RETURN TO LOGIN"):
            st.session_state.page = "login"
            st.rerun()

# ----------------- DASHBOARD -----------------
elif st.session_state.page == "dashboard":
    st.markdown('<div class="heading-box">TRADING TERMINAL ACTIVE</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.success(f"WELCOME BACK, {admin_data['user_id'].upper()}")
        st.markdown("""
        <div style="background:#10271A; border:1px solid #17683B; border-radius:10px; padding:15px; text-align:center;">
            <h3 style="color:#00F080; margin-bottom:5px; font-size:16px;">KUSHAL PRO MAX ENGINE</h3>
            <p style="color:#008F49; font-size:12px; margin-bottom:5px;">PRIVATE HIGH-SPEED ANALYTICS & 6-DIGIT PIN UNLOCKED</p>
            <p style="color:#00E875; font-size:11px;">● SYSTEM FULLY SECURE</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("DISCONNECT & LOCK TERMINAL", type="primary"):
            st.session_state.current_user = None
            st.session_state.page = "login"
            st.rerun()

st.markdown("""
<div class="footer-box">
    ● SYSTEM ONLINE | SINGLE ADMIN & 6-DIGIT PIN SECURED | KUSHAL PRO MAX TRADING © 2026
</div>
""", unsafe_allow_html=True)
