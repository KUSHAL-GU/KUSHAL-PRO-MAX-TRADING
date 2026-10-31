import streamlit as st

# 1. Page Configuration & Futuristic Theme Setup
st.set_page_config(
    page_title="Kushal Pro Max Trading",
    page_icon="⚡",
    layout="centered"
)

# Custom Cyberpunk / Dark Green UI matching the exact reference image
st.markdown("""
    <style>
    .stApp {
        background-color: #040906;
        color: #00FF66;
        font-family: 'Courier New', Courier, monospace;
    }
    .badge-box {
        text-align: center;
        background-color: #0a1f13;
        border: 1px solid #133b22;
        color: #00FF66;
        font-size: 10px;
        letter-spacing: 2px;
        padding: 5px 16px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 12px;
        font-weight: bold;
    }
    .main-heading {
        text-align: center;
        color: #00FF66;
        font-size: 28px;
        font-weight: 900;
        letter-spacing: 2px;
        text-shadow: 0 0 15px rgba(0, 255, 102, 0.4);
        margin-bottom: 2px;
    }
    .sub-heading {
        text-align: center;
        color: #00FF66;
        font-size: 24px;
        font-weight: 900;
        letter-spacing: 3px;
        text-shadow: 0 0 12px rgba(0, 255, 102, 0.3);
        margin-bottom: 8px;
    }
    .analytics-text {
        text-align: center;
        color: #728a7b;
        font-size: 11px;
        letter-spacing: 1.5px;
        margin-bottom: 15px;
    }
    .divider {
        width: 100%;
        height: 1px;
        background-color: #133b22;
        margin: 0 auto 25px auto;
    }
    .card-box {
        background-color: #07120b;
        border: 1px solid #133b22;
        border-radius: 16px;
        padding: 28px 22px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
        margin-bottom: 15px;
    }
    .card-title {
        text-align: center;
        color: #00FF66;
        font-size: 18px;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 22px;
    }
    .input-label {
        color: #728a7b;
        font-size: 10px;
        letter-spacing: 1.5px;
        margin-bottom: 5px;
        font-weight: bold;
    }
    div.stButton > button:first-child {
        background-color: #00FF66;
        color: #040906;
        font-weight: 900;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 1px;
        border: none;
        width: 100%;
        border-radius: 8px;
        padding: 12px;
        box-shadow: 0 0 15px rgba(0, 255, 102, 0.4);
        margin-top: 10px;
    }
    div.stButton > button:first-child:hover {
        background-color: #00cc52;
        box-shadow: 0 0 20px rgba(0, 255, 102, 0.7);
    }
    .secondary-btn div.stButton > button:first-child {
        background-color: #0a1f13;
        color: #00FF66;
        border: 1px solid #133b22;
    }
    .secondary-btn div.stButton > button:first-child:hover {
        background-color: #133b22;
        color: #00FF66;
    }
    input {
        background-color: #040906 !important;
        color: #00FF66 !important;
        border: 1px solid #133b22 !important;
        border-radius: 8px !important;
    }
    .footer-row {
        display: flex;
        justify-content: space-between;
        color: #728a7b;
        font-size: 10px;
        letter-spacing: 1px;
        margin-top: 15px;
    }
    .footer-copy {
        text-align: center;
        color: #465c4f;
        font-size: 10px;
        letter-spacing: 1px;
        margin-top: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Session State Initialization
if "page" not in st.session_state:
    st.session_state.page = "login"
if "users_db" not in st.session_state:
    st.session_state.users_db = {}

# 3. Header Section (Exact Image Layout)
st.markdown("<div style='text-align: center;'><div class='badge-box'>WELCOME TO</div></div>", unsafe_allow_html=True)
st.markdown("<div class='main-heading'>KUSHAL PRO MAX</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-heading'>TRADING</div>", unsafe_allow_html=True)
st.markdown("<div class='analytics-text'>ADVANCED FINANCIAL ANALYTICS</div>", unsafe_allow_html=True)
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Main Card Container
with st.container():
    st.markdown("<div class='card-box'>", unsafe_allow_html=True)

    # ----------------- LOGIN SCREEN -----------------
    if st.session_state.page == "login":
        st.markdown("<div class='card-title'>SECURE LOGIN</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='input-label'>USER ID</div>", unsafe_allow_html=True)
        user_id = st.text_input("uid_login", label_visibility="collapsed", placeholder="Enter your User ID")
        
        st.markdown("<div class='input-label'>PASSWORD</div>", unsafe_allow_html=True)
        password = st.text_input("pwd_login", type="password", label_visibility="collapsed", placeholder="••••••••••••")
        
        col_f1, col_f2 = st.columns([2, 1])
        with col_f2:
            if st.button("Forgot Password?", key="forgot_link"):
                st.session_state.page = "forgot"
                st.rerun()

        if st.button("SECURE LOGIN →"):
            if user_id in st.session_state.users_db and st.session_state.users_db[user_id]["password"] == password:
                st.session_state.page = "otp"
                st.session_state.current_user = user_id
                st.rerun()
            else:
                st.error("ACCESS DENIED: INVALID CREDENTIALS!")
                
        st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
        if st.button("+ CREATE ACCOUNT"):
            st.session_state.page = "register"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div style='text-align: center; margin-top: 14px;'><span style='color: #728a7b; font-size: 10px; letter-spacing: 1px;'>NEW USER? REGISTER YOUR ACCOUNT</span></div>", unsafe_allow_html=True)

    # ----------------- REGISTRATION SCREEN -----------------
    elif st.session_state.page == "register":
        st.markdown("<div class='card-title'>CREATE ACCOUNT</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='input-label'>USER ID</div>", unsafe_allow_html=True)
        new_user_id = st.text_input("uid_reg", label_visibility="collapsed", placeholder="Enter User ID")
        
        st.markdown("<div class='input-label'>PASSWORD</div>", unsafe_allow_html=True)
        new_password = st.text_input("pwd_reg", type="password", label_visibility="collapsed", placeholder="Enter Password")
        
        st.markdown("<div class='input-label'>MOBILE NUMBER</div>", unsafe_allow_html=True)
        new_mobile = st.text_input("mob_reg", label_visibility="collapsed", placeholder="Enter Mobile Number")
        
        st.markdown("<div class='input-label'>KDS VERIFICATION CODE</div>", unsafe_allow_html=True)
        kds_info = st.text_input("kds_reg", label_visibility="collapsed", placeholder="Enter KDS Code")
        
        if st.button("REGISTER ACCOUNT →"):
            if new_user_id and new_password and new_mobile:
                st.session_state.users_db[new_user_id] = {
                    "password": new_password,
                    "mobile": new_mobile,
                    "kds": kds_info
                }
                st.success("ACCOUNT CREATED SUCCESSFULLY.")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("FILL ALL REQUIRED FIELDS!")
                
        st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
        if st.button("← BACK TO LOGIN"):
            st.session_state.page = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ----------------- OTP SCREEN -----------------
    elif st.session_state.page == "otp":
        st.markdown("<div class='card-title'>TWO-FACTOR AUTH</div>", unsafe_allow_html=True)
        user = st.session_state.current_user
        mobile = st.session_state.users_db[user]["mobile"]
        
        st.info(f"OTP DISPATCHED TO (*{mobile[-4:]}). [DEMO OTP: 1234]")
        
        st.markdown("<div class='input-label'>ENTER 4-DIGIT OTP</div>", unsafe_allow_html=True)
        otp_input = st.text_input("otp_input", type="password", label_visibility="collapsed", placeholder="1234")
        
        if st.button("VERIFY & LAUNCH →"):
            if otp_input == "1234":
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("INVALID OTP!")

    # ----------------- RECOVERY SCREEN -----------------
    elif st.session_state.page == "forgot":
        st.markdown("<div class='card-title'>SYSTEM RECOVERY</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='input-label'>SELECT RECOVERY MODE</div>", unsafe_allow_html=True)
        option = st.selectbox("rec_mode", ["RESET PASSWORD", "RETRIEVE USER ID", "RETRIEVE MOBILE NUMBER"], label_visibility="collapsed")
        
        if option == "RESET PASSWORD":
            st.markdown("<div class='input-label'>USER ID</div>", unsafe_allow_html=True)
            u_id = st.text_input("r_uid", label_visibility="collapsed", placeholder="Enter User ID")
            st.markdown("<div class='input-label'>KDS CODE</div>", unsafe_allow_html=True)
            kds_in = st.text_input("r_kds", label_visibility="collapsed", placeholder="Enter KDS Code")
            if st.button("EXECUTE RESET →"):
                if u_id in st.session_state.users_db and st.session_state.users_db[u_id]["kds"] == kds_in:
                    st.success(f"PASSWORD: {st.session_state.users_db[u_id]['password']}")
                else:
                    st.error("VERIFICATION FAILED!")
                    
        elif option == "RETRIEVE USER ID":
            st.markdown("<div class='input-label'>MOBILE NUMBER</div>", unsafe_allow_html=True)
            mob = st.text_input("r_mob", label_visibility="collapsed", placeholder="Enter Mobile Number")
            st.markdown("<div class='input-label'>KDS CODE</div>", unsafe_allow_html=True)
            kds_in = st.text_input("r_kds2", label_visibility="collapsed", placeholder="Enter KDS Code")
            if st.button("FETCH USER ID →"):
                found = False
                for uid, data in st.session_state.users_db.items():
                    if data["mobile"] == mob and data["kds"] == kds_in:
                        st.success(f"USER ID: {uid}")
                        found = True
                        break
                if not found:
                    st.error("NO MATCH FOUND!")
                    
        elif option == "RETRIEVE MOBILE NUMBER":
            st.markdown("<div class='input-label'>USER ID</div>", unsafe_allow_html=True)
            u_id = st.text_input("r_uid2", label_visibility="collapsed", placeholder="Enter User ID")
            st.markdown("<div class='input-label'>PASSWORD</div>", unsafe_allow_html=True)
            pwd = st.text_input("r_pwd", type="password", label_visibility="collapsed", placeholder="Enter Password")
            if st.button("FETCH MOBILE →"):
                if u_id in st.session_state.users_db and st.session_state.users_db[u_id]["password"] == pwd:
                    st.success(f"MOBILE: {st.session_state.users_db[u_id]['mobile']}")
                else:
                    st.error("INVALID CREDENTIALS!")

        st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
        if st.button("← RETURN TO LOGIN"):
            st.session_state.page = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ----------------- DASHBOARD -----------------
    elif st.session_state.page == "dashboard":
        st.markdown(f"<div class='card-title'>TERMINAL ACTIVE</div>", unsafe_allow_html=True)
        st.success(f"WELCOME, {st.session_state.current_user.upper()}! ENGINE ONLINE.")
        st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
        if st.button("DISCONNECT / LOGOUT"):
            st.session_state.page = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Footer exactly matching the image
st.markdown("""
    <div class='footer-row'>
        <span>🟢 SYSTEM ONLINE</span>
        <span>ENCRYPTED ACCESS</span>
    </div>
    <div class='footer-copy'>
        KUSHAL PRO MAX © 2026
    </div>
""", unsafe_allow_html=True)
