import streamlit as st
from languages import LANGUAGES
from langdetect import detect, LangDetectException
from gtts import gTTS
from langchain.schema import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from tempfile import NamedTemporaryFile

# Set up Streamlit page
st.set_page_config(page_title="EchoLango", page_icon="🌍", layout="wide")

# Custom CSS for dark-themed styling with updated fields
st.markdown("""
<style>
    body {
        background-color: #1a1a2e;
    }
    .main-container {
        background-color: #2a2a3e;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        max-width: 1000px;
        margin: auto;
        margin-top: 20px;
    }
    h1 {
        color: #4ecca3;
        font-family: 'Poppins', sans-serif;
        text-align: center;
        font-size: 2.8rem;
        margin-bottom: 8px;
    }
    h4 {
        color: #a3a3c2;
        font-family: 'Poppins', sans-serif;
        text-align: center;
        font-weight: 400;
        margin-bottom: 25px;
    }
    .stTextArea textarea {
        background-color: #3a3a4e;
        border: 1px solid #4a4a6e;
        border-radius: 8px;
        padding: 12px;
        font-size: 1rem;
        font-family: 'Inter', sans-serif;
        color: #e6e6fa;
        transition: border-color 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #4ecca3;
        outline: none;
        box-shadow: 0 0 0 3px rgba(78, 204, 163, 0.2);
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #3a3a4e;
        border: 1px solid #4a4a6e;
        border-radius: 8px;
        padding: 8px;
        font-size: 1rem;
        font-family: 'Inter', sans-serif;
        color: #e6e6fa;
    }
    .stSelectbox div[data-baseweb="select"] > div > div {
        color: #e6e6fa;
    }
    .stButton button {
        background-color: #4ecca3;
        color: #1a1a2e;
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 1rem;
        font-family: 'Inter', sans-serif;
        border: none;
        transition: background-color 0.3s ease, transform 0.1s ease;
    }
    .stButton button:hover {
        background-color: #3db992;
        transform: translateY(-1px);
    }
    .stButton button:active {
        transform: translateY(0);
    }
    .stSpinner {
        color: #4ecca3;
    }
    .audio-button {
        background-color: transparent;
        color: #e6e6fa;
        border: 1px solid #4a4a6e;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 1rem;
        font-family: 'Inter', sans-serif;
        transition: border-color 0.3s ease, color 0.3s ease;
    }
    .audio-button:hover {
        border-color: #4ecca3;
        color: #4ecca3;
    }
    .footer {
        text-align: center;
        color: #a3a3c2;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        margin-top: 30px;
    }
    .divider {
        border-top: 1px solid #4a4a6e;
        margin: 25px 0;
    }
    .language-label {
        margin-top:3px;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #a3a3c2;
        margin-bottom: 1px;
    }
    .translated-label {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #4ecca3;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
    }
    .translated-label::before {
        content: "✔";
        margin-right: 8px;
        color: #4ecca3;
    }
    .stWarning div {
        background-color: #ff6b6b !important;
        color: #1a1a2e !important;
    }
</style>
""", unsafe_allow_html=True)

# Main container
with st.container():
    
    # Title & Subtitle
    st.markdown("<h1>🌍 EchoLango</h1>", unsafe_allow_html=True)
    st.markdown("<h4>AI-powered translation in your language 🚀</h4>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Initialize Llama 3 via Groq
    chat = ChatGroq(
        temperature=0.7,
        model_name="llama3-70b-8192",
        groq_api_key="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"  # replace with your actual key
    )

    # Function to translate
    def query_llama3(text, source_lang, target_lang):
        system_prompt = f"""
        You are a professional translator called 'EchoLango'.
        Translate only the given text from {source_lang} to {target_lang}.
        Maintain natural fluency and cultural accuracy.
        Return only the translated text.
        """
        messages = [
            SystemMessage(content=system_prompt.strip()),
            HumanMessage(content=f"Translate: {text}")
        ]
        response = chat.invoke(messages)
        return response.content

    # Function to convert text to audio
    def text_to_audio(text, lang="en"):
        try:
            tts = gTTS(text=text, lang=lang)
            with NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                tts.write_to_fp(f)
                return f.name
        except Exception as e:
            st.error(f"Audio error: {e}")
            return None

    # Language selectors with labels
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='language-label'>🔤 Source Language</div>", unsafe_allow_html=True)
        source_lang = st.selectbox("Source Language", LANGUAGES.keys(), index=0, key="source_lang")
    with col2:
        st.markdown("<div class='language-label'>🌍 Target Language</div>", unsafe_allow_html=True)
        target_lang = st.selectbox("Target Language", LANGUAGES.keys(), index=1, key="target_lang")

    # Session state defaults
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""
    if "translated" not in st.session_state:
        st.session_state.translated = ""

    # Input text area
    st.markdown("<div class='language-label'>✍️ Enter text to translate:</div>", unsafe_allow_html=True)
    st.session_state.input_text = st.text_area("", value=st.session_state.input_text, height=120, key="input_text_area")

    # Translate button
    if st.button("🔁 Translate"):
        if st.session_state.input_text.strip():
            with st.spinner("Translating..."):
                st.session_state.translated = query_llama3(
                    st.session_state.input_text,
                    source_lang,
                    target_lang
                )
        else:
            st.warning("⚠️ Please enter text to translate.")

    # Output box with updated label
    if st.session_state.translated:
        st.markdown("<div class='translated-label'>Translated Text</div>", unsafe_allow_html=True)
        st.text_area("", value=st.session_state.translated, height=120, key="translated_text")

    # Audio buttons with updated styling
    audio_col1, audio_col2 = st.columns(2)
    with audio_col1:
        if st.session_state.input_text:
            if st.button("🔊 Listen to Input Text", key="input_audio", help="Listen to the input text in the source language"):
                audio_path = text_to_audio(st.session_state.input_text, LANGUAGES[source_lang])
                if audio_path:
                    with open(audio_path, 'rb') as audio_file:
                        audio_bytes = audio_file.read()
                        st.audio(audio_bytes, format='audio/mp3')

    with audio_col2:
        if st.session_state.translated:
            if st.button("🔊 Listen to Translated Text", key="translated_audio", help="Listen to the translated text in the target language"):
                audio_path = text_to_audio(st.session_state.translated, LANGUAGES[target_lang])
                if audio_path:
                    with open(audio_path, 'rb') as audio_file:
                        audio_bytes = audio_file.read()
                        st.audio(audio_bytes, format='audio/mp3')

    # Footer
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<p class='footer'>Made by <strong>Utkarsh Patil</strong></p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)