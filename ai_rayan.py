import streamlit as st
import google.generativeai as genai

# 1. إعدادات الواجهة (دعم كامل للعربي)
st.set_page_config(page_title="مساعد ريان المطور", page_icon="🤖")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stChatMessage { text-align: right; direction: rtl; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. جلب المفتاح السري
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ خطأ: المفتاح السري غير مفعّل في Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. اختيار الموديل (تغيير الصيغة لحل مشكلة 404 في الصورة 16)
# جربنا كل الأسماء، الحين بنستخدم الصيغة الأكثر قبولاً للسيرفرات
@st.cache_resource
def load_model():
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="أنت مساعد ذكي اسمك 'مساعد ريان' تخدم المستخدم بكل مهارة وباللغة العربية."
    )

model = load_model()

# 4. ذاكرة المحادثة
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

st.title("🤖 مساعد ريان المطور")
st.caption("النسخة النهائية المستقرة 100%")

# عرض المحادثة السابقة
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 5. إرسال الرسالة والرد المباشر
if prompt := st.chat_input("تفضل، اسألني أي شيء..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        try:
            # استخدام نظام البث (Streaming)
            response = st.session_state.chat.send_message(prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"حدث خطأ في الاتصال: {str(e)}")
            st.info("نصيحة: تأكد من تحديث ملف requirements.txt ليتضمن أحدث إصدار.")
