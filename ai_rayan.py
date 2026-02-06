import streamlit as st
from google import genai # المكتبة الجديدة

# 1. إعدادات الواجهة
st.set_page_config(page_title="مساعد ريان المطور", page_icon="🤖")
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stChatMessage { text-align: right; direction: rtl; }
</style>""", unsafe_allow_html=True)

# 2. الربط بالمفتاح السري
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("المفتاح مفقود من Secrets!")
    st.stop()

# إعداد العميل الجديد (New Client)
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("🤖 مساعد ريان المطور")
st.success("تم التحديث للمكتبة الجديدة 2026 ✅")

# 3. إدارة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. معالجة الشات
if prompt := st.chat_input("اسألني أي شيء..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # مناداة الموديل بالطريقة الجديدة
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt
            )
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"خطأ فني: {str(e)}")
