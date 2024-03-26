import io
import streamlit as st
import requests

def get_available_voices(language='en', voice_gender='female'):
    url = 'https://api.eleven-labs.com/v1/voices'
    params = {
        'language': language,
        'gender': voice_gender,
    }
    headers = {
        'x-api-key': 'e1dc986145b7b5bc3a1a5c2813e3bab9',
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def generate_voiceover(text, voice_id, speed=1.0, pitch=1.0, volume=0.5):
    # Adjust speed, pitch, and volume (not supported by ElevenLabs)
    speed_adjustment = int((speed - 1.0) * 100)  # Adjust speed from -100 to 100 (default: 0)

    # Generate voiceover using ElevenLabs API
    url = 'https://api.eleven-labs.com/v1/tts'
    payload = {
        'text': text,
        'voice_id': voice_id,
        'speed': speed_adjustment,
        'pitch': pitch,
        'volume': volume,
    }
    headers = {
        'x-api-key': 'e1dc986145b7b5bc3a1a5c2813e3bab9',
    }
    response = requests.post(url, json=payload, headers=headers)

    audio = response.content

    return audio

# Streamlit UI
st.title("Voiceover Generator")
text_input = st.text_area("Enter text to generate voiceover")
language = st.selectbox("Select language", ("English", "Arabic"))  # Language selection
voice_gender = st.radio("Select voice gender", ("female", "male"))
if language == "English":
    available_voices = get_available_voices(language='en', voice_gender=voice_gender)
elif language == "Arabic":
    available_voices = get_available_voices(language='ar', voice_gender=voice_gender)
else:
    available_voices = []
voice_options = [voice['name'] for voice in available_voices] if available_voices else []
voice = st.selectbox("Select voice", voice_options)  # Voice selection
speed = st.slider("Select speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
pitch = st.slider("Select pitch", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
volume = st.slider("Select volume", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
if st.button("Generate Voiceover"):
    if text_input:
        if voice in voice_options:
            selected_voice = available_voices[voice_options.index(voice)]
            audio = generate_voiceover(text_input, selected_voice['id'], speed, pitch, volume)
            st.audio(audio, format='audio/mp3')
        else:
            st.error("Invalid voice selection.")

