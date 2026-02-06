import streamlit as st
import google.generativeai as genai

# 1. إعدادات المظهر (UI) لدعم العربي واليمين لليسار بشكل احترافي
st.set_page_config(page_title="مساعد ريان المطور", page_icon="🤖", layout="centered")

# تنسيق الواجهة لتكون مريحة للعين وتدعم العربية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stChatMessage { text-align: right; direction: rtl; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. ربط المفتاح السري من إعدادات Streamlit (حل مشكلة KeyError)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("⚠️ خطأ: تأكد من إضافة GOOGLE_API_KEY في إعدادات Secrets في موقع Streamlit.")
    st.stop()

# 3. إعداد الموديل مع الاسم الصحيح (حل مشكلة NotFound)
# أضفنا "models/" قبل اسم الموديل لضمان استقراره أونلاين
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-pro", 
    system_instruction="أنت مساعد ذكي جداً اسمك 'مساعد ريان'، خبير في البرمجة، وتتحدث بالعربية بأسلوب ممتع وواضح."
)

# 4. إدارة ذاكرة المحادثة (History)
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

st.title("🤖 مساعد ريان المطور")
st.write("أهلاً بك في نسختك الخاصة! أنا جاهز للإجابة على أي سؤال.")

# عرض الرسائل السابقة من الذاكرة
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 5. صندوق الشات ومعالجة الردود
if prompt := st.chat_input("اسألني أي شيء..."):
    # عرض رسالة المستخدم فوراً
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # طلب الرد من الذكاء الاصطناعي مع خاصية التحديث المباشر
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        try:
            response = st.session_state.chat.send_message(prompt, stream=True)
            for chunk in response:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال: {str(e)}")
