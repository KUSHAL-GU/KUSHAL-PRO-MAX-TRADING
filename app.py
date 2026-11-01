import streamlit as st

st.set_page_config(
    page_title="KUSHAL PRO MAX TRADING",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if "page" not in st.session_state:
    st.session_state.page = "login"

if "users_db" not in st.session_state:
    st.session_state.users_db = {}

# Clean CSS designed to prevent overflow and fit single screen (Compact Width Fix)
st.markdown("""
<style>
.stApp {
    background: #020805;
    color: #00A94F;
    font-family: 'Segoe UI', Arial, sans-serif;
}
.block-container {
    max-width: 400px !important;
    padding: 10px 10px 15px !important;
    margin: auto !important;
}
.main-header {
    background: #050D09;
    border: 2px solid #174B30;
    border-radius: 12px;
    padding: 10px;
    text-align: center;
    margin-bottom: 8px;
    box-shadow: 0 0 10px rgba(0, 255, 102, 0.08);
}
.welcome-tag {
    background: #092318;
    border: 1px solid #00E875;
    border-radius: 16px;
    padding: 2px 10px;
    color: #00E875;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    display: inline-block;
    margin-bottom: 4px;
}
.main-title {
    color: #00F080;
    font-size: 17px;
    font-weight: 750;
    letter-spacing: 0.8px;
    margin: 2px 0;
}
.sub-title {
    color: #008F49;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1px;
    margin: 0;
}
.heading-box {
    background: #0B2015;
    border: 1px solid #17683B;
    border-radius: 6px;
    padding: 6px;
    text-align: center;
    margin-bottom: 8px;
    color: #00E875;
    font-size: 12px;
    font-weight: 750;
    letter-spacing: 1.5px;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #09170F;
    border: 1px solid #174B30;
    border-radius: 10px;
    padding: 8px 10px;
    margin-bottom: 8px;
}
.stTextInput label {
    color: #00C968 !important;
    font-size: 10px !important;
    font-weight: 700 !important;
}
.stTextInput input {
    background: #10271A !important;
    color: #00F080 !important;
    border: 1px solid #17683B !important;
    border-radius: 5px !important;
    min-height: 30px !important;
    padding: 4px 8px !important;
    font-size: 12px !important;
}
.stButton button {
    width: 100% !important;
    min-height: 32px !important;
    border-radius: 5px !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    border: 1px solid #17683B !important;
    margin-top: 3px;
    margin-bottom: 3px;
}
.stButton button[kind="primary"] {
    background: #00D875 !important;
    color: #031008 !important;
    border: 1px solid #00F080 !important;
}
.stButton button[kind="secondary"] {
    background: #10271A !important;
    color: #00E875 !important;
}
.footer-box {
    background: #08180F;
    border: 1px solid #174B30;
    border-radius: 5px;
    padding: 4px;
    text-align: center;
    color: #008F49;
    font-size: 9px;
    letter-spacing: 0.8px;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <div class="welcome-tag">WELCOME TO</div>
    <div class="main-title">KUSHAL PRO MAX TRADING</div>
    <div class="sub-title">ADVANCED FINANCIAL ANALYTICS</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.page == "login":
    st.markdown('<div class="heading-box">SECURE LOGIN</div>', unsafe_allow_html=True)
    with st.container(border=True):
        user_id = st.text_input("USER ID", placeholder="ENTER YOUR USER ID")
        password = st.text_input("PASSWORD", type="password", placeholder="ENTER YOUR PASSWORD")
        
        if st.button("SECURE LOGIN →", type="primary"):
            if user_id in st.session_state.users_db and st.session_state.users_db[user_id]["password"] == password:
                st.session_state.current_user = user_id
                st.session_state.page = "otp"
                st.rerun()
            else:
                st.error("INVALID USER ID OR PASSWORD")
                
        if st.button("FORGOT PASSWORD?"):
            st.session_state.page = "forgot"
            st.rerun()
            
        if st.button("+ CREATE NEW ACCOUNT"):
            st.session_state.page = "register"
            st.rerun()
            
        st.markdown('<p style="text-align:center; color:#008F49; font-size:10px; margin-top:3px;">NEW USER? REGISTER YOUR ACCOUNT</p>', unsafe_allow_html=True)

elif st.session_state.page == "register":
    st.markdown('<div class="heading-box">CREATE NEW ACCOUNT</div>', unsafe_allow_html=True)
    with st.container(border=True):
        new_user_id = st.text_input("CREATE USER ID", placeholder="ENTER A UNIQUE USER ID")
        new_password = st.text_input("CREATE PASSWORD", type="password", placeholder="CREATE YOUR PASSWORD")
        confirm_password = st.text_input("CONFIRM PASSWORD", type="password", placeholder="RE-ENTER PASSWORD")
        new_mobile = st.text_input("MOBILE NUMBER", placeholder="ENTER 10 DIGIT NUMBER")
        kds_info = st.text_input("KDS RECOVERY CODE", type="password", placeholder="CREATE RECOVERY CODE")
        
        if st.button("REGISTER ACCOUNT →", type="primary"):
            if not all([new_user_id, new_password, confirm_password, new_mobile, kds_info]):
                st.error("PLEASE FILL ALL REQUIRED FIELDS")
            elif new_user_id in st.session_state.users_db:
                st.error("USER ID ALREADY EXISTS")
            elif len(new_password) < 8:
                st.error("PASSWORD MUST BE AT LEAST 8 CHARACTERS")
            elif new_password != confirm_password:
                st.error("PASSWORDS DO NOT MATCH")
            elif not new_mobile.isdigit() or len(new_mobile) != 10:
                st.error("ENTER A VALID 10 DIGIT MOBILE NUMBER")
            else:
                st.session_state.users_db[new_user_id] = {
                    "password": new_password,
                    "mobile": new_mobile,
                    "kds": kds_info
                }
                st.success("ACCOUNT CREATED SUCCESSFULLY")
                st.session_state.page = "login"
                st.rerun()
                
        if st.button("← BACK TO LOGIN"):
            st.session_state.page = "login"
            st.rerun()

elif st.session_state.page == "otp":
    st.markdown('<div class="heading-box">TWO FACTOR AUTHENTICATION</div>', unsafe_allow_html=True)
    user = st.session_state.current_user
    mobile = st.session_state.users_db[user]["mobile"]
    with st.container(border=True):
        st.info(f"DEMO OTP: 1234 | MOBILE ENDING: {mobile[-4:]}")
        otp_input = st.text_input("ENTER 4 DIGIT OTP", type="password")
        if st.button("VERIFY & LAUNCH TERMINAL →", type="primary"):
            if otp_input == "1234":
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("INVALID OTP")
        if st.button("CANCEL LOGIN"):
            st.session_state.page = "login"
            st.rerun()

elif st.session_state.page == "forgot":
    st.markdown('<div class="heading-box">ACCOUNT RECOVERY</div>', unsafe_allow_html=True)
    with st.container(border=True):
        option = st.selectbox("SELECT RECOVERY OPTION", ["RESET PASSWORD", "RETRIEVE USER ID", "RETRIEVE MOBILE NUMBER"])
        st.markdown("---")
        if option == "RESET PASSWORD":
            u_id = st.text_input("ENTER USER ID")
            kds_in = st.text_input("ENTER KDS RECOVERY CODE", type="password")
            new_pwd = st.text_input("ENTER NEW PASSWORD", type="password")
            confirm_pwd = st.text_input("CONFIRM NEW PASSWORD", type="password")
            if st.button("RESET PASSWORD →", type="primary"):
                if u_id in st.session_state.users_db and st.session_state.users_db[u_id]["kds"] == kds_in:
                    if len(new_pwd) < 8:
                        st.error("PASSWORD MUST BE AT LEAST 8 CHARACTERS")
                    elif new_pwd != confirm_pwd:
                        st.error("PASSWORDS DO NOT MATCH")
                    else:
                        st.session_state.users_db[u_id]["password"] = new_pwd
                        st.success("PASSWORD RESET SUCCESSFULLY")
                else:
                    st.error("RECOVERY VERIFICATION FAILED")
        elif option == "RETRIEVE USER ID":
            mob = st.text_input("ENTER MOBILE NUMBER")
            kds_in = st.text_input("ENTER KDS RECOVERY CODE", type="password")
            if st.button("RETRIEVE USER ID →", type="primary"):
                found = False
                for uid, data in st.session_state.users_db.items():
                    if data["mobile"] == mob and data["kds"] == kds_in:
                        st.success(f"YOUR USER ID: {uid}")
                        found = True
                        break
                if not found:
                    st.error("NO MATCHING ACCOUNT FOUND")
        elif option == "RETRIEVE MOBILE NUMBER":
            u_id = st.text_input("ENTER USER ID")
            pwd = st.text_input("ENTER PASSWORD", type="password")
            if st.button("RETRIEVE MOBILE NUMBER →", type="primary"):
                if u_id in st.session_state.users_db and st.session_state.users_db[u_id]["password"] == pwd:
                    mobile = st.session_state.users_db[u_id]["mobile"]
                    st.success(f"REGISTERED MOBILE: ******{mobile[-4:]}")
                else:
                    st.error("INVALID USER ID OR PASSWORD")
        if st.button("← RETURN TO LOGIN"):
            st.session_state.page = "login"
            st.rerun()

elif st.session_state.page == "dashboard":
    st.markdown('<div class="heading-box">TRADING DASHBOARD</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.success(f"WELCOME {st.session_state.current_user.upper()}")
        st.markdown("""
        <div style="background:#10271A; border:1px solid #17683B; border-radius:8px; padding:10px; text-align:center;">
            <h3 style="color:#00F080; margin-bottom:3px; font-size:15px;">KUSHAL PRO MAX ENGINE</h3>
            <p style="color:#008F49; font-size:11px; margin-bottom:3px;">ADVANCED FINANCIAL ANALYTICS</p>
            <p style="color:#00E875; font-size:10px;">● TERMINAL ACTIVE</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("DISCONNECT / LOGOUT", type="primary"):
            st.session_state.current_user = None
            st.session_state.page = "login"
            st.rerun()

st.markdown("""
<div class="footer-box">
    ● SYSTEM ONLINE | KUSHAL PRO MAX TRADING © 2026
</div>
""", unsafe_allow_html=True)
