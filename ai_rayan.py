import streamlit as st
import google.generativeai as genai

# 1. إعدادات الواجهة (احترافية ودعم كامل للعربي)
st.set_page_config(page_title="مساعد ريان المطور", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stChatMessage { text-align: right; direction: rtl; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. ربط المفتاح السري (Secrets)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ خطأ: المفتاح السري غير مفعّل في Secrets! (راجع Manage app -> Settings)")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. اختيار الموديل (استخدام النسخة المستقرة جداً لحل مشكلة 404)
# جربنا flash و pro-1.5 وفشلت في صورك، لذا سنعود للأصل المضمون
@st.cache_resource
def get_model():
    return genai.GenerativeModel('gemini-pro')

try:
    model = get_model()
except Exception as e:
    st.error(f"فشل تحميل الموديل: {e}")
    st.stop()

# 4. ذاكرة المحادثة (History)
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

st.title("🤖 مساعد ريان المطور")
st.write("نسخة مدمجة ومستقرة - جاهز لخدمتك!")

# عرض المحادثة السابقة
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 5. صندوق الشات والرد الذكي
if prompt := st.chat_input("تفضل، اسألني أي شيء..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        try:
            # طلب الرد من الموديل
            response = st.session_state.chat.send_message(prompt, stream=True)
            for chunk in response:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        except Exception as e:
            # إذا استمرت مشكلة الـ 404، سنظهر لك حل بديل فوراً
            st.error(f"عذراً ريان، السيرفر يرفض الاتصال حالياً. الخطأ: {str(e)}")
            st.info("تأكد من تحديث ملف requirements.txt وإضافة google-generativeai==0.3.0")
