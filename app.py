import streamlit as st

# ১. পেজ সেটআপ ও প্রো-লেভেল থিম
st.set_page_config(
    page_title="Kushal Pro Max Trading",
    page_icon="📈",
    layout="centered"
)

# ৯০% ডার্ক এবং লাইট গ্রিন কাস্টম লুক (CSS)
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #00FF66;
    }
    .main-title {
        text-align: center;
        color: #00FF66;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .sub-text {
        text-align: center;
        color: #A0A0A0;
        margin-bottom: 30px;
    }
    div.stButton > button:first-child {
        background-color: #00FF66;
        color: #000000;
        font-weight: bold;
        border: none;
        width: 100%;
        border-radius: 5px;
        padding: 10px;
    }
    div.stButton > button:first-child:hover {
        background-color: #00CC52;
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# ২. সেসনের মেমোরি স্টেট সেটআপ
if "page" not in st.session_state:
    st.session_state.page = "login"
if "users_db" not in st.session_state:
    st.session_state.users_db = {} # ইউজার ডাটা লোকাল সেসনে থাকবে

# ৩. হেডিং
st.markdown("<div class='main-title'>ওয়েলকাম কুশল প্রো ম্যাক্স ট্রেডিং</div>", unsafe_allow_html=True)

# ----------------- নতুন একাউন্ট খোলার স্ক্রিন (Registration) -----------------
if st.session_state.page == "register":
    st.subheader("📝 নতুন অ্যাকাউন্ট তৈরি করুন")
    
    new_user_id = st.text_input("ইউজার আইডি (User ID)")
    new_password = st.text_input("পাসওয়ার্ড (Password)", type="password")
    new_mobile = st.text_input("মোবাইল নম্বর (Mobile Number)")
    kds_info = st.text_input("KDS তথ্য (Verification Info)")
    
    if st.button("রেজিস্টার করুন"):
        if new_user_id and new_password and new_mobile:
            st.session_state.users_db[new_user_id] = {
                "password": new_password,
                "mobile": new_mobile,
                "kds": kds_info
            }
            st.success("✅ অ্যাকাউন্ট সফলভাবে তৈরি হয়েছে! এখন লগইন করুন।")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error("❌ সব তথ্য সঠিকভাবে দিন!")
            
    if st.button("⬅️ লগইন পেজে ফিরে যান"):
        st.session_state.page = "login"
        st.rerun()

# ----------------- লগইন স্ক্রিন (Login Screen) -----------------
elif st.session_state.page == "login":
    st.markdown("<div class='sub-text'>অ্যালগরিদম ড্যাশবোর্ডে প্রবেশ করতে সিকিউর লগইন করুন</div>", unsafe_allow_html=True)
    
    user_id = st.text_input("ইউজার আইডি (User ID)")
    password = st.text_input("পাসওয়ার্ড (Password)", type="password")
    
    if st.button("লগইন করুন (Login)"):
        if user_id in st.session_state.users_db and st.session_state.users_db[user_id]["password"] == password:
            st.session_state.page = "otp"
            st.session_state.current_user = user_id
            st.rerun()
        else:
            st.error("❌ ভুল ইউজার আইডি অথবা পাসওয়ার্ড!")
            
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Create New Account"):
            st.session_state.page = "register"
            st.rerun()
    with col2:
        if st.button("🔑 Forgot Credentials"):
            st.session_state.page = "forgot"
            st.rerun()

# ----------------- ওটিপি স্ক্রিন (OTP Screen) -----------------
elif st.session_state.page == "otp":
    st.subheader("🔒 ওটিপি ভেরিফিকেশন (OTP Verification)")
    user = st.session_state.current_user
    mobile = st.session_state.users_db[user]["mobile"]
    
    st.info(f"আপনার নিবন্ধিত নম্বর ({mobile[-4:]})-এ ওটিপি পাঠানো হয়েছে। (Demo OTP: 1234)")
    otp_input = st.text_input("4-Digit OTP দিন", type="password")
    
    if st.button("ভেরিফাই ও প্রবেশ করুন"):
        if otp_input == "1234":
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("❌ ভুল ওটিপি (OTP)!")

# ----------------- পাসওয়ার্ড/আইডি উদ্ধার (Forgot Options) -----------------
elif st.session_state.page == "forgot":
    st.subheader("⚙️ তথ্য পুনরুদ্ধার (Recovery Option)")
    option = st.radio("কী উদ্ধার করতে চান?", ["পাসওয়ার্ড ভুলে গেছি", "ইউজার আইডি ভুলে গেছি", "মোবাইল নম্বর ভুলে গেছি"])
    
    if option == "পাসওয়ার্ড ভুলে গেছি":
        u_id = st.text_input("ইউজার আইডি দিন")
        kds_in = st.text_input("KDS ভেরিফিকেশন দিন")
        if st.button("পাসওয়ার্ড রিসেট"):
            if u_id in st.session_state.users_db and st.session_state.users_db[u_id]["kds"] == kds_in:
                st.success(f"আপনার পাসওয়ার্ড হলো: {st.session_state.users_db[u_id]['password']}")
            else:
                st.error("❌ তথ্য মিলছে না!")
                
    elif option == "ইউজার আইডি ভুলে গেছি":
        mob = st.text_input("মোবাইল নম্বর দিন")
        kds_in = st.text_input("KDS ভেরিফিকেশন দিন")
        if st.button("আইডি খুঁজুন"):
            found = False
            for uid, data in st.session_state.users_db.items():
                if data["mobile"] == mob and data["kds"] == kds_in:
                    st.success(f"আপনার ইউজার আইডি হলো: {uid}")
                    found = True
                    break
            if not found:
                st.error("❌ তথ্য মিলছে না!")
                
    elif option == "মোবাইল নম্বর ভুলে গেছি":
        u_id = st.text_input("ইউজার আইডি দিন")
        pwd = st.text_input("পাসওয়ার্ড দিন", type="password")
        if st.button("নম্বর দেখুন"):
            if u_id in st.session_state.users_db and st.session_state.users_db[u_id]["password"] == pwd:
                st.success(f"আপনার নিবন্ধিত নম্বর: {st.session_state.users_db[u_id]['mobile']}")
            else:
                st.error("❌ পাসওয়ার্ড ও ইউজার আইডি দুটোই সঠিক হতে হবে!")

    if st.button("⬅️ প্রধান পেজে ফিরে যান"):
        st.session_state.page = "login"
        st.rerun()

# ----------------- আসল ড্যাশবোর্ড (Dashboard) -----------------
elif st.session_state.page == "dashboard":
    st.success(f"🎉 স্বাগতম {st.session_state.current_user}! কুশল প্রো ম্যাক্স ইঞ্জিন সক্রিয় রয়েছে।")
    if st.button("Logout"):
        st.session_state.page = "login"
        st.rerun()
