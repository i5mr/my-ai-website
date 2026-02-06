import streamlit as st
import google.generativeai as genai

# إعدادات الواجهة
st.set_page_config(page_title="مساعد ريان المطور", page_icon="🤖")

# دعم العربية
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stChatMessage { text-align: right; direction: rtl; }
</style>""", unsafe_allow_html=True)

# الربط بالمفتاح
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("المفتاح مفقود من Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# حل مشكلة 404: نحدد الموديل المباشر
model = genai.GenerativeModel('gemini-1.5-flash')

# ذاكرة المحادثة
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

st.title("🤖 مساعد ريان المطور")
st.success("تم تحديث النظام.. جرب الآن!")

# عرض الشات
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# إرسال الرسالة
if prompt := st.chat_input("تفضل اسألني..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # استخدام الموديل مباشرة بدون تحديد النسخة في الرابط
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"الخطأ لسه موجود: {str(e)}")
            st.info("إذا طلع خطأ، سوّ Reboot للموقع من Manage App")
