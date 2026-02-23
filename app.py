import streamlit as st
from chatbot import get_response
import speech_recognition as sr
from googletrans import Translator

# ---------- CONFIG ----------
st.set_page_config(page_title="Farmer Chatbot", page_icon="🌾", layout="wide")

# ---------- SESSION STATE FOR CHAT ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- SIDEBAR ----------
st.sidebar.title("⚙️ Settings")

language = st.sidebar.selectbox("🌍 Select Output Language", ["English", "Telugu"])
use_voice = st.sidebar.checkbox("🎤 Enable Voice Input")

st.sidebar.markdown("---")
st.sidebar.info("📚 Dataset answers | 🤖 AI answers")

# ---------- HEADER ----------
st.title("🌾 Smart Farmer Assistant")
st.caption("Helping farmers with crop advice, pests, soil, weather & more")

translator = Translator()

# ---------- TRANSLATION ----------
def translate_text(text, dest_lang):
    if not text or text.strip() == "":
        return text  # return as-is if empty

    try:
        return translator.translate(text, dest=dest_lang).text
    except Exception:
        return text  # fallback if translation fails
        
# ---------- VOICE INPUT ----------
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio)
    except:
        st.error("Voice not recognized")
        return ""

# ---------- INPUT ----------
query = st.text_input("💬 Ask your farming question")

if use_voice and st.button("🎤 Speak"):
    query = get_voice_input()
    st.success(f"You said: {query}")

# ---------- PROCESS ----------
if st.button("Send") and query:
    user_query = query

    # Translate Telugu → English
    if language == "Telugu":
        user_query = translate_text(query, "en")

    response = get_response(user_query)

    # Translate back to Telugu
    if language == "Telugu":
        response = translate_text(response, "te")

    # Save chat
    st.session_state.chat_history.append(("user", query))
    st.session_state.chat_history.append(("bot", response))

# ---------- DISPLAY CHAT ----------
st.markdown("### 🗨️ Conversation")

for role, message in st.session_state.chat_history:
    if role == "user":
        st.markdown(
            f"""
            <div style='background-color:#e6f7ff;color:black;padding:12px;border-radius:10px;margin-bottom:8px'>
            👨‍🌾 <b>You:</b> {message}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Badge detection
        badge = "📚" if message.startswith("📚") else "🤖"

        st.markdown(
            f"""
            <div style='background-color:#f0ffe6;color:black;padding:12px;border-radius:10px;margin-bottom:12px'>
            {badge} <b>Assistant:</b> {message.replace("📚","").replace("🤖","")}
            </div>
            """,
            unsafe_allow_html=True
        )