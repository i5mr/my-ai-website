import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والجماليات (ثبات كامل للغة العربية)
st.set_page_config(page_title="مساعد ريان المطور", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { 
        font-family: 'Cairo', sans-serif; 
        direction: rtl; 
        text-align: right; 
    }
    .stChatMessage { text-align: right; direction: rtl; border-radius: 15px; }
    /* إصلاح مكان أيقونات البوت والمستخدم */
    .stChatMessage [data-testid="stChatMessageAvatarUser"] { order: 1; }
    .stChatMessage [data-testid="stChatMessageAvatarAssistant"] { order: 1; }
    </style>
    """, unsafe_allow_html=True)

# 2. جلب المفتاح السري (Secrets)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ خطأ: المفتاح السري GOOGLE_API_KEY غير مفعّل في إعدادات Secrets.")
    st.stop()

# 3. دالة لاختيار الموديل المتاح (لحل مشكلة 404 في الصورة الأخيرة)
@st.cache_resource
def load_model():
    # نحاول أولاً تشغيل النسخة السريعة والمستقرة
    try:
        return genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="أنت مساعد ذكي جداً اسمك 'مساعد ريان'، خبير في البرمجة وتتحدث بأسلوب ودي."
        )
    except:
        # إذا فشلت، نستخدم النسخة التقليدية
        return genai.GenerativeModel(model_name="gemini-pro")

model = load_model()

# 4. ذاكرة المحادثة المستمرة
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

st.title("🤖 مساعد ريان المطور")
st.write("نسخة مدمجة وخالية من الأخطاء بإذن الله.")

# عرض الرسائل السابقة
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
            # إرسال الرسالة مع تفعيل خاصية الـ Streaming
            response = st.session_state.chat.send_message(prompt, stream=True)
            for chunk in response:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"حدث خطأ تقني: {str(e)}")
            st.info("نصيحة: تأكد من أن مفتاح الـ API صحيح وله صلاحية الوصول لموديلات Gemini.")
