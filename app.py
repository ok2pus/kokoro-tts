import io
import streamlit as st
import soundfile as sf
from kokoro import KPipeline

st.set_page_config(page_title="Kokoro TTS", page_icon="🔊")
st.title("🔊 Kokoro Text-to-Speech")

# Cache the pipeline so it's loaded once, not on every click
@st.cache_resource
def get_pipeline():
    return KPipeline(lang_code='a')

VOICES = [
    "af_heart", "af_bella", "af_nicole", "af_nova", "af_sarah",
    "af_sky", "af_river", "af_jessica", "af_kore", "af_aoede",
    "am_michael", "am_puck", "am_fenrir", "am_onyx", "am_adam",
    "am_echo", "am_eric", "am_liam",
]

col1, col2 = st.columns([2, 1])
with col1:
    voice = st.selectbox("Voice", VOICES, index=0)
with col2:
    speed = st.slider("Speed", 0.5, 2.0, 1.0, 0.1)

text = st.text_area(
    "Text to speak",
    value="Hello! This is your locally-hosted text to speech engine.",
    height=150,
)

if st.button("Generate speech", type="primary"):
    if not text.strip():
        st.warning("Enter some text first.")
    else:
        with st.spinner("Generating... (first run downloads the model)"):
            pipeline = get_pipeline()
            generator = pipeline(text, voice=voice, speed=speed)
            chunks = [audio for _, _, audio in generator]

            if chunks:
                import numpy as np
                audio = np.concatenate(chunks)
                buf = io.BytesIO()
                sf.write(buf, audio, 24000, format="WAV")
                st.audio(buf.getvalue(), format="audio/wav")
                st.download_button(
                    "Download WAV",
                    data=buf.getvalue(),
                    file_name=f"{voice}_output.wav",
                    mime="audio/wav",
                )
            else:
                st.error("No audio generated.")