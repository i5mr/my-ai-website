import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والهوية
st.set_page_config(page_title="جمناي المطور - نسختك الخاصة", page_icon="🤖", layout="centered")

# 2. لمسة جمالية (CSS) عشان يصير الموقع فخم
st.markdown("""
    <style>
    /* تغيير الخط وتنسيق الاتجاه للعربي */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }

    /* تنسيق فقاعات الدردشة */
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
        padding: 10px;
    }
    
    /* إخفاء القوائم غير الضرورية لشكل أنظف */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. ربط الذكاء الاصطناعي
genai.configurevst.secrets["GOOGLE_API_KEY"]
model = genai.GenerativeModel('gemini-1.5-pro')

# 4. الذاكرة والرمز السري
if "messages" not in st.session_state:
    st.session_state.messages = []
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# واجهة الدخول (الرمز السري)
if not st.session_state.authenticated:
    st.title("🔒 منطقة خاصة")
    code = st.text_input("أدخل رمز الدخول للموقع:", type="password")
    if code == "1234": # غير الرمز من هنا
        st.session_state.authenticated = True
        st.rerun()
    st.stop()

# 5. واجهة المحادثة الرئيسية
st.title("🤖 جمناي المطور")
st.caption("مساعدك الذكي في البرمجة والذكاء الاصطناعي")

# عرض رسائل الدردشة من الذاكرة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# صندوق الكتابة (مثل المواقع الاحترافية)
if prompt := st.chat_input("بماذا يمكنني مساعدتك اليوم؟"):
    # أضف رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # رد الذكاء الاصطناعي
    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير..."):
            response = model.generate_content(prompt)
            full_response = response.text
            st.markdown(full_response)
    
    # حفظ رد البوت في الذاكرة
    st.session_state.messages.append({"role": "assistant", "content": full_response})