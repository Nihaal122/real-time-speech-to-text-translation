import streamlit as st
import speech_recognition as sr
from googletrans import Translator

st.set_page_config(page_title="Speech to Text & Translation", layout="centered")

st.title("🎙️ Speech to Text & Translation")
st.write("Click the button, speak clearly, then wait for the result.")

# ---------- Language Selection ----------
input_language = st.selectbox("Spoken Language", ["English", "Hindi"])
translate_to = st.selectbox("Translate To", ["English", "Hindi"])

input_lang_code = "en-IN" if input_language == "English" else "hi-IN"
target_lang_code = "en" if translate_to == "English" else "hi"

# ---------- Initialize ----------
recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.2
translator = Translator()

# ---------- Button ----------
if st.button("🎤 Speak"):
    with st.spinner("Listening... please speak"):
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language=input_lang_code).strip()

        if input_language == translate_to:
            translated = text
        else:
            translated = translator.translate(text, dest=target_lang_code).text

        st.success("✅ Speech Recognized")

        st.subheader("📝 Transcribed Text")
        st.write(text)

        st.subheader("🌍 Translated Text")
        st.write(translated)

    except sr.UnknownValueError:
        st.error("Could not understand speech. Try again.")

    except sr.RequestError:
        st.error("Speech recognition service unavailable.")
