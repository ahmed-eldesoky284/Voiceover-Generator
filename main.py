from gtts import gTTS
import io
import streamlit as st
import numpy as np
import pygame

def generate_voiceover(text, voice_gender='female', speed=1.0, pitch=1.0, lang='en', volume=0.5):
    # Specify language
    lang = lang if lang else 'en'

    # Specify gender
    gender = 'female' if voice_gender == 'female' else 'male'

    # Initialize gTTS
    tts = gTTS(text=text, lang=lang, slow=False if speed > 1.0 else True)

    # Save the audio to a file-like object
    output_file = io.BytesIO()
    tts.write_to_fp(output_file)

    # Load the voiceover audio from the file-like object
    output_file.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)

    # Set the volume
    pygame.mixer.music.set_volume(volume)

    # Play the voiceover audio
    pygame.mixer.music.play()

    # Wait until the voiceover finishes playing
    while pygame.mixer.music.get_busy():
        continue

# Streamlit UI
st.title("Voiceover Generator")
text_input = st.text_area("Enter text to generate voiceover")
voice_gender = st.radio("Select voice gender", ("female", "male"))
speed = st.slider("Select speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
pitch = st.slider("Select pitch", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
lang = st.selectbox("Select language", ("en", "ar"))  # English or Arabic
volume = st.slider("Select volume", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
if st.button("Generate Voiceover"):
    if text_input:
        st.audio(generate_voiceover(text_input, voice_gender, speed, pitch, lang, volume), format='audio/mp3')

