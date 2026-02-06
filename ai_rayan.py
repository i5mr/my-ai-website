import streamlit as st
import google.generativeai as genai

# 1. إعدادات المظهر (UI) لدعم العربي واليمين لليسار
st.set_page_config(page_title="مساعد ريان الذكي", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stChatMessage { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

# 2. ربط المفتاح السري (هنا حل مشكلة الصورة 9)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("خطأ: لم يتم العثور على GOOGLE_API_KEY في إعدادات Secrets!")
    st.stop()

# 3. إعداد الموديل مع "شخصية" قوية
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction="أنت مساعد ذكي جداً، خبير في البرمجة، وتتحدث بالعربية بأسلوب ممتع وواضح."
)

# 4. ذاكرة المحادثة
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

st.title("🤖 مساعد ريان المطور")
st.write("أهلاً بك! أنا نسختك الخاصة من الذكاء الاصطناعي، كيف أساعدك اليوم؟")

# عرض الرسائل السابقة
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# صندوق الشات
if prompt := st.chat_input("اسألني أي شيء..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        # إرسال الرسالة مع التحديث المباشر (Streaming)
        response = st.session_state.chat.send_message(prompt, stream=True)
        for chunk in response:
            full_response += chunk.text
            response_placeholder.markdown(full_response + "▌")
        response_placeholder.markdown(full_response)