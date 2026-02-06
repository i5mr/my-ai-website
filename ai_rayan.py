import streamlit as st
from google import genai

# 1. إعدادات الواجهة المتوافقة مع 1.54
st.set_page_config(page_title="مساعد ريان المطور", page_icon="🤖")

st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stChatMessage { text-align: right; direction: rtl; }
</style>""", unsafe_allow_html=True)

# 2. الربط بالمفتاح
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("المفتاح مفقود من Secrets!")
    st.stop()

# إعداد العميل (Client) بأحدث طريقة لعام 2026
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("🤖 مساعد ريان المطور")
st.info("نظام متصل ومستقر - إصدار 2026")

# 3. الذاكرة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# عرض المحادثة
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# 4. معالجة الشات (بدون v1beta لضمان عدم حدوث 404)
if prompt := st.chat_input("تفضل اسألني..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # استخدام موديل flash السريع والمستقر
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt
            )
            st.markdown(response.text)
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # إذا تعذر، نحاول الموديل الاحتياطي فوراً
            try:
                response = client.models.generate_content(model="gemini-pro", contents=prompt)
                st.markdown(response.text)
            except:
                st.error("السيرفر يرفض الاتصال، جرب تضغط Reboot App من الـ Logs")
