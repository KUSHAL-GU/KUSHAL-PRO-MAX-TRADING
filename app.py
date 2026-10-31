import streamlit as st

# 1. Page Configuration & Futuristic Theme Setup
st.set_page_config(
    page_title="Kushal Pro Max Trading",
    page_icon="⚡",
    layout="centered"
)

# Premium Dark Matrix-Green Theme & Futuristic Cyberpunk Style (CSS)
st.markdown("""
    <style>
    .stApp {
        background-color: #030d08;
        color: #00FF66;
        font-family: 'Courier New', Courier, monospace;
    }
    .main-title {
        text-align: center;
        color: #00FF66;
        font-size: 30px;
        font-weight: 900;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(0, 255, 102, 0.5);
        margin-bottom: 5px;
    }
    .sub-text {
        text-align: center;
        color: #00CC52;
        font-size: 13px;
        letter-spacing: 1px;
        margin-bottom: 30px;
    }
    div.stButton > button:first-child {
        background-color: #00FF66;
        color: #030d08;
        font-weight: bold;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 1px;
        border: none;
        width: 100%;
        border-radius: 4px;
        padding: 10px;
        box-shadow: 0 0 10px rgba(0, 255, 102, 0.3);
    }
    div.stButton > button:first-child:hover {
        background-color: #00CC52;
        color: #000000;
        box-shadow: 0 0 15px rgba(0, 255, 102, 0.6);
    }
    input {
        background-color: #051a0f !important;
        color: #00FF66 !important;
        border: 1px solid #00FF66 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Session State Initialization
if "page" not in st.session_state:
    st.session_state.page = "login"
if "users_db" not in st.session_state:
    st.session_state.users_db = {}

# 3. Main Header & Sub-header (100% English & Futuristic)
st.markdown("<div class='main-title'>KUSHAL PRO MAX TRADING</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>// SECURE ALGO-TRADING & EXECUTION TERMINAL //</div>", unsafe_allow_html=True)

# ----------------- REGISTRATION SCREEN -----------------
if st.session_state.page == "register":
    st.subheader("⚙️ INITIALIZE NEW ACCOUNT")
    
    new_user_id = st.text_input("ENTER USER ID")
    new_password = st.text_input("ENTER PASSWORD", type="password")
    new_mobile = st.text_input("MOBILE NUMBER")
    kds_info = st.text_input("KDS VERIFICATION CODE")
    
    if st.button("REGISTER ACCOUNT"):
        if new_user_id and new_password and new_mobile:
            st.session_state.users_db[new_user_id] = {
                "password": new_password,
                "mobile": new_mobile,
                "kds": kds_info
            }
            st.success("✅ ACCOUNT CREATED SUCCESSFULLY. PROCEED TO LOGIN.")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error("❌ ERROR: FILL ALL REQUIRED FIELDS!")
            
    if st.button("<< BACK TO LOGIN"):
        st.session_state.page = "login"
        st.rerun()

# ----------------- LOGIN SCREEN -----------------
elif st.session_state.page == "login":
    st.markdown("<div class='sub-text'>AUTHENTICATION GATEWAY REQUIRED</div>", unsafe_allow_html=True)
    
    user_id = st.text_input("USER ID")
    password = st.text_input("PASSWORD", type="password")
    
    if st.button("SECURE LOGIN"):
        if user_id in st.session_state.users_db and st.session_state.users_db[user_id]["password"] == password:
            st.session_state.page = "otp"
            st.session_state.current_user = user_id
            st.rerun()
        else:
            st.error("❌ ACCESS DENIED: INVALID CREDENTIALS!")
            
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("CREATE ACCOUNT"):
            st.session_state.page = "register"
            st.rerun()
    with col2:
        if st.button("RECOVERY PROTOCOL"):
            st.session_state.page = "forgot"
            st.rerun()

# ----------------- OTP SCREEN -----------------
elif st.session_state.page == "otp":
    st.subheader("🔐 TWO-FACTOR AUTHENTICATION (2FA)")
    user = st.session_state.current_user
    mobile = st.session_state.users_db[user]["mobile"]
    
    st.info(f"OTP DISPATCHED TO MOBILE ENDPOINT (*{mobile[-4:]}). [DEMO OTP: 1234]")
    otp_input = st.text_input("ENTER 4-DIGIT OTP", type="password")
    
    if st.button("VERIFY & LAUNCH TERMINAL"):
        if otp_input == "1234":
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("❌ AUTHENTICATION FAILED: INVALID OTP!")

# ----------------- RECOVERY SCREEN -----------------
elif st.session_state.page == "forgot":
    st.subheader("🛠️ SYSTEM RECOVERY PROTOCOL")
    option = st.selectbox("SELECT RECOVERY MODE", ["RESET PASSWORD", "RETRIEVE USER ID", "RETRIEVE MOBILE NUMBER"])
    
    if option == "RESET PASSWORD":
        u_id = st.text_input("ENTER USER ID")
        kds_in = st.text_input("ENTER KDS CODE")
        if st.button("EXECUTE PASSWORD RESET"):
            if u_id in st.session_state.users_db and st.session_state.users_db[u_id]["kds"] == kds_in:
                st.success(f"PASSWORD RETRIEVED: {st.session_state.users_db[u_id]['password']}")
            else:
                st.error("❌ VERIFICATION FAILED!")
                
    elif option == "RETRIEVE USER ID":
        mob = st.text_input("ENTER MOBILE NUMBER")
        kds_in = st.text_input("ENTER KDS CODE")
        if st.button("FETCH USER ID"):
            found = False
            for uid, data in st.session_state.users_db.items():
                if data["mobile"] == mob and data["kds"] == kds_in:
                    st.success(f"USER ID FOUND: {uid}")
                    found = True
                    break
            if not found:
                st.error("❌ NO MATCHING RECORD FOUND!")
                
    elif option == "RETRIEVE MOBILE NUMBER":
        u_id = st.text_input("ENTER USER ID")
        pwd = st.text_input("ENTER PASSWORD", type="password")
        if st.button("FETCH MOBILE ENDPOINT"):
            if u_id in st.session_state.users_db and st.session_state.users_db[u_id]["password"] == pwd:
                st.success(f"REGISTERED MOBILE: {st.session_state.users_db[u_id]['mobile']}")
            else:
                st.error("❌ INVALID USER ID OR PASSWORD!")

    if st.button("<< RETURN TO LOGIN"):
        st.session_state.page = "login"
        st.rerun()

# ----------------- DASHBOARD -----------------
elif st.session_state.page == "dashboard":
    st.success(f"🚀 TERMINAL ACTIVE: WELCOME, {st.session_state.current_user.upper()}! KUSHAL PRO MAX ENGINE ONLINE.")
    if st.button("DISCONNECT / LOGOUT"):
        st.session_state.page = "login"
        st.rerun()
