import streamlit as st

# 1. Page Configuration & Futuristic Theme Setup
st.set_page_config(
    page_title="Kushal Pro Max Trading",
    page_icon="⚡",
    layout="centered"
)

# Custom Cyberpunk / Dark Green UI matching your exact requirements (CSS)
st.markdown("""
    <style>
    .stApp {
        background-color: #070e0a;
        color: #00FF66;
        font-family: 'Courier New', Courier, monospace;
    }
    .top-pill-badge {
        text-align: center;
        color: #00FF66;
        font-size: 11px;
        letter-spacing: 2.5px;
        background-color: #0d2114;
        border: 1px solid #143d22;
        padding: 6px 18px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 12px;
        font-weight: bold;
    }
    .main-title {
        text-align: center;
        color: #00FF66;
        font-size: 32px;
        font-weight: 900;
        letter-spacing: 3px;
        text-shadow: 0 0 15px rgba(0, 255, 102, 0.5);
        margin-bottom: 5px;
        line-height: 1.1;
    }
    .sub-title-trading {
        text-align: center;
        color: #00FF66;
        font-size: 14px;
        font-weight: bold;
        letter-spacing: 4px;
        margin-bottom: 8px;
        text-transform: uppercase;
    }
    .sub-text-analytics {
        text-align: center;
        color: #8fa397;
        font-size: 10px;
        letter-spacing: 2px;
        margin-bottom: 25px;
    }
    .divider-line {
        width: 100%;
        height: 1px;
        background-color: #143d22;
        margin: 0 auto 25px auto;
    }
    .card-container {
        background-color: #0b1711;
        border: 1px solid #143d22;
        border-radius: 16px;
        padding: 30px 25px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
        margin-bottom: 20px;
    }
    .section-heading {
        text-align: center;
        color: #00FF66;
        font-size: 18px;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 20px;
    }
    .field-label {
        color: #8fa397;
        font-size: 11px;
        letter-spacing: 1.5px;
        margin-bottom: 5px;
        font-weight: bold;
    }
    div.stButton > button:first-child {
        background-color: #00FF66;
        color: #070e0a;
        font-weight: 900;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 1px;
        border: none;
        width: 100%;
        border-radius: 8px;
        padding: 12px;
        box-shadow: 0 0 15px rgba(0, 255, 102, 0.3);
        margin-top: 10px;
    }
    div.stButton > button:first-child:hover {
        background-color: #00cc52;
        color: #070e0a;
        box-shadow: 0 0 20px rgba(0, 255, 102, 0.6);
    }
    .secondary-button-wrapper div.stButton > button:first-child {
        background-color: #0d2114;
        color: #00FF66;
        border: 1px solid #143d22;
    }
    .secondary-button-wrapper div.stButton > button:first-child:hover {
        background-color: #143d22;
        color: #00FF66;
    }
    input {
        background-color: #050f09 !important;
        color: #00FF66 !important;
        border: 1px solid #143d22 !important;
        border-radius: 8px !important;
    }
    .footer-text {
        display: flex;
        justify-content: space-between;
        color: #8fa397;
        font-size: 10px;
        letter-spacing: 1px;
        margin-top: 15px;
    }
    .footer-bottom {
        text-align: center;
        color: #5c7063;
        font-size: 10px;
        letter-spacing: 1px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Session State Initialization
if "page" not in st.session_state:
    st.session_state.page = "login"
if "users_db" not in st.session_state:
    st.session_state.users_db = {}

# 3. Header Section (Your Custom Layout)
st.markdown("<div style='text-align: center;'><span class='top-pill-badge'>WELCOME TO</span></div>", unsafe_allow_html=True)
st.markdown("<div class='main-title'>KUSHAL PRO MAX</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title-trading'>TRADING</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text-analytics'>ADVANCED FINANCIAL ANALYTICS</div>", unsafe_allow_html=True)
st.markdown("<div class='divider-line'></div>", unsafe_allow_html=True)

# Container for clean card styling
with st.container():
    st.markdown("<div class='card-container'>", unsafe_allow_html=True)

    # ----------------- REGISTRATION SCREEN -----------------
    if st.session_state.page == "register":
        st.markdown("<div class='section-heading'>CREATE ACCOUNT</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='field-label'>USER ID</div>", unsafe_allow_html=True)
        new_user_id = st.text_input("UID_REG", label_visibility="collapsed", placeholder="Choose your User ID")
        
        st.markdown("<div class='field-label'>PASSWORD</div>", unsafe_allow_html=True)
        new_password = st.text_input("PWD_REG", type="password", label_visibility="collapsed", placeholder="Set secure password")
        
        st.markdown("<div class='field-label'>MOBILE NUMBER</div>", unsafe_allow_html=True)
        new_mobile = st.text_input("MOB_REG", label_visibility="collapsed", placeholder="Enter mobile number")
        
        st.markdown("<div class='field-label'>KDS VERIFICATION CODE</div>", unsafe_allow_html=True)
        kds_info = st.text_input("KDS_REG", label_visibility="collapsed", placeholder="Enter KDS identification code")
        
        if st.button("REGISTER ACCOUNT →"):
            if new_user_id and new_password and new_mobile:
                st.session_state.users_db[new_user_id] = {
                    "password": new_password,
                    "mobile": new_mobile,
                    "kds": kds_info
                }
                st.success("✅ ACCOUNT CREATED SUCCESSFULLY.")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("❌ ERROR: FILL ALL REQUIRED FIELDS!")
                
        st.markdown("<div class='secondary-button-wrapper'>", unsafe_allow_html=True)
        if st.button("← BACK TO LOGIN"):
            st.session_state.page = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ----------------- LOGIN SCREEN -----------------
    elif st.session_state.page == "login":
        st.markdown("<div class='section-heading'>SECURE LOGIN</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='field-label'>USER ID</div>", unsafe_allow_html=True)
        user_id = st.text_input("UID_LOGIN", label_visibility="collapsed", placeholder="Enter your User ID")
        
        st.markdown("<div class='field-label'>PASSWORD</div>", unsafe_allow_html=True)
        password = st.text_input("PWD_LOGIN", type="password", label_visibility="collapsed", placeholder="••••••••••••")
        
        col_f1, col_f2 = st.columns([2, 1])
        with col_f2:
            if st.button("Forgot Password?", key="forgot_btn"):
                st.session_state.page = "forgot"
                st.rerun()

        if st.button("SECURE LOGIN →"):
            if user_id in st.session_state.users_db and st.session_state.users_db[user_id]["password"] == password:
                st.session_state.page = "otp"
                st.session_state.current_user = user_id
                st.rerun()
            else:
                st.error("❌ ACCESS DENIED: INVALID CREDENTIALS!")
                
        st.markdown("<div class='secondary-button-wrapper'>", unsafe_allow_html=True)
        if st.button("+ CREATE ACCOUNT"):
            st.session_state.page = "register"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div style='text-align: center; margin-top: 15px;'><span style='color: #8fa397; font-size: 11px;'>NEW USER? REGISTER YOUR ACCOUNT</span></div>", unsafe_allow_html=True)

    # ----------------- OTP SCREEN -----------------
    elif st.session_state.page == "otp":
        st.markdown("<div class='section-heading'>TWO-FACTOR AUTH</div>", unsafe_allow_html=True)
        user = st.session_state.current_user
        mobile = st.session_state.users_db[user]["mobile"]
        
        st.info(f"OTP DISPATCHED TO (*{mobile[-4:]}). [DEMO OTP: 1234]")
        
        st.markdown("<div class='field-label'>ENTER 4-DIGIT OTP</div>", unsafe_allow_html=True)
        otp_input = st.text_input("OTP_INPUT", type="password", label_visibility="collapsed", placeholder="1234")
        
        if st.button("VERIFY & LAUNCH →"):
            if otp_input == "1234":
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("❌ AUTHENTICATION FAILED: INVALID OTP!")

    # ----------------- RECOVERY SCREEN -----------------
    elif st.session_state.page == "forgot":
        st.markdown("<div class='section-heading'>SYSTEM RECOVERY</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='field-label'>SELECT RECOVERY MODE</div>", unsafe_allow_html=True)
        option = st.selectbox("REC_MODE", ["RESET PASSWORD", "RETRIEVE USER ID", "RETRIEVE MOBILE NUMBER"], label_visibility="collapsed")
        
        if option == "RESET PASSWORD":
            st.markdown("<div class='field-label'>USER ID</div>", unsafe_allow_html=True)
            u_id = st.text_input("R_UID", label_visibility="collapsed", placeholder="Enter User ID")
            st.markdown("<div class='field-label'>KDS CODE</div>", unsafe_allow_html=True)
            kds_in = st.text_input("R_KDS", label_visibility="collapsed", placeholder="Enter KDS Code")
            if st.button("EXECUTE RESET →"):
                if u_id in st.session_state.users_db and st.session_state.users_db[u_id]["kds"] == kds_in:
                    st.success(f"PASSWORD: {st.session_state.users_db[u_id]['password']}")
                else:
                    st.error("❌ VERIFICATION FAILED!")
                    
        elif option == "RETRIEVE USER ID":
            st.markdown("<div class='field-label'>MOBILE NUMBER</div>", unsafe_allow_html=True)
            mob = st.text_input("R_MOB", label_visibility="collapsed", placeholder="Enter Mobile Number")
            st.markdown("<div class='field-label'>KDS CODE</div>", unsafe_allow_html=True)
            kds_in = st.text_input("R_KDS2", label_visibility="collapsed", placeholder="Enter KDS Code")
            if st.button("FETCH USER ID →"):
                found = False
                for uid, data in st.session_state.users_db.items():
                    if data["mobile"] == mob and data["kds"] == kds_in:
                        st.success(f"USER ID: {uid}")
                        found = True
                        break
                if not found:
                    st.error("❌ NO MATCH FOUND!")
                    
        elif option == "RETRIEVE MOBILE NUMBER":
            st.markdown("<div class='field-label'>USER ID</div>", unsafe_allow_html=True)
            u_id = st.text_input("R_UID2", label_visibility="collapsed", placeholder="Enter User ID")
            st.markdown("<div class='field-label'>PASSWORD</div>", unsafe_allow_html=True)
            pwd = st.text_input("R_PWD", type="password", label_visibility="collapsed", placeholder="Enter Password")
            if st.button("FETCH MOBILE →"):
                if u_id in st.session_state.users_db and st.session_state.users_db[u_id]["password"] == pwd:
                    st.success(f"MOBILE: {st.session_state.users_db[u_id]['mobile']}")
                else:
                    st.error("❌ INVALID CREDENTIALS!")

        st.markdown("<div class='secondary-button-wrapper'>", unsafe_allow_html=True)
        if st.button("← RETURN TO LOGIN"):
            st.session_state.page = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ----------------- DASHBOARD -----------------
    elif st.session_state.page == "dashboard":
        st.markdown(f"<div class='section-heading'>TERMINAL ACTIVE</div>", unsafe_allow_html=True)
        st.success(f"🚀 WELCOME, {st.session_state.current_user.upper()}! ENGINE ONLINE.")
        st.markdown("<div class='secondary-button-wrapper'>", unsafe_allow_html=True)
        if st.button("DISCONNECT / LOGOUT"):
            st.session_state.page = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class='footer-text'>
        <span>🟢 SYSTEM ONLINE</span>
        <span>ENCRYPTED ACCESS</span>
    </div>
    <div class='footer-bottom'>
        KUSHAL PRO MAX © 2026
    </div>
""", unsafe_allow_html=True)
