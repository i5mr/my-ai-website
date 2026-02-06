import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والجماليات (دعم كامل للعربي)
st.set_page_config(page_title="مساعد ريان المطور", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stChatMessage { text-align: right; direction: rtl; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. التحقق من المفتاح السري (Secrets)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("⚠️ خطأ: المفتاح السري غير موجود في إعدادات Secrets!")
    st.stop()

# 3. اختيار الموديل المستقر (هذا الجزء يحل مشكلة NotFound في الصورة الأخيرة)
# سنستخدم 'gemini-1.5-flash' أو 'gemini-pro' لضمان التوافق
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", 
        system_instruction="أنت مساعد ذكي جداً اسمك 'مساعد ريان'، خبير في البرمجة وتساعد الناس بذكاء."
    )
except Exception:
    # حل احتياطي في حال فشل الموديل المذكور
    model = genai.GenerativeModel(model_name="gemini-pro")

# 4. الذاكرة
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

st.title("🤖 مساعد ريان المطور")
st.caption("النسخة المدمجة والمستقرة")

# عرض المحادثة
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 5. معالجة الرسائل
if prompt := st.chat_input("تفضل، اسألني أي شيء..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        try:
            # طلب الرد
            response = st.session_state.chat.send_message(prompt, stream=True)
            for chunk in response:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"حدث خطأ في الاتصال بالموديل: {str(e)}")
