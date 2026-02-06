import streamlit as st
import google.generativeai as genai

# 1. إعدادات الواجهة (دعم كامل للغة العربية)
st.set_page_config(page_title="مساعد ريان المطور", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stChatMessage { text-align: right; direction: rtl; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. ربط المفتاح السري (Secrets)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ خطأ: المفتاح السري غير مفعّل في Secrets!")
    st.stop()

# 3. اختيار الموديل المستقر (حل مشكلة 404 في صورة 12)
# سنستخدم اسم الموديل التقليدي لضمان التوافق مع كل السيرفرات
model = genai.GenerativeModel('gemini-pro') 

# 4. الذاكرة
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

st.title("🤖 مساعد ريان المطور")
st.caption("النسخة النهائية المستقرة")

# عرض المحادثة
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 5. معالجة الرسائل والرد المباشر
if prompt := st.chat_input("اسألني أي شيء..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        try:
            # استخدام نظام الـ Streaming لرد سريع
            response = st.session_state.chat.send_message(prompt, stream=True)
            for chunk in response:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"حدث خطأ تقني: {str(e)}")
