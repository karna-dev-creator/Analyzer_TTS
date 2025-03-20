from gtts import gTTS
from deep_translator import GoogleTranslator
import os
import uuid  # ✅ Use UUID for unique filenames

# Ensure the "audio" folder exists
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

def hindi_trans(text):
    """Convert text to Hindi speech and save as a unique file."""
    
    # Translate English text to Hindi
    translated_text = GoogleTranslator(source="auto", target="hi").translate(text)

    # ✅ Generate a unique filename using UUID
    filename = f"audio_{uuid.uuid4().hex}.mp3"
    file_path = os.path.join(AUDIO_DIR, filename)

    # Convert translated Hindi text to speech
    tts = gTTS(text=translated_text, lang="hi")
    tts.save(file_path)

    return filename  # ✅ Return only the filename
